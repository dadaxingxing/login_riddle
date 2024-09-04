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
    return redirect(url_for('/login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = user_info.find_one({'username': username})

        if user and bcrypt.check_password_hash(user['password'], password):
            session['user'] = username
            return redirect(url_for('dashboard'))
        else:
            return 'Invalid Credential'

    return render_template('login.html')


@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        existing = user_info.find_one({'username': username})

        if existing is None:
            # Hash the password and store it in the database
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            user_info.insert_one({'username': username, 'password': hashed_password})
            
            session['user'] = username
            return redirect(url_for('login'))
        else:
            return 'Existing already exist!'
    
    return render_template('register.html')


@app.route('/dashboard')
def dashboard():
    
    if 'user' in session:
        username = session['user']
        return render_template('dashboard.html', username=username)
    else:
        return redirect(url_for('login'))
    

@app.route('/logout')
def logout():
    del session['user']
    return redirect(url_for('login'))