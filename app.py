from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql #type: ignore
from werkzeug.security import generate_password_hash, check_password_hash
import re 

# Create the Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key'


db_config = {
    'host': 'localhost',
    'user': 'ludvik',
    'password': 'Seidou',
    'database': 'geir_book'
}


def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email)

# Route for the homepage
@app.route('/')
def root():
    return render_template('index.html')  # Renders the 'index.html' template

@app.route('/signup', methods=['GET', 'PoST'])
def signup():
    if request.method == 'POST':
        print(request.form['first_name'])
    return render_template('signup.html')

@app.route('/submit', methods=['POST'])
def submit():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    password = request.form['password']

    if not is_valid_email(email):
        flash('Invalid email format.', 'danger')
        return redirect(url_for(signup))

    # hashed_password = generate_password_hash(password, method='sha256')

    try:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (first_name, last_name, email, password))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/')
    except Exception as e:
        flash('Email already exists or another error occurred.', 'danger')
        print(f"Error: {e}")
        return redirect(url_for('signup'))



# Run the Flask app
if __name__ == '__main__':
    # Set the app to be accessible on the network
    app.run(host='0.0.0.0', port=8080, debug=True)
