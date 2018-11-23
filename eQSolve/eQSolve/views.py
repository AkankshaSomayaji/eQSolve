"""
Routes and views for the flask application.
"""

from datetime import datetime
import werkzeug
from eQSolve.solveeq import calcy
from eQSolve.solveeq import quad
from flask import render_template, request, url_for
from eQSolve import app
from eQSolve import solveeq
from eQSolve.models import User,Equation,UserToEq
from eQSolve import db
import json
import random
from werkzeug.utils import secure_filename
import os
from eQSolve.ImageToText import GetImageData


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']




@app.route('/')
def index():
    """Renders the main page"""
    return render_template(
        'main.html',
        title='eQSolve',
        year = datetime.now().year,
        backgroundColor = "#ff7f50",
        headerColor = "#2f3542"
        )

@app.route('/solve')
def solve():
    """Renders the main page"""
    return render_template(
        'solve.html',
        title='eQSolve',
        year = datetime.now().year,
        backgroundColor = "#d72323",
        headerColor = "#2a363b"
        )


@app.route('/about')
def about():
    """Renders the main page"""
    return render_template(
        'about.html',
        title='eQSolve',
        year = datetime.now().year,
        backgroundColor = "#d72323",
        headerColor = "#2a363b"
        )


@app.route('/explore')
def explore():
    return render_template(
        'explore.html',
        title='eQSolve - Explore',
        year = datetime.now().year,
        backgroundColor = "#d72323",
        headerColor = "#2a363b"
        )


@app.route('/solveeq', methods=['GET','POST'])
def solveeq():
    #print('yo')
    if request.method == "POST":
        #print("helo")
        eqs= request.data
        eqs= eqs.decode("utf-8")
        #print(eqs)
        if "," in eqs:
            try:
                eq1,eq2=eqs.split(",")
                res=calcy(eq1,eq2)

            except:
                res = "Error"
            if res !="Error":
                db_e = Equation(eq1=eq1,eq2=eq2,sol=res)
                try:
                    db.session.add(db_e)
                    db.session.commit()
                except:
                    print("DB failed")
            
        else:
            try:
                eq=eqs
                
            except:
                res="Error"

            res=quad(eq)
            if res !="Error":
                #db stuff
                db_e = Equation(eq1=eq,sol=res);
                try:
                    db.session.add(db_e)
                    db.session.commit()
                except:
                    print("DB failed")

    return(res)


@app.route('/linear/rand',methods=['GET'])
def LinearRand():
    allEq = Equation.query.all()
    res = random.randint(2,len(allEq)-2)
    a = Equation.query.filter_by(id=res).first()

    if a.eq2 is None:
        e2 = "NA"
        e1 = a.eq1
        sol = a.sol
    else:
        e1 = a.eq1
        e2 = a.eq2
        sol = a.sol
    print(e1)
    print(e2)
    print(sol)
    return e1+","+e2+","+sol

@app.route('/linear',methods=['GET'])
def linear():
    allEq = Equation.query.filter(Equation.eq2 != None).all()
    i = random.sample(range(0,len(allEq)-1),4)
    retStr = ""
    for j in range(len(i)):
        if(j == 0):
            retStr = retStr + allEq[i[j]].eq1
        else:
            retStr = retStr + "," + allEq[i[j]].eq1
        retStr = retStr + "," + allEq[i[j]].eq2
        retStr = retStr + "," + allEq[i[j]].sol
    print(retStr)
    return retStr

@app.route('/quad',methods=['GET'])
def quad():
    allEq = Equation.query.filter(Equation.eq2 == None).all()
    i = random.sample(range(0,len(allEq)-1),4)
    retStr = ""
    for j in range(len(i)):
        if(j == 0):
            retStr = retStr + allEq[i[j]].eq1
        else:
            retStr = retStr + "," + allEq[i[j]].eq1
        retStr = retStr + ",NA"
        retStr = retStr + "," + allEq[i[j]].sol
    return retStr


@app.route('/upload',methods=['GET','POST'])
def upload_file():
    if request.method == 'POST':
        if 'pic' not in request.files:
            return "Failed"
        print("here")
        file = request.files['pic']
        print("file got")
        if file.filename == '':
            return "No file uploaded"
        if file and allowed_file(file.filename):
            print("entered if")
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            t = GetImageData()
            g = t.m()
            return g
            
