"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, request
from eQSolve import app
from eQSolve import solveeq



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

@app.route('/solveeq', methods=['GET','POST'])
def solveeq():
    print('yo')
    if request.method == "POST":
        eqs=request.form["eqns"]
        print('helllo')
        print(eqs)
        if ',' in eqs:
            eq1,eq2=eqs.split(',')
            res=solveeq.calcy(eq1,eq2)
        else:
            eq=eqs
            res=solveeq.quad(eq)
    return(res)
