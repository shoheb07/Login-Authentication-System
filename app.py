from flask import Flask, render_template, request, redirect, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.secret_key = "secretkey"

# Create Database
def init_db():

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

# Home Page
@app.route('/')
def home():

    if 'user' in session:
        return render_template(
            'dashboard.html',
            username=session['user']
        )

    return redirect('/login')

# Register Page
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        hashed_password =
            generate_password_hash(password)

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        try:

            cursor.execute("""
            INSERT INTO users(username, password)
            VALUES (?, ?)
            """, (username, hashed_password))

            conn.commit()

        except:
            return "Username already exists!"

        finally:
            conn.close()

        return redirect('/login')

    return render_template('register.html')

# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        cursor.execute("""
        SELECT * FROM users
        WHERE username=?
        """, (username,))

        user = cursor.fetchone()

        conn.close()

        if user and check_password_hash(
            user[2],
            password
        ):

            session['user'] = username

            return redirect('/')

        else:
            return "Invalid Username or Password!"

    return render_template('login.html')

# Logout
@app.route('/logout')
def logout():

    session.pop('user', None)

    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
