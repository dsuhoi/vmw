from os import path

from app.models import Articles
from flask import render_template, request


def render_decorator(render_file, arg_list):
    def decorator(func):
        def wrapper():
            file_name, _ = path.splitext(render_file)
            instruction = Articles.query.filter(Articles.title == file_name).first()
            result = None
            try:
                task_get = request.args.get("task_list")
                params = {arg: request.args.get(arg) for arg in arg_list}
                if params[arg_list[0]] and params[arg_list[0]] != "":
                    result = {}
                    result["text"] = func(task_get, params, result)

            except Exception as e:
                return render_template(
                    render_file,
                    params=params,
                    error=e.__str__(),
                    instruction=instruction,
                )
            else:
                return render_template(
                    render_file, params=params, result=result, instruction=instruction
                )

        return wrapper

    return decorator
