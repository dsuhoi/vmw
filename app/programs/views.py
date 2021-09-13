from . import programs
from flask import Flask, request, render_template, redirect, url_for

@programs.route('/')
def index():
    return render_template('programs.html')

