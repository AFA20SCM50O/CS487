import psycopg2, psycopg2.extras
import sys
import datetime
from flask import Flask, flash, redirect, render_template, request, session, url_for
#from table_defs import *
app = Flask(__name__)
import sqlite3, hashlib, os
from werkzeug.utils import secure_filename
app.config['SECRET_KEY'] = 'secret'


app = Flask(__name__)

# conn and cur as global variables
db_settings = {
    "host": "localhost",
    "database": "RideShareApp",
    "user": "postgres",
    "password": "Alfred45"}
conn = psycopg2.connect(**db_settings)
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)


################################Login Page##########################
def getLogindetails():
    if 'username' not in session:
            loggedIn = False
            rider_first_name = ""
            rider_id = " "
    else:
        try:
            username = session['username']
            print("username is: ", username)
            sql = "SELECT * FROM rider WHERE rider_username=%s"
            cur.execute(sql, (username, ))
            print("trying to fetchone on p")
            p = cur.fetchone()
            print("p is: ", p)
            rider_first_name = p[1]
            rider_id = p[0]
            print("rider_id from inside getLoginDetails: ", rider_id)
            loggedIn = True
        except Exception as e:
            print(e)
            print("Unexpected error:", sys.exc_info()[0])
            loggedIn = False
            rider_first_name = ""
            session.pop('username')
    return (loggedIn, rider_first_name, rider_id)

def valid(username,password):
    print("made it to valid function")
    print("username:", username, " type")
    print("password:", password)
    sql = "select rider_username, rider_password from rider where rider_username=%s"
    cur.execute(sql, (username,))
    print("excecuted valid query")
    user = cur.fetchall()
    print("user{}".format(user))
    try:
        for i in user:
            print("i:", i)
            if username == i[0] and password == i[1]:
                print("username:", username)
                print("password:", password)
                return True
    except Exception as e:
        print(e)
        print("Unexpected error:", sys.exc_info()[0])
        return False
# not sure if we need this either could use as example to check login in other routes
# @app.route("/")
# def root():
#     loggedIn, first_name = getLogindetails()
#     cur.execute('SELECT * FROM categories')            
#     categoryData = cur.fetchall()              
#     return render_template('index.html', loggedIn = loggedIn, first_name = first_name, categoryData=categoryData)

@app.route('/index')
def loginform():
    
    if request.args.get('username'):
        username = request.args.get('username')
        print("username =", username)
        password = request.args.get('password')
        print("password=", password)
        if valid(username,password):
            print("in valid block")
            session['username'] = username
            print(session['username'])
            print("loginform(): is username in session?")
            print('username' in session)
            return redirect(url_for('product_search')) #different redirect
        else:
            flash("Invalid credentials")
            return render_template('index.html' )
    else:
        return render_template('index.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('driver_name', None)
    return redirect(url_for('index')) 


@app.route("/register",  methods=['GET', 'POST'])
def registration():
    print("I am in registration")
    if request.method == "POST":
        print("I am in the if... POST")
        rider_first_name = request.form.get ('rider_first_name')
        rider_last_name = request.form.get('rider_last_name')
        dUN = request.form.get('username')
        dPW = request.form.get('password')
        #address fields
        street_number = request.form.get ('street_number')
        street_name = request.form.get ('street_name')
        city = request.form.get ('city')
        state = request.form.get ('state')
        zip = request.form.get ('zip')
        

        #queries
        addr_check_query = "SELECT addresdriver_id FROM address WHERE \
                            street_number=%s AND street_name=%s AND city= %s AND state=%s AND zip=%s"
        addr_insert_query = "INSERT INTO address (street_number, street_name, city, state, zip)  \
                            VALUES  (%s, %s, %s, %s, %s)"
        rider_check_query = "SELECT rider_id FROM rider WHERE rider_username=%s"
        rider_insert_query = "INSERT into rider (rider_first_name, rider_last_name, addresdriver_id, rider_username, rider_password)  VALUES  (%s, %s, %s, %s, %s)"
        try:
            print("I am in the try block")
            #check for username exists
            cur.execute(rider_check_query, (dUN,))
            print("executed rider_check_query")
            res = cur.fetchone()
            print("results = ", res)
            if res is None:
                print("res is None block")
                # before inserting into rider insert into address if doesn't already exist:
                cur.execute(addr_check_query, (street_number, street_name, city, state, zip))
                print("executed addr_check_query")
                res = cur.fetchone()
                if res is None:
                    cur.execute(addr_insert_query, (street_number, street_name, city, state, zip))
                    conn.commit()
                    cur.execute(addr_check_query, (street_number, street_name, city, state, zip))
                    res = cur.fetchone()
                    addresdriver_id = res[0]
                else:
                    addresdriver_id = res[0]
                # now insert into rider using determined addresdriver_id:
                cur.execute(rider_insert_query, (rider_first_name, rider_last_name, addresdriver_id, dUN, dPW))
                conn.commit()
            else:
                print("Username already taken, please try again")

            return redirect (url_for('index'))
        except Exception as f :
            print (f)
            print("In the exception block")
            conn.rollback()
    return render_template("register.html", **locals())

def getLogindetails_driver():
    if 'driver_username' not in session:
            loggedIn = False
            driver_username = " "
            driver_id = " "
    else:
        try:
            driver_name = session['driver_username']
            print("driver_name is: ", driver_username)
            sql2 = "SELECT * FROM driver WHERE driver_username=%s"
            cur.execute(sql2, (driver_username, ))
            print("trying to fetchone on p")
            p = cur.fetchone()
            print("p is: ", p)
            driver_name = p[2]
            driver_id = p[0]
            loggedIn = True
        except Exception as e:
            print(e)
            print("Unexpected error:", sys.exc_info()[0])
            loggedIn = False
            driver_username = " "
            session.pop('driver_username')
    return (loggedIn, driver_username, driver_id)

def valid_driver(driver_username, driver_id):
    sql = "select driver_username, driver_id from driver where driver_username=%s"
    cur.execute(sql, (driver_username, ))
    driver = cur.fetchall()
    try:
        for i in driver:
            if driver_username == i[0] and int(driver_id) == int(i[1]):
                return True
    except:
        return False
# not sure if we need this either could use as example to check login in other routes
# @app.route("/")
# def root():
#     loggedIn, first_name = getLogindetails()
#     cur.execute('SELECT * FROM categories')
#     categoryData = cur.fetchall()
#     return render_template('index.html', loggedIn = loggedIn, first_name = first_name, categoryData=categoryData)

@app.route('/driverlogin')
def driverloginform():
    print("In driverloginform")
    if request.args.get('driver_username'):
        print("in outer if block")
        driver_username = request.args.get('driver_username')
        driver_id = request.args.get('driver_id')
        print("driver_username", driver_username)
        print("driver_id", driver_id)
        if valid_driver(driver_username, driver_id):
            print("in inner if block")
            session['driver_username'] = driver_username
            print(session['driver_username'])
            print("loginform(): is driver_username in session?")
            print('driver_username' in session)
            return redirect(url_for('add_product'))
        else:
            flash("Invalid credentials")
            return render_template('driverlogin.html' )
    else:
        return render_template('driverlogin.html')
if __name__ == '__main__':
    app.run (debug=True)
