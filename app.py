from flask import Flask, render_template,url_for,request,session,redirect
from flask_session import Session
import os
import psycopg2
import urlparse
import traceback

app = Flask(__name__)
sess=Session()
urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])

conn = psycopg2.connect(
	database=url.path[1:],
	user=url.username,
	password=url.password,
	host=url.hostname,
	port=url.port
)
cursor = conn.cursor()
app = Flask(__name__)
sess=Session()


@app.route("/student-register" , methods=['GET','POST'])
def student_register():
	flag= None
	global conn,cursor
	print "Got request"
	print request.method
	if request.method == "POST" :
		form_dict = request.form.to_dict()
		query = "INSERT INTO student (f_name,l_name,email_id,roll_no,git_handle) values ('%s','%s','%s','%s','%s') " % (form_dict["fname"],form_dict["lname"],form_dict["emailid"],form_dict["rollno"],form_dict["githubhandle"])
		try :
			cursor.execute(query)
			conn.commit()
			return render_template('index.html' , flag="Success")
		except :
			conn.rollback()
			print traceback.format_exc()
			return "Addition failed"

@app.route("/project-register" , methods=['GET','POST'])
def project_register():
	flag = None
	global conn,cursor
	print "Got request"
	print request.method
	if request.method == "POST" :
		form_dict = request.form.to_dict()
		index = form_dict['plink'].find("github.com/")
		phandle = form_dict['plink'][index+11:]
		query = "INSERT INTO project (f_name,l_name,email_id,project_link,project_name,project_handle) values ('%s','%s','%s','%s','%s','%s') " % (form_dict["fname"],form_dict["lname"],form_dict["emailid"],form_dict["plink"],form_dict["pname"],phandle)
		try :
			cursor.execute(query)
			conn.commit()
			return render_template('index.html',flag = "Success")
		except :
			conn.rollback()
			print traceback.format_exc()
			return "Addition failed"


@app.route("/")
def main():
	return render_template('index.html')

@app.route("/index")
def index():
	return render_template('index.html')

# if __name__ == "__main__":

app.secret_key = 'kwoc'
app.config['SESSION_TYPE'] = 'filesystem'

sess.init_app(app)
app.debug = True
	# app.run()