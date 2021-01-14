from flask import Flask,render_template,request,redirect,url_for,session
#from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
import sqlite3
import os
app=Flask(__name__)

# app.config['MYSQL_HOST']='localhost'
# app.config['MYSQL_USER']='root'
# app.config['MYSQL_PASSWORD']='1999'
# app.config['MYSQL_DB']='project'

# mysql=MySQL(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///retina.db"
db = SQLAlchemy(app)

class signup(db.Model):
	id=db.Column(db.Integer,primary_key = True)
	fullname = db.Column(db.String(200), nullable = False)
	email = db.Column(db.String(200), nullable = False, unique = True)
	username = db.Column(db.String(200), nullable = False)
	password = db.Column(db.String(200), nullable = False)


db.create_all()


@app.route('/')
def home():
	return render_template('index.html')

@app.route('/login',methods=['GET','POST'])
def login():
	if request.method=='POST':
		username = request.form['uname']
		password = request.form['password']
		check = signup.query.filter_by(username = username).all()
		check = signup.query.filter_by(password = password).all()
		if len(check) > 0:
			return "success"
		else:
			return "invalid"
	else:
		return render_template("login.html")
	# 	cursor=mysql.connect().cursor()
	# 	cursor.execute("SELECT * FROM signup WHERE username ='" + username + "' and password ='" + password + "'")
	# 	result_set = cursor.fetchall()
	# 	if result_set is None:
	# 		return " wrong"
	# 	else:
	# 		return "success"
	# else:
	# 	return render_template("login.html")

		

	# 	if len(check)>0:
	# 		return 'success'
	# 	else:
	# 		return redirect('/')
	# else:
	# 	return render_template('login.html')
		# for row in check:



	# return render_template('login.html')



@app.route('/signup', methods=['GET','POST'])
def signup():
	if request.method == 'POST':
		fullname=request.form['name']
		email=request.form['mail']
		username=request.form['uname']
		password=request.form['password']
		add_user = signup(fullname = fullname, email = email, username = username, password = password)
		db.session.add(add_user)
		db.session.commit()
		try:
			db.session.commit()
			return "success"
		except:
			return "wrong"
	return render_template("signup.html")
	# 	cur=mysql.connection.cursor()
	# 	cur.execute("INSERT INTO signup(fullname,email,username,password) VALUES(%s,%s,%s,%s)",(fullname,email,username,password))
	# 	mysql.connection.commit()
	# 	cur.close()
	# 	return redirect("/login")
	# return render_template('signup.html')


@app.route('/upload',methods=['GET','POST'])
def upload():
	return render_template("image.html")


@app.route('/contact',methods=['GET','POST'])
def contact():
	if request.method == 'POST':
		con = request.form
		firstname = con['fname']
		lastname = con['lname']
		email = con['email']
		mobile = con['phno']
		note = con['area']
		cur = mysql.connection.cursor()
		cur.execute("INSERT INTO contact1(firstname,lastname,email,mobile,note) VALUES(%s,%s,%s,%s,%s)",(firstname,lastname,email,mobile,note))
		mysql.connection.commit()
		cur.close()
		return redirect('/')
	return render_template('index1.html')

@app.route('/about',methods=['GET','POST'])
def about():
	return render_template('about.html')


if __name__=='__main__':
	app.run(debug=True)
