from flask import Flask, request, render_template, make_response, request, current_app, url_for
from flask_cors import CORS,cross_origin
from datetime import timedelta
from functools import update_wrapper
import json
import numpy as np
import re
import mysql.connector
from scipy import spatial
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
   
		#print(eqn1)
		#eqn2 = request.form["eqn2"]
        #print( name + " Hello")
    return render_template("recom.html")
	
@app.route("/calc",methods=['GET', 'POST','OPTIONS'])
#@crossdomain(origin='*')
@cross_origin(origins='*',support_credentials=True,headers=['Content-Type'])

def calcy():
	l=[]
	if request.method == "POST":
		li=[2,2,1] #call the function to fetch the coeffs of eqns entered
		con= mysql.connector.connect(user='root',password=' ',host='localhost',port='3306',database='equations')
		cursor=con.cursor()
		sql = "SELECT * FROM recom ";
		cursor.execute(sql)
		results = cursor.fetchall()
		print(results)
		print(type(results))
		for i in results:
			result = 1 - spatial.distance.cosine(list(i), li)
			if(result>0.5):
				l.append(i)
				print(i)
			#print(result)
			#print(i)
		#result = 1 - spatial.distance.cosine(a, dataSetII)	
		#eqn1 = request.form["eqn1"]
		#eqn2 = request.form["eqn2"]
		#return "{eqn1:"+eqn1+",eqn2:"+eqn2+"}"
		
		#eq1=request.form["eqn1"]
		#eq2=request.form["eqn2"]
		
		#dataSetII = [2, 54, 13, 15]
		#result = 1 - spatial.distance.cosine(dataSetI, dataSetII)
		#print(result)
		return str(l)
if __name__ == "__main__":
	app.run(host='127.0.0.1', port=443)		