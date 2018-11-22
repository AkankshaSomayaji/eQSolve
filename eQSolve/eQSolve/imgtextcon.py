from flask import Flask, request, render_template, make_response, request, current_app, url_for
from flask_cors import CORS,cross_origin
from datetime import timedelta
from functools import update_wrapper
import json
import numpy as np
import re
import mysql.connector
from flask_uploads import UploadSet, configure_uploads, IMAGES
import mysql.connector

app = Flask(__name__)
CORS(app,support_credentials=True,resources={r'/*':{"origins":'*'}})
app.debug = True

import requests

class OCRSpaceLanguage:
    Arabic = 'ara'
    Bulgarian = 'bul'
    Chinese_Simplified = 'chs'
    Chinese_Traditional = 'cht'
    Croatian = 'hrv'
    Danish = 'dan'
    Dutch = 'dut'
    English = 'eng'
    Finnish = 'fin'
    French = 'fre'
    German = 'ger'
    Greek = 'gre'
    Hungarian = 'hun'
    Korean = 'kor'
    Italian = 'ita'
    Japanese = 'jpn'
    Norwegian = 'nor'
    Polish = 'pol'
    Portuguese = 'por'
    Russian = 'rus'
    Slovenian = 'slv'
    Spanish = 'spa'
    Swedish = 'swe'
    Turkish = 'tur'

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
    return render_template("image_upload.html")	

class OCRSpace:
    def __init__(self, language=OCRSpaceLanguage.English):
        """ ocr.space API wrapper
        :param api_key: API key string
        :param language: document language
        """
        self.api_key = 'ee7e9df0f88895'
        self.language = language
        self.payload = {
            'isOverlayRequired': True,
            'apikey': self.api_key,
            'language': self.language,
        }

    def ocr_file(self, filename):
        """ OCR.space API request with local file
        :param filename: Your file path & name
        :return: Result in JSON format
        """
        with open(filename, 'rb') as f:
            r = requests.post(
                'https://api.ocr.space/parse/image',
                files={filename: f},
                data=self.payload,
            )
			#print r.json()
        return r.json()

photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = 'static/img'
configure_uploads(app, photos)
		
@app.route('/upload', methods=['GET', 'POST'])		
def upload():
	fin=""
	res=""
	#print("------------------------upload")
	if ((request.method == 'POST' or request.method == 'GET') and 'photo' and 'photo2' in request.files):
		#print("---------In if loop-----------")
		"""filename = photos.save(request.files['photo'][0])
		filename2 = photos.save(request.files['photo'][1])
		return filename,filename2"""
		file_obj = request.files
		#print(len(file_obj))
		for f in file_obj:
			print("In for loop")
			file = request.files.get(f)
			filename = photos.save(file,name=file.filename)
			
			#test_file = ocr_space_file(filename='static/img/'+filename, language='eng')
			var1=OCRSpace()
			#print(var1)
			eq=var1.ocr_file('static/img/'+filename)['ParsedResults'][0]['ParsedText']
			#print("hey-----------------------")
			#print(eq)
			#return var1	
			
			#print("hey-----------------------")
			#print(eq)
			eq=eq.replace(" ", "")
			eq.strip()
			print(eq)
			'''eqf=""
			for i in eq:
				if (ord(i)==8212):
					eqf=eqf+"-"
				else:
					eqf=eqf+i
			#print(eqf)
			fin=fin+eqf.strip()+";"'''
		#print(fin)
	'''	eq=fin.split(";")
		print("-------Equations are below--------")
		print(eq[1])
		print(eq[0],eq[1])'''
	return eq
	#return eq
		
if __name__ == "__main__":
	app.run(host='127.0.0.1', port=443)		