# first step in flas is importing packages
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
# setting app as flask app
app = Flask(__name__)
#configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
#setting database
db = SQLAlchemy(app)

#cfeating new class or table for database
class Blogpost(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	title = db.Column(db.Text, nullable = False)
	content = db.Column(db.String(100), nullable = False)
	author = db.Column(db.String(100), nullable = False, default = 'N/A')
	date_posted = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

	def __repr__(self):
		return 'BlogPost' + str(self.id)

		### To cfreate database we use from app import db(importing database)
		# then db.create_all() it will create a table
		# To operate on table we have to call table as ## from app import table name(Blogpost)
		# To select all values use ## table name.query_all()[Blogpost.query_all()] it will gives all values

		## To add values to database we use ##db.session.add(values of columns which the table contains)like(title='jhj',content='rtee',author='rr')
		## SINCE all values stores as LISTS call by list INDEX call as [table name.query.all()[0](with index and what you want to get).title or content what are the attribute the table contains]
		## To select we use tablename.query.all() [if i want to select particular column call by index or with namr like first ,second,....]
		## if we want to select particular we can use filter_by and if we want in irder we can use order_by and we can use GET() also
		## To DELETE values from database we can use db.session.delete(values[Blogpost.query.get(4)])
		## after this we have commit using db.session.commit()
		## to UPDATE we use tablename.query.get(values as column values.what update you want)
		##ex:[Blogpost.query.get(2).title='Duplicate']

		## AND WHENEVER WE MAKE NEW CHANGES OR WE DO CURD OPERATION WE HAVE TO COMMIT USING DB,SESSION.COMMIT()
#setting route for the app.
# it acts as a domain we can write domain also.
# since we operating on localhost no need to mension domain.
#("/") it represents base routing or default.

# @app.route('/')
# #defining a function which should operate under this route
# def hello():
# 	return "hello world"

#in this we can set route and through web we can call name
# @app.route('/me/<string:name>')
# def hello(name):
# 	return 'Hello,' + name
# all_posts=[
# 	{ 'title': 'Post 1',
# 	'content':'what is that',
# 	'author': 'Robin'
# 	},
# 	{
# 	'title': 'Post 2',
# 	'content': 'what the hell'
# 	}
# ]
## Home page
@app.route('/')
def index():
	return render_template('index.html')

## creating a posts
@app.route('/posts',methods = ['GET','POST'])
def posts():

	if request.method == 'POST':
		post_title = request.form['title']
		post_content = request.form['content']
		post_author = request.form['author']
		new_post = Blogpost(title = post_title, content = post_content, author = post_author)
		db.session.add(new_post)
		db.session.commit()
		return redirect('/posts')
	else:
		all_posts = Blogpost.query.order_by(Blogpost.date_posted).all()

		return render_template('posts.html', posts=all_posts)

# To delete the post#
@app.route('/posts/delete/<int:id>')
def delete(id):
	post = Blogpost.query.get_or_404(id)
	db.session.delete(post)
	db.session.commit()
	return redirect('/posts')

## editing the posts
@app.route('/posts/edit/<int:id>',methods = ['GET','POST'])
def edit(id):
	post = Blogpost.query.get_or_404(id)
	if request.method == 'POST':
		
		post.title = request.form['title']
		post.author = request.form['author']
		post.content = request.form['content']
		db.session.commit()
		return redirect('/posts')
	else:
		return render_template('edit.html', post = post)

## creating new posts
@app.route('/posts/new',methods = ['GET','POST'])
def new_post():
	if request.method == 'POST':
		
		post.title = request.form['title']
		post.author = request.form['author']
		post.content = request.form['content']
		new_post = Blogpost(title = post_title, content = post_content, author = post_author)
		db.session.add(new_post)
		db.session.commit()
		return redirect('/posts')
	else:
		return render_template('new_post.html')


#if we want to change dynamically we can do as
@app.route('/me/users/<string:name>/posts/<int:id>')
def hello(name ,id):
	return "Hello," + name + ", your id is:" + str(id)

@app.route('/onlyget', methods=['GET','POST'])
def get_req():
	return "get only webpage 23"
# finally calling a main function and running a app
if __name__ == '__main__':
	app.run(debug=True)