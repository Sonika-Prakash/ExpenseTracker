from flask import Flask, render_template, session, request, redirect, url_for, json
from flask_mysqldb import MySQL
import MySQLdb.cursors
from datetime import date

app = Flask(__name__)
app.secret_key = 'a'

app.config['MYSQL_HOST'] = 'remotemysql.com'
app.config['MYSQL_USER'] = 'Ri5TBZtQKp'
app.config['MYSQL_PASSWORD'] = '36GxOi5Rk3'
app.config['MYSQL_DB'] = 'Ri5TBZtQKp'
mysql = MySQL(app)

@app.route('/')
def home():
    if not session.get('loggedin'):
        return render_template('signup.html')
    else:
        cursor = mysql.connection.cursor()
        months = ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        labels = json.dumps(["budget", "spent", "remaining"])
        colors = json.dumps(["pink", "lightblue", "green"])
        res1 = cursor.execute("SELECT * FROM transactions WHERE username = %s ORDER BY date", (session['username'], ))
        data1 = cursor.fetchall()
        currentMonth = months[date.today().month]
        data2 = 0
        data3 = 0
        res2 = cursor.execute("SELECT * FROM monthly_budget WHERE username = %s AND month = %s", (session['username'], currentMonth.lower()))
        data = cursor.fetchall()
        if len(data) == 0:
            data2 = 0
            data3 = 0
        else:
            data2 = data[0][3]
            data3 = data[0][4]
        print(data)
        print(data2)
        values = json.dumps([data2, data3, data2 - data3])
        cursor.close()
        if res1 > 0:
            return render_template('home.html', data1 = data1, data2 = data2, data3 = data3, labels = labels, values = values)
        else:
            msg = "There are no transactions made in this month. Add a transaction."
            return render_template('home.html', msg = msg)


@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    msg = ''
    successmsg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE username = %s', (username, ))
        account = cursor.fetchone()
        if account:
            msg = 'Username already exists.'
        else:
            # validate password
            SpecialSym =['!', '$', '@', '#', '%', '&', '*', '^', '_']
            if len(password) < 8:
                msg = 'Password length must be atleast 8!'
                return render_template('signup.html', msg = msg)
            if len(password) > 10:
                msg = 'Password length should not be greater than 10!'
                return render_template('signup.html', msg = msg)
            if not any(char.isdigit() for char in password):
                msg = 'Password should have at least one digit!'
                return render_template('signup.html', msg = msg)
            if not any(char.isupper() for char in password):
                msg = 'Password should have at least one uppercase letter'
                return render_template('signup.html', msg = msg)
                
            if not any(char.islower() for char in password):
                msg = 'Password should have at least one lowercase letter'
                return render_template('signup.html', msg = msg)
                
            if not any(char in SpecialSym for char in password):
                msg = 'Password should have at least one special character'
                return render_template('signup.html', msg = msg)

            # password is validated, insert the new user data into database
            cursor.execute("INSERT INTO users VALUE(%s, %s, %s)", (username, email, password))
            mysql.connection.commit()
            successmsg = 'You have successfully registered! You can login now.'
            
        cursor.close()
        
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('signup.html', msg = msg, successmsg = successmsg)


@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['username'] = account[0]
            session['email'] = account[1]
            print(account)
            msg = 'Logged in successfully!'
            print(msg)
            return redirect(url_for('home'))
        else:
            msg = 'Incorrect credentials!'
            print(msg)
    return render_template('login.html', msg = msg)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    session.pop('email', None)
    msg = 'Logged out successfully!'
    print(msg)
    return redirect(url_for('signup'))

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 8080, debug = True)