
from flask import render_template

def index():
    return render_template('index.html')

def legend():
    return render_template('legend.html')
