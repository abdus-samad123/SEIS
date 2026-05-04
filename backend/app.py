from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def get_db():
    return sqlite3.connect('database.db')


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
    user = cursor.fetchone()

    conn.close()

    if user:
        return jsonify({"status": "success"})
    return jsonify({"status": "fail"})


@app.route('/logout', methods=['POST'])
def logout():
    return jsonify({"status": "logged_out"})


@app.route('/forgot-password', methods=['POST'])
def forgot_password():
    email = request.json.get('email')
    return jsonify({"message": f"Reset link sent to {email}"})


if __name__ == '__main__':
    app.run(debug=True)
