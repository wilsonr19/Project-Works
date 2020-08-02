import pandas as pd
import numpy as np
import scipy.stats as ss
import sklearn.model_selection as ms
import sklearn.preprocessing as pre
import sklearn.linear_model as lm
import sklearn.metrics as me
import os
import glob
from flask import Flask,render_template,request,redirect,flash,url_for
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.utils import secure_filename
import urllib.request
import pygal


UPLOAD_FOLDER = 'C:/Users/DELL/Desktop/csv'

app=Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['txt','csv', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db = SQLAlchemy(app)

class userlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    reg_timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return("userlist - {}".format(self.id))

def bar_label(data,column_select):
    cat = data.select_dtypes(include = ['object'])
    a = cat[column_select]
    b = a.unique().tolist()
    return b
#bar_label(hous,'MSZoning')  

def bar_value(data,column_select):
    cat = data.select_dtypes(include = ['object'])
    a = cat[column_select]
    b = a.value_counts().tolist()
    return b  

def bins(y):
    maximum = y.max()
    minimum = y.min()
    scale = [ ]
    for i in y:
        scale.append((100*(i-minimum))/(maximum - minimum))
    h = pd.cut(bins = 10,x = scale).value_counts().tolist()
    return h


#flag = 1,gives all the columns with more association,
#but we want less association as less association 
#between independent variable is expected so flag = 0
#Send clean data 
#This was written to identify multicoliniarity but then was not useless
#Thif function gives columns with more or less association between each other
def cram(data,flag,threshold):
    cram = [ ]
    cat = data.select_dtypes(include=['object'])
    #cat.columns
    #cat[cat.columns[1]]
    #len(cat.columns)
    for row in range(1,len(cat.columns)):
        for col in range(row):
            if flag == 1:
                if cramers_v(cat[cat.columns[row]],cat[cat.columns[col]]) > threshold:
                    cram.append([cat.columns.values[row],cat.columns.values[col]])
            else :
                if cramers_v(cat[cat.columns[row]],cat[cat.columns[col]]) < threshold:
                    cram.append([cat.columns.values[row],cat.columns.values[col]])
                
    return cram
#cram(hous,0,0.6)

#Association between catogorical and numerical target
def eta_target(data,target,threshold):
    cat = data.select_dtypes(include=['object'])
    eta = [ ]
    for i in range(len(cat.columns)):
        if(anova_eta(cat[cat.columns[i]],target)) > float(threshold):
            eta.append(cat.columns.values[i])
    return eta
#a = "SalePrice"
#b=eta_target(d,d["survived"],0.5)


#gives association or effect size between target and cat
def anova_eta(categories, measurements):
        fcat, _ = pd.factorize(categories)
        cat_num = np.max(fcat)+1
        y_avg_array = np.zeros(cat_num)
        n_array = np.zeros(cat_num)
        for i in range(0,cat_num):
            cat_measures = measurements[np.argwhere(fcat == i).flatten()]
            n_array[i] = len(cat_measures)
            y_avg_array[i] = np.average(cat_measures)
        y_total_avg = np.sum(np.multiply(y_avg_array,n_array))/np.sum(n_array)
        numerator = np.sum(np.multiply(n_array,np.power(np.subtract(y_avg_array,y_total_avg),2)))
        denominator = np.sum(np.power(np.subtract(measurements,y_total_avg),2))
        if numerator == 0:
            eta = 0.0
        else:
            eta = numerator/denominator
        return eta

#gives association between cat
def cramers_v(x, y):
    confusion_matrix = pd.crosstab(x,y)
    chi2 = ss.chi2_contingency(confusion_matrix)[0]
    n = confusion_matrix.sum().sum()
    phi2 = chi2/n
    r,k = confusion_matrix.shape
    phi2corr = max(0, phi2-((k-1)*(r-1))/(n-1))
    rcorr = r-((r-1)**2)/(n-1)
    kcorr = k-((k-1)**2)/(n-1)
    return np.sqrt(phi2corr/min((kcorr-1),(rcorr-1)))
#cramers_v(hous["Neighborhood"],hous["Street"])


#gives correlation between numerical,actually giving the columns with high relation,so not useful,
#because we doing with target
def correlation(data,threshold):
    result = []
    correlation_matrix = data.corr()
    #print (correlation_matrix)
    for row in range(1,len(correlation_matrix)):
        for col in range(row):
            if correlation_matrix.iloc[row,col] < -threshold or correlation_matrix.iloc[row,col] >  threshold:
                result.append([correlation_matrix.columns.values[row],correlation_matrix.columns.values[col]])
    return result
#correlation(hous,0.8)        


#Gives correlation between target and numerical values
def correlation_target(data,target,threshold):
    resul = [ ]
    num = data.select_dtypes(include=['number'])
    target = target.name
    num = num.drop([target],axis=1)
    #print(num.columns)
    for i in range(len(num.columns)):
        if num[num.columns[i]].corr(data[target])>float(threshold):
            resul.append(num.columns.values[i])
    return resul
#correlation_target(hous,hous['SalePrice'],0.5)    

#Gives last columns with high correlation
def num_lastt(data,target,threshold):
    nume=correlation_target(data,target,threshold)
    for i in range(1,len(nume)):
        #print(i)
        for j in range(i):
         #   print(j)
            try:
                if data[nume[i]].corr(data[nume[j]])>0.5:
                    #print(data[nume[i]].corr(target))
                    #print(nume[j])
                    a = data[nume[i]].corr(target)
                    #print(a)
                    z = data[nume[i]].corr(target)
                    #print(z)
                    if a > z:
                        nume.remove(nume[j])
                    else:
                        nume.remove(nume[i])
            except:
                continue
    return nume
#num_lastt(hous,hous["SalePrice"],0.5)


#Final categorical variables after deleting multicoliniarty 
def cat_lastt(data,target,threshold):
    b=eta_target(data,target,threshold)
    for i in range(1,len(b)):
        for j in range(i):
            try:
                if cramers_v(data[b[i]],data[b[j]])>0.5:
                    a = anova_eta(data[b[i]],target)
                    z =  anova_eta(data[b[j]],target)
                    if a > z:
                        b.remove(b[j])
                    else:
                        b.remove(b[i])
            except:
                break
    return b
#cat_lastt(d,d["survived"],0.05)

def final(data,target,threshold_num,threshold_cat):
    final = [ ]
    cat = cat_lastt(data,target,threshold_cat)
    num = num_lastt(data,target,threshold_num)
    final = cat + num
    return final

def mis_cat(series):
    mode=series.value_counts().index[0]
    series=series.fillna(mode)
    return series

def model(data,feature,target):
    result = { }
    train_mis=data.columns[(data.isnull().sum()/data.shape[0])<.4].tolist()
    train_1=data[train_mis]
    train_cat=train_1.select_dtypes(include=['object'])
    for x in train_cat:
        train_cat[x]=mis_cat(train_cat[x])
    train_int=train_1.select_dtypes(include=['int64'])
    for x in train_int:
        train_int[x]=train_int[x].fillna(np.mean(train_int[x]))
    train_fl=train_1.select_dtypes(include=['float64'])
    for x in train_fl:
        train_fl[x]=train_fl[x].fillna(np.mean(train_fl[x]))
    train_final = pd.concat([train_cat,train_int,train_fl],axis=1)
    Y=train_final[target]
    #print(Y.shape)
    #X =train_final.drop(target,axis = 1)
    X=train_final[feature]
    #print(X.shape)
    col_ob=X.select_dtypes(include=['object']).columns
    for x in col_ob:
        X[x]=pre.LabelEncoder().fit_transform(X[x])
    x_train,x_test,y_train,y_test=ms.train_test_split(X,Y,test_size=0.3,random_state=1)
    linear_reg=lm.LinearRegression()
    linear_reg.fit(x_train,y_train)
    tr= linear_reg.score(x_train,y_train)
    te = linear_reg.score(x_test,y_test)
    result['Train score'] = tr * 100 
    result['Test score'] = te * 100
    return result



@app.route('/', methods=['GET', 'POST'])
def login():
	if request.method == "POST":
		username = request.form["username"]
		password = request.form["password"]
		print(username)
		print(password)
		user_check = userlist.query.filter_by(user_name = username).all()
		user_check = userlist.query.filter_by(password = password).all()
		print(user_check)
		print('above line is user_chek')
		if len(user_check) == 0:
			return "No combination found"
		else:
			return redirect("/homepage")
	else:
		return render_template("login.html")

@app.route("/registration", methods=['GET', 'POST'])
def registration():
	if request.method == "POST":
		user_name = request.form["username"]
		email = request.form["email"]
		password = request.form["password"]
		confirm_password = request.form["password_confirm"]
		if password != confirm_password:
			return "Passwords do not match"
		print("{}, {}, {}".format(
			user_name,  email, password
		))
		new_user = userlist(
			user_name = user_name,
			email = email,
			password = password
		)
		db.session.add(new_user)
		db.session.commit()
		return redirect('/')
		try:

			db.session.commit()
			return(redirect("/"))
		except:
			return "Error Occured in the try catch"
	return render_template("registration.html")



def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/homepage')
def homepage():
    return render_template('homepage1.html')
	
@app.route('/upload')
def upload_form():
	return render_template('index2.html')

@app.route('/upload', methods=['POST'])
def upload_file():
	if request.method == 'POST':
        # check if the post request has the file part
		if 'file' not in request.files:
			print('No file part')#flash
			return redirect(request.url)
		file = request.files['file']
		if file.filename == '':
			print('No file selected for uploading')#flash
			return redirect(request.url)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			#flash('File successfully uploaded')
			return redirect('/visual')
		else:
			print('Allowed file types are txt,csv, pdf, png, jpg, jpeg, gif')#flash
			return redirect(request.url)



# path = r"C:/Users/DELL/Desktop/csv" # use your path
# all_files = glob.glob(path + "/*.csv")
# #li=[]
# for filename in all_files:
#     hous = pd.read_csv(filename, index_col=None, header=0)
#     #li.append(hous)
# #hous=pd.read_csv(r"C:/Users/DELL/Desktop/DataSets/train.csv")
# col = hous.columns.tolist()
# cat = hous.select_dtypes(include = ['object'])
# num = hous.select_dtypes(include = ['number'])
# cat_list = cat.columns.tolist()
# num_list = num.columns.tolist()



    

@app.route('/visual')
def visual():
    return render_template("graph.html",col = col)


@app.route('/graph',methods = ['POST', 'GET'])
def graph():
   if request.method == 'POST':
      user = request.form['graph_column']
      if user in cat_list:
        return redirect(url_for('graphbar',name = user))
      elif user in num_list:
        return redirect(url_for('graphhist',name = user))
   else:
      user = request.args.get('graph_column')
      return redirect(url_for('graph123',name = user))

@app.route('/graphbar/<name>')
def graphbar(name):
    #graph_column = request.form['abc']
    line_chart = pygal.Bar()
    line_chart.title = 'Browser usage evolution (in %)'
    label = bar_label(hous,name)
    value = bar_value(hous,name)
    line_chart.x_labels = label
    line_chart.add(name, value)
    return line_chart.render_response()
    #return name

@app.route('/graphhist/<name>')
def graphhist(name):
    histy = bins(hous[name])
    hist = pygal.Histogram()
    hist.add(name, [(histy[0], 0, 10), (histy[1], 10, 20), (histy[2], 20, 30),(histy[3],30,40),(histy[4],40,50),(histy[5],50,60),(histy[6],60,70),(histy[7],70,80),(histy[8],80,90),(histy[9],90,100)])
    #hist.add('Narrow bars',  [(10, 1, 2), (12, 4, 4.5), (8, 11, 13)])
    #hist.render()
    return hist.render_response()


@app.route('/feature', methods=['GET','POST'])
def feature():
    return render_template('base.html',posts = col)


@app.route('/reg')
def reg(target_model,target):
	score = model(hous,target_model,target)
	return score


@app.route('/display',methods = ['POST','GET'])
def display():
	target=request.form['column']
	numerical = request.form["num"]
	categorical = request.form['cat']
	var = final(hous,hous[target],numerical,categorical)
	#target_model = request.form.getlist('mycheckbox')

	#if request.form['action'] == 'fet':
	score = model(hous,var,target)
	#elif request.form['action'] == 'model-select':
	#return redirect(url_for('reg',target_model= var,target=target))
	return render_template('base.html',score=score, posts= col,var=var)

	#if 'fet' in request.form:
	#score = model(hous,var,target)
	#if 'model-select' in request.form:
	#	target_model = request.form.getlist('mycheckbox')
	#	score = model(hous,target_model,target)
	#return render_template('base.html', posts= col,score = score,var=var)

 #malkondu nidhe maadu 




#final(,d["survived"],0.5,0.3)    
#@app.route('/display',methods = ['POST','GET'])
#def display():
	#if request.form.post['action'] == 'fet':
#	if 'fet' in request.form :
		#request.method == 'POST': 
#		target=request.form['column']
#		numerical = request.form["num"]
#		categorical = request.form['cat']
		#return " %s " %numerical
#		var = final(hous,hous[target],numerical,categorical)
		#return render_template('base.html', posts= col,var=var,target_model = target_model)
#	if 'model' in request.form :
	#if request.form.post['action'] == 'model':
		#if request.method == "POST":
#		target_model = request.form.getlist('mycheckbox')
#		score = model(hous,target_model,target)
#	return render_template('base.html', posts= col,score = score,var=var,target_model = target_model)
	#return render_template('base.html',posts = col ,target_model = target_model)
	#return "Welcome"
	
	


if __name__ == '__main__':
   app.run(debug = True)