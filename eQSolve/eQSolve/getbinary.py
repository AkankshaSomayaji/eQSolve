'''<?php
	//header("Content-type:video/mp4");
	$file = fopen("sample.mp4", "rb");
	
	$retstr = fread($file, 1000000);
	
	echo $retstr; 

?>'''
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
   
		#print(eqn1)
		#eqn2 = request.form["eqn2"]
        #print( name + " Hello")
    return render_template("xhrbinary.html")
	
@app.route("/calc",methods=['GET', 'POST','OPTIONS'])
#@crossdomain(origin='*')
@cross_origin(origins='*',support_credentials=True,headers=['Content-Type'])
def calcy():
	if request.method == "POST":
		print("-----------------------")
		value=request.form["count"]
		print(value)
		#return val
	if(value=="linear"):
		file = open("lineareqnsolve.mp4", "rb")
		result = file.read(1000000)
		#print(result)
		return result
	elif(value=="lcm" or value=="hcf"):	
		file = open("hcfandlcm.mp4", "rb")
		result = file.read(1000000)
		#print(result)
		return result
	else:
		print("Screwed up")
		return "hi"
if __name__ == "__main__":
	app.run(host='127.0.0.1', port=443)	