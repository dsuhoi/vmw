from os import path

from app.models import Articles
from flask import render_template, request


def render_decorator(arg_list, render_file=None):
    def decorator(func):
        nonlocal render_file
        render_file = func.__name__ + ".html" if not render_file else render_file

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

        wrapper.__name__ = func.__name__
        return wrapper

    return decorator


def params_algorithms(func_reg, params):
    func_reg.params = params


def register_algorithms(func_reg, func, wrapper):
    if not hasattr(func_reg, "FUNC_DICT"):
        func_reg.FUNC_DICT = {}
    func_reg.FUNC_DICT |= {func.__name__: wrapper}


def get_algorithms(func_reg, params, result, task=""):
    algos = func_reg.FUNC_DICT
    res = algos.get(task, list(algos.values())[0])(params)

    result |= func_reg.params if hasattr(func_reg, "params") else {}
    if isinstance(res, tuple):
        result["graphJSON"] = res[0]
        return res[1]
    return res
