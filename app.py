from flask import Flask, request, render_template_string
import mysql.connector

app = Flask(__name__)

# Replace with your actual db4free credentials
DB_CONFIG = {
    'host': 'db4free.net',
    'user': 'cloudappuser',
    'password': 'mypassword123',
    'database': 'cloudappdb'
}

@app.route('/', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
            result = cursor.fetchone()
            if result:
                msg = 'Login Successful!'
            else:
                msg = 'Invalid Credentials.'
        except Exception as e:
            msg = f'Error: {e}'
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    return render_template_string("""
        <h2>User Login</h2>
        <form method="post">
            Username: <input name="username"><br>
            Password: <input type="password" name="password"><br>
            <button type="submit">Login</button>
        </form>
        <p>{{ msg }}</p>
    """, msg=msg)

if __name__ == '__main__':
    app.run()
