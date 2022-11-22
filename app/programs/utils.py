from os import path
from types import ModuleType
from typing import Callable

from app.models import Articles
from flask import Blueprint, render_template, request

ALG_REGISTRATOR = "result"


def render_decorator(
    arg_list: list[str], render_file: str = None, func_name: str = None
):
    """
    Wraps the route for the program algorithm.

    arg_list - a list of names of arguments required by the program (names as in .html).
    render_file - html file (template) where data is sent.
    func_name - name of the function other than the default value.
    """

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


def params_algorithms(func_reg: Callable, params: list[str], ext_params=dict()):
    func_reg.__params__ = params
    func_reg.__ext_params__ = ext_params


def register_algorithms(func_reg: Callable, func: Callable, wrapper: Callable):
    """
    Registration of algorithm-functions.
    func_reg - A decorator that registers a function.
    func - algorithm-function.
    wrapper - wrapper of algorithm-function.
    """
    if not hasattr(func_reg, "FUNC_DICT"):
        func_reg.__func_dict__ = {}
    func_reg.__func_dict__ |= {func.__name__: wrapper}


def get_algorithms(
    func_reg: Callable, params: list[str], result: dict, task: str = None
):
    algos = func_reg.__func_dict__
    res = algos.get(task, list(algos.values())[0])(params)
    result |= func_reg.__ext_params__
    if isinstance(res, tuple):
        result["graphJSON"] = res[0]
        return res[1]
    return res


def get_route(desc: Blueprint, module: ModuleType):
    name = module.__name__.split(".")[-1]

    @desc.route("/" + name, methods=["GET"])
    @render_decorator(arg_list=module.result.__params__, func_name=name)
    def callback(task, params, config):
        return get_algorithms(getattr(module, ALG_REGISTRATOR), params, config, task)


def get_routes_for_module(desc: Blueprint, module_list: list[ModuleType]):
    """
    Creation and registration of algorithm function paths.
    desc - flask path descriptor.
    """
    for mod in module_list:
        get_route(desc, mod)
