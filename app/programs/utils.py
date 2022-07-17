from os import path

from app.models import Articles
from flask import render_template, request

ALG_REGISTRATOR = "result"


def render_decorator(arg_list, render_file=None, func_name=None):
    def decorator(func):
        f_name = func_name if func_name else func.__name__
        nonlocal render_file
        render_file = f_name + ".html" if not render_file else render_file

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

        wrapper.__name__ = f_name
        return wrapper

    return decorator


def params_algorithms(func_reg, params, ext_params=dict()):
    func_reg.__params__ = params
    func_reg.__ext_params__ = ext_params


def register_algorithms(func_reg, func, wrapper):
    if not hasattr(func_reg, "FUNC_DICT"):
        func_reg.__func_dict__ = {}
    func_reg.__func_dict__ |= {func.__name__: wrapper}


def get_algorithms(func_reg, params, result, task=None):
    algos = func_reg.__func_dict__
    res = algos.get(task, list(algos.values())[0])(params)
    result |= func_reg.__ext_params__
    if isinstance(res, tuple):
        result["graphJSON"] = res[0]
        return res[1]
    return res


def get_route(desc, module):
    name = module.__name__.split(".")[-1]

    @desc.route("/" + name, methods=["GET"])
    @render_decorator(arg_list=module.result.__params__, func_name=name)
    def callback(task, params, config):
        return get_algorithms(getattr(module, ALG_REGISTRATOR), params, config, task)


def get_routes_for_module(desc, modules_):
    for mod in modules_:
        get_route(desc, mod)
