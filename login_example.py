from flask import Flask, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
from pymongo import MongoClient
#from flask_ext import PyMongo
import win32api
import bcrypt
import requests


app = Flask(__name__)
client = MongoClient("mongodb://louayayadi:louaylouay@cluster0-shard-00-00-6qbjh.mongodb.net:27017,cluster0-shard-00-01-6qbjh.mongodb.net:27017,cluster0-shard-00-02-6qbjh.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")
db = client.get_database('testdb')
records = db.dbl
app.config['MONGO_DBNAME'] = 'testdb'
app.config['MONGO_URI'] = 'mongodb://louayayadi:louaylouay@cluster0-shard-00-00-6qbjh.mongodb.net:27017,cluster0-shard-00-01-6qbjh.mongodb.net:27017,cluster0-shard-00-02-6qbjh.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority'

mongo = PyMongo(app)

@app.route('/')
def index():
    if 'username' in session and 'password' in session:
        #login_user = records.find_one({'name' : session['username']})
        
        #return 'You are logged in as: ' + session['username']+'<br> Your email is: '+login_user['mail']+ ' <br>Your Country is: ' +login_user['country']+" <br>Your Gender: "+login_user['Gender']
        #request.form['username']=session['username']
        return render_template('registercopy.html')
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    
    users=records
    login_user = users.find_one({'name' : request.form['username']})

    if login_user:
        if request.form['pass']==login_user['password']:
        #if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):
            session['username'] = request.form['username']
            session['password'] = request.form['pass']
            users.find_one({'username': request.form['username']})
            #return redirect(url_for('index'))
            
            return render_template('registercopy.html',username=session['username'],Email=login_user['mail'],gender=login_user['Gender'],Country=login_user['country'])
            
    return 'Invalid username/password combination'
    #alert(text='Invalid username/password combination', title='Error', button='OK')
@app.route('/registercopy', methods=['POST', 'GET'])
def registercopy():
    if request.method == 'POST':
                return render_template('index.html')
@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = records
        existing_user = users.find_one({'name' : request.form['username']})

        if existing_user is None:
            #hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'name' : request.form['username'], 'password' : request.form['pass'],'mail' : request.form['mail'],'country' : request.form['count'],'Gender' : request.form['gdr']})
            session['mail'] = request.form['mail']
            #return redirect(url_for('index'))
            login_user = users.find_one({'name' : request.form['username']})
            #users.find_one({'username': request.form['username']})
            #return redirect(url_for('index'))
            
            return render_template('registercopy.html',username=login_user['name'],Email=login_user['mail'],gender=login_user['Gender'],Country=login_user['country'])
            
        return 'That username already exists!'
        

    return render_template('register.html')

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)