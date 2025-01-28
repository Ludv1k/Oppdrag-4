from flask import Flask, render_template, request, redirect, url_for, flash, session
import pymysql #type: ignore
# from werkzeug.security import generate_password_hash, check_password_hash
import re 

# Create the Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key'


db_config = {
    'host': 'localhost',
    'user': 'geir',
    'password': 'gpttrans',
    'database': 'geir_book'
}


def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email)

# Route for the homepage
@app.route('/')
def root():
    first_name = session.get('first_name')
    return render_template('index.html')  # Renders the 'index.html' template

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template('signup.html')

@app.route('/submit', methods=['POST'])
def submit():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    password = request.form['password']

    if not is_valid_email(email):
        flash('Invalid email format.', 'danger')
        return redirect(url_for('signup'))

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

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            conn = pymysql.connect(**db_config)
            cursor = conn.cursor()

            query = "SELECT first_name, password FROM users WHERE email = %s"
            cursor.execute(query, (email,))
            user = cursor.fetchone()
            cursor.close()
            conn.close()

            if user:
                first_name, stored_password = user
                if password == stored_password:
                    session['first_name'] = first_name
                    flash(f'Welcome back, {first_name}!', 'success')
                    return redirect(url_for('registering_book'))
                else:
                    flash('Incorrect password. Please try again', 'danger')
            else:
                flash('No account found with that email. Please sign up.', 'danger')
        except Exception as e:
            flash('An error occurred. Please try again later.', 'danger')
            print(f"Error: {e}")
        
        return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/registering_book', methods=['GET', 'POST'])
def registering_book():
    if 'first_name' not in session:
        flash('Please log in to access this page.', 'danger')
        return redirect(url_for('login'))
    return render_template('registering_book.html')

@app.route('/book', methods=['POST'])
def book():
    name_of_book = request.form['name_of_book']
    author = request.form['author']
    language_for_translation = request.form['language_for_translation']


    try:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        query = "INSERT INTO books (name_of_book, author, language_for_translation) VALUES (%s, %s, %s)"
        cursor.execute(query, (name_of_book, author, language_for_translation))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/')
    except Exception as e:
        flash('An error occurred.', 'danger')
        print(f"Error: {e}")
        return redirect(url_for('root'))

@app.route('/logout')
def logout():
    session.pop('first_name', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('root'))


# Run the Flask app
if __name__ == '__main__':
    # Set the app to be accessible on the network
    app.run(host='0.0.0.0', port=8080, debug=True)
