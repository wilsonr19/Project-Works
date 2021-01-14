from flask import Flask,render_template,request,redirect,url_for
from flask_mysqldb import MySQL
app=Flask(__name__)

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='1999'
app.config['MYSQL_DB']='project'

mysql=MySQL(app)

@app.route('/home')
def home():
	return render_template('index.html')

# @app.route('/login',methods=['GET','POST'])
# def login():
# 	if request.method=='POST':
# 		details = request.form
# 		username = details['uname']
# 		password = details['password']
# 		cursor=mysql.connect().cursor()
# 		cursor.execute("SELECT * FROM signup WHERE username ='" + username + "' and password ='" + password + "'")
# 		result_set = cursor.fetchall()
# 		if result_set is None:
# 			return " wrong"
# 		else:
# 			return "success"
# 	else:
# 		return render_template("login.html")

		

	# 	if len(check)>0:
	# 		return 'success'
	# 	else:
	# 		return redirect('/')
	# else:
	# 	return render_template('login.html')
		# for row in check:



	# return render_template('login.html')



@app.route('/',methods=['GET','post'])
def signup():
	if request.method=='POST':
		details=request.form
		fullname=details['name']
		email=details['mail']
		username=details['uname']
		password=details['password']
		cur=mysql.connection.cursor()
		cur.execute("INSERT INTO signup(fullname,email,username,password) VALUES(%s,%s,%s,%s)",(fullname,email,username,password))
		mysql.connection.commit()
		cur.close()
		return redirect("/home")
	return render_template('signup.html')


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
