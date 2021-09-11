from . import main
from flask import Flask, request, render_template, redirect, url_for

@main.route('/')
@main.route('/index')
def index():
    import math as m

    return f"<p>Hello, World!!! {m.sin(12)}</p>"
