import psycopg2, psycopg2.extras
import sys
import datetime
from flask import Flask, flash, redirect, render_template, request, session, url_for
from table_defs import *
app = Flask(__name__)
import sqlite3, hashlib, os
from werkzeug.utils import secure_filename
app = Flask(__name__)

# conn and cur as global variables
conn = psycopg2.connect(host="localhost",
                            database=
                            user=
                            password="
                            )
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

@app.route('/')
def index():
    return 'render_template('index.html', **locals())>'


######################################LOGIN PAGE########################################################
#TODO: #Create Login Page with login verification & if not logged in redirect to account creation
        #verify login through DB
        #
def getLogindetails():
    if 'username' not in session:
            loggedIn = False
            customer_first_name = ""
            customer_id = " "
    else:
        try:
            username = session['username']
            print("username is: ", username)
            sql = "SELECT * FROM customer WHERE username=%s" #DB not yet set up will need to redo query
            cur.execute(sql, (username, ))
            print("trying to fetchone on p")
            p = cur.fetchone()
            print("p is: ", p)
            customer_first_name = p[1]
            customer_id = p[0]
            print("customer_id from inside getLoginDetails: ", customer_id)
            loggedIn = True
        except Exception as e:
            print(e)
            print("Unexpected error:", sys.exc_info()[0])
            loggedIn = False
            customer_first_name = ""
            session.pop('username')
    return (loggedIn, customer_first_name, customer_id)

def valid(username,password):
    print("made it to valid function")
    cur.execute("select username, password from customer where username='"+username+"'")
    print("excecuted valid query")
    user = cur.fetchall()
    try:
        for i in user:
            if username == i[0] and password == i[1]:
                return True
    except Exception as e:
        print(e)
        print("Unexpected error:", sys.exc_info()[0])
        return False
    return True

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
            return render_template('login.html' )
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('staff_name', None)
    return redirect(url_for('index')) 


@app.route("/register",  methods=['GET', 'POST'])
def registration():
    print("I am in registration")
    if request.method == "POST":
        print("I am in the if... POST")
        customer_first_name = request.form.get ('customer_first_name')
        customer_last_name = request.form.get('customer_last_name')
        dUN = request.form.get('username')
        dPW = request.form.get('password')
        #address fields
        street_number = request.form.get ('street_number')
        street_name = request.form.get ('street_name')
        city = request.form.get ('city')
        state = request.form.get ('state')
        zip = request.form.get ('zip')
        # balance (set to 0 for new customer)
        balance = 0

        #queries
        #DB not yet set up query will need to reworked
        addr_check_query = "SELECT address_id FROM address WHERE \
                            street_number=%s AND street_name=%s AND city= %s AND state=%s AND zip=%s"
        addr_insert_query = "INSERT INTO address (street_number, street_name, city, state, zip)  \
                            VALUES  (%s, %s, %s, %s, %s)"
        customer_check_query = "SELECT customer_id FROM customer WHERE username=%s"
        customer_insert_query = "INSERT into customer (customer_first_name, customer_last_name, balance, address_id, username, password)  VALUES  (%s, %s, %s, %s, %s, %s)"
        try:
            print("I am in the try block")
            #check for username exists
            cur.execute(customer_check_query, (dUN,))
            print("executed customer_check_query")
            res = cur.fetchone()
            print("results = ", res)
            if res is None:
                print("res is None block")
                # before inserting into customer insert into address if doesn't already exist:
                cur.execute(addr_check_query, (street_number, street_name, city, state, zip))
                print("executed addr_check_query")
                res = cur.fetchone()
                if res is None:
                    cur.execute(addr_insert_query, (street_number, street_name, city, state, zip))
                    conn.commit()
                    cur.execute(addr_check_query, (street_number, street_name, city, state, zip))
                    res = cur.fetchone()
                    address_id = res[0]
                else:
                    address_id = res[0]
                # now insert into customer using determined address_id:
                cur.execute(customer_insert_query, (customer_first_name, customer_last_name, balance, address_id, dUN, dPW))
                conn.commit()
            else:
                print("Username already taken, please try again")

            return redirect (url_for('loginform'))
        except Exception as f :
            print (f)
            print("In the exception block")
            conn.rollback()
    return render_template("register.html", **locals())

def getLogindetails_staff():
    if 'staff_name' not in session:
            loggedIn = False
            staff_name = " "
            staff_id = " "
    else:
        try:
            staff_name = session['staff_name']
            print("staff_name is: ", staff_name)
            sql2 = "SELECT * FROM staff_member WHERE staff_name=%s"
            cur.execute(sql2, (staff_name, ))
            print("trying to fetchone on p")
            p = cur.fetchone()
            print("p is: ", p)
            staff_name = p[2]
            staff_id = p[0]
            loggedIn = True
        except Exception as e:
            print(e)
            print("Unexpected error:", sys.exc_info()[0])
            loggedIn = False
            staff_name = " "
            session.pop('staff_name')
    return (loggedIn, staff_name, staff_id)

def valid_staff(staff_name, staff_id):
    sql = "select staff_name, staff_id from staff_member where staff_name=%s"
    cur.execute(sql, (staff_name, ))
    staff = cur.fetchall()
    try:
        for i in staff:
            if staff_name == i[0] and int(staff_id) == int(i[1]):
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

@app.route('/index')
def staffloginform():
    print("In staffloginform")
    if request.args.get('staff_name'):
        print("in outer if block")
        s_name = request.args.get('staff_name')
        s_id = request.args.get('staff_id')
        print("s_name", s_name)
        print("s_id", s_id)
        if valid_staff(s_name, s_id):
            print("in inner if block")
            session['staff_name'] = s_name
            print(session['staff_name'])
            print("loginform(): is staff_name in session?")
            print('staff_name' in session)
            return redirect(url_for('add_product'))
        else:
            flash("Invalid credentials")
            return render_template('stafflogin.html' )
    else:
        return render_template('stafflogin.html')

if __name__ == '__main__':
    app.run (debug=True)
