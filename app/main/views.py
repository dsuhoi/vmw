from . import main
from flask import Flask, request, render_template, redirect, url_for

@main.route('/')
@main.route('/index')
def index():
    return render_template('index.html')

@main.route('/contacts')
def contacts():
    return render_template('contacts.html')

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/program')
def program():
    return render_template('graph.html')

@main.route('/articles')
def articles():
    return render_template('articles.html')
