from flask import Flask, request, render_template, make_response, request, current_app, url_for
from flask_cors import CORS,cross_origin
from datetime import timedelta
from functools import update_wrapper
import json
import numpy as np
import re
import mysql.connector

app = Flask(__name__)
CORS(app,support_credentials=True,resources={r'/*':{"origins":'*'}})
app.debug = True

def crossdomain(origin=None, methods=None, headers=None, max_age=21600,
                attach_to_all=True, automatic_options=True):
    """Decorator function that allows crossdomain requests.
      Courtesy of
      https://blog.skyred.fi/articles/better-crossdomain-snippet-for-flask.html
    """
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, list):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, list):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        """ Determines which methods are allowed
        """
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        """The decorator function
        """
        def wrapped_function(*args, **kwargs):
            """Caries out the actual cross domain code
            """
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers
            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            h['Access-Control-Allow-Credentials'] = 'true'
            h['Access-Control-Allow-Headers'] = \
                "Origin, X-Requested-With, Content-Type, Accept, Authorization"
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

@app.route("/", methods=['GET', 'POST','OPTIONS'])
#@crossdomain(origin='*')
@cross_origin(origins='*',support_credentials=True)
def index():
    #@cross_origin(origins="*",support_credentials=True)
    if request.method == "POST":
        eqn1 = request.form["eqn1"]
		#print(eqn1)
		#eqn2 = request.form["eqn2"]
        #print( name + " Hello")
    return render_template("om.html")
	
@app.route("/calc",methods=['GET', 'POST','OPTIONS'])
#@crossdomain(origin='*')
@cross_origin(origins='*',support_credentials=True,headers=['Content-Type'])
def calcy():
	if request.method == "POST":
		#eqn1 = request.form["eqn1"]
		#eqn2 = request.form["eqn2"]
		#return "{eqn1:"+eqn1+",eqn2:"+eqn2+"}"
		
		eq1=request.form["eqn1"]
		eq2=request.form["eqn2"]
		
		print(eq1)
		print(eq2)

		s1=eq1.split("=")
		s2=eq2.split("=")

		c1=float(s1[1].strip())
		c2=float(s2[1].strip())
		flag1=0
		
		r1=re.match("([0-9]+)(.?)([0-9]*)\*([a-z]+)(\+|-?)([0-9]*)([.]?)([0-9]*)\*?([a-z]*)",s1[0].strip())
		#print(r1.groups())
		if(r1):
			if(r1.groups()[3]==r1.groups()[8] and r1.groups()[3]!=''):
				a1=float(r1.groups()[0]+(r1.groups()[1])+(r1.groups()[2]))+float(r1.groups()[4]+(r1.groups()[5])+(r1.groups()[6])+(r1.groups()[7]))
				b1=float(0)
				#print(c1/a1)
			elif(r1.groups()[3]!=r1.groups()[8] and r1.groups()[3]!='' and r1.groups()[8]!=''):
				a1=float(r1.groups()[0]+(r1.groups()[1])+(r1.groups()[2]))
				b1=float(r1.groups()[4]+(r1.groups()[5])+(r1.groups()[6])+(r1.groups()[7]))
				flag1=1
			elif(r1.groups()[3]!=r1.groups()[8] and r1.groups()[8]==''):
				a1=float(r1.groups()[0]+(r1.groups()[1])+(r1.groups()[2]))
				b1=float(0)
				c1=c1-float(r1.groups()[4]+(r1.groups()[5])+(r1.groups()[6])+(r1.groups()[7]))
				flag1=2
				#print(c1/a1)

		flag2=0	
		r2=re.match("([0-9]+)(.?)([0-9]*)\*([a-z]+)(\+|-?)([0-9]*)([.]?)([0-9]*)\*?([a-z]*)",s2[0].strip())
		#print(r2.groups())
		if(r2):
			if(r2.groups()[3]==r2.groups()[8] and r2.groups()[3]!=''):
				a2=float(r2.groups()[0]+(r2.groups()[1])+(r2.groups()[2]))+float(r2.groups()[4]+(r2.groups()[5])+(r2.groups()[6])+(r2.groups()[7]))
				b2=float(0)
				#print(c2/a2)
			elif(r2.groups()[3]!=r2.groups()[8] and r2.groups()[3]!='' and r2.groups()[8]!=''):
				a2=float(r2.groups()[0]+(r2.groups()[1])+(r2.groups()[2]))
				b2=float(r2.groups()[4]+(r2.groups()[5])+(r2.groups()[6])+(r2.groups()[7]))
				flag2=1
			elif(r2.groups()[3]!=r2.groups()[8] and r2.groups()[8]==''):
				a2=float(r2.groups()[0]+(r2.groups()[1])+(r2.groups()[2]))
				b2=float(0)
				c2=c2-float(r2.groups()[4]+(r2.groups()[5])+(r2.groups()[6])+(r2.groups()[7]))
				flag2=2
				#print(c2/a2)
		
		#print(a1,b1,c1,a2,b2,c2)
		con= mysql.connector.connect(user='root',password=' ',host='localhost',port='3306',database='equations')
		cursor=con.cursor()

		id=con.cursor()
		q1="SELECT max(id) from recommendations" 
		id.execute(q1)
		mid = id.fetchone()[0]
		mid=mid+1
		args=(a1,b1,c1,mid)
		cursor.execute("insert into recommendations(a,b,c,id) values(%s,%s,%s,%s)",args)
		print('one row insert')
		
		args=(a2,b2,c2,mid+1)
		cursor.execute("insert into recommendations(a,b,c,id) values(%s,%s,%s,%s)",args)
		print('one row insert')
		
		con.commit()
		cursor.close()
		con.close()
		res=''
		if(flag1==1 and flag2==1):
			a = np.array([[a1,b1], [a2,b2]])
			b = np.array([c1,c2])
			x = np.linalg.solve(a, b)
			return(str(x[0])+str(x[1]))
		
		if(flag1==0 or flag1==2):
			res=res+str(c1/a1)
		if(flag2==0 or flag2==2):
			res=res+str(c2/a2)
		print(res)
		return res
	return "Error"

'''@app.after_request
def add_headers(response):
	response.headers.add('Access-Control-Allow-Origin','*')
	response.headers.add('Access-Control-Allow-Headers','Content-Type,Authorization')
'''
	
if __name__ == "__main__":
	app.run(host='127.0.0.1', port=443)