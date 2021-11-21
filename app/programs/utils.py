from flask import request, render_template

def render_decorator(render_file, arg_list):
    def decorator(func):
        def wrapper():
            result = None
            try:
                task_get = request.args.get('task_list')
                params = {arg: request.args.get(arg) for arg in arg_list}
                if params[arg_list[0]] and params[arg_list[0]]!='':
                    result = {}
                    result['text'] = func(task_get, params, result)
            except Exception as e:
                return render_template(render_file, params=params, error=e.__str__())
            else:
                return render_template(render_file, params=params, result=result)
        return wrapper
    return decorator
