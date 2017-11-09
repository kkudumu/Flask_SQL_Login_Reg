from flask import Flask, request, redirect, render_template, session, flash, abort, make_response
from mysqlconnection import MySQLConnector
import md5
import os, binascii

app = Flask(__name__)
mysql = MySQLConnector(app,'registration')
app.secret_key = 'abcde12345fghij'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/processreg', methods=["POST"])
def processreg():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']

    if len(request.form['email']) < 1 or len(request.form['first_name']) < 1 or len(request.form['last_name']) < 1 or len(request.form['password']) < 1 or len(request.form['password']) < 1 or len(request.form['confirm_password']) < 1:
        flash("Please do not leave any blank fields")
        return redirect("/")
    elif len(request.form['first_name']) < 2 or len(request.form['last_name']) < 2:
        flash("Names need to be longer than 2 letters")
        return redirect("/")
    elif len(request.form['password']) < 8:
        flash("Password needs to be longer than 8 characters")
        return redirect("/")
    elif request.form['password'] != request.form['confirm_password']:
        flash("Passwords did not match")
        return redirect("/")
    elif (request.form['first_name']).isalpha() == False or (request.form['last_name']).isalpha() == False:
        flash("Names cannot contain any non-alphabetic characters")
        return redirect("/")
    else:
        query = "SELECT EXISTS (SELECT * FROM registration WHERE email = '" + email + "')"
        show_query = mysql.query_db(query)
        for dict in show_query:
            for key in dict:
                if dict[key] == 1:
                    flash('Email already registered')
                    return redirect('/')
                else:
                    #flash('Registration successful')
                    salt = binascii.b2a_hex(os.urandom(15))
                    hashed_pw = md5.new(password + salt).hexdigest()
                    query = "INSERT INTO registration(first_name, last_name, email, salt, password, created, modified) VALUES (:first_name, :last_name, :email, :salt, :password, NOW(), NOW())"
                    data = {'first_name': first_name, 'last_name': last_name, 'email': email, 'salt': salt, 'password': hashed_pw}
                    mysql.query_db(query, data)
                    return redirect('/success')

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/processlog", methods=["POST"])
def processlog():
    email = request.form['email']
    password = request.form['password']
    query = "SELECT * FROM registration WHERE email = :email LIMIT 1"
    data = {'email': email}
    output = mysql.query_db(query, data)
    print output
    if len(output) != 0:
        encrypted_password = md5.new(password + output[0]['salt']).hexdigest()
        # if the hashed passwords match
        if output[0]['password'] == encrypted_password:
            session['userID'] = output[0]['id']
            print session['userID']
            return redirect('/success')
        else:
            flash('PASSWORD INCORRECT')
    else:
        flash('EMAIL DOES NOT EXIST IN DB')
    return redirect('/login')
@app.route("/success")
def success():
        return render_template('success.html')
  


app.run(debug=True)