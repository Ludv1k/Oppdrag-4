from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import re 

# Create the Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key'


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'ludvik'
app.config['MYSQL_PASSWORD'] = 'Seidou'
app.config['MYSQL_DATABASE'] = 'user_auth'

mysql = MySQL(app)


def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email)

# Route for the homepage
@app.route('/')
def root():
    return render_template('index.html')  # Renders the 'index.html' template

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']

        if not is_valid_email(email):
            flash('Invalid email format.', 'danger')
            return redirect(url_for(signup))
        
        hashed_password = generate_password_hash(password, method='sha256')
        
        try:
            cursor = mysql.connection.cursor()
            cursor.execute(
                "INSERT INTO users (first_name, last_name, email, password) VALUES (%s, %s, %s, %s)",
                (first_name, last_name, email, hashed_password)
            )
            mysql.connection.commit()
            cursor.close()
            flash('Account created successfully!', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash('Email already exists or another error occurred.', 'danger')
            print(f"Error: {e}")
            return redirect(url_for('signup'))
    return render_template('signup.html')



# Run the Flask app
if __name__ == '__main__':
    # Set the app to be accessible on the network
    app.run(host='0.0.0.0', port=8080, debug=True)
