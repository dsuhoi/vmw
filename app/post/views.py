from . import post
from flask import Flask, request, render_template, redirect, url_for

@post.route('/')
def index():
    return render_template('post.html')


