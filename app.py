from flask import Flask, render_template, request, redirect, url_for, session
from flask_bcrypt import Bcrypt
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client["mydatabase"]
user_info = db['users']

app = Flask(__name__)
app.secret_key = 'supersecretkey'
bcrypt = Bcrypt(app)


@app.route('/')
def default():
    return 'hello!'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = user_info.find_one({'username': username})

        if user and bcrypt.check_password_hash(user['password'], password):
            session['user'] = username
            return redirect(url_for('login'))
        else:
            return 'Invalid Credential'

    return render_template('login.html')