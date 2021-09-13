from . import discrete_math as dscm
from flask import Flask, request, render_template, redirect, url_for

@dscm.route('/')
def index():
    return render_template('discrete_math.html')

