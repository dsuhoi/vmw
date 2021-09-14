from . import discrete_math as dscm
from flask import Flask, request, render_template, redirect, url_for

@dscm.route('/')
def index():
    return render_template('discrete_math.html')

@dscm.route('/graphs', methods=['GET'])
def graphs():
    try:
        matrix_get = request.args.get('matrix')
        task_get = request.args.get('task_list')
        if matrix_get and matrix_get !='':
            matrix_get = [[int(x) for x in row.split(' ')] for row in
                    matrix_get.split('\r\n')]
    except Exception as e:
        return render_template('graphs.html', error=e.__str__())
    else:
        l = {'text': (matrix_get, task_get)}
        return render_template('graphs.html', result=l)
