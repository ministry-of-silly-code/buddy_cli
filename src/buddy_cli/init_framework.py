import argparse
import inspect
import os
from typing import Callable, Union, Dict, Any

from halo import Halo


class FatalException(Exception):
    pass


def coalesce(*arg):
    for el in arg:
        if el is not None:
            return el
    return None


def get_fn_parameters(action):
    if hasattr(action, 'func'):
        return list(set(inspect.signature(action).parameters) - set(action.keywords.keys()))
    else:
        return list(inspect.signature(action).parameters)


class WorkingDirectory:

    def __init__(self, *, path, force):
        if force:
            os.system(f"rm -rf {path}")
        elif os.listdir(path):
            raise Exception("The directory exists and it's not empty")

        os.makedirs(path)
        self.base_path = path
        self.current_path = os.getcwd()

    def __enter__(self):
        os.chdir(self.base_path)
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        os.chdir(self.current_path)


def prompt(action: Union[Callable[[], None], Callable[[str], None]],
           parsed_args: Dict[str, Any],
           force=None):
    def unsnake(string):
        return string.replace('_', ' ')

    action_name = getattr(action, 'func', action).__name__
    param_names = get_fn_parameters(action)

    apply = coalesce(force, parsed_args[action_name])
    if apply is None:
        if param_names:
            apply = input(f"Do you want to {unsnake(action_name)}? "
                          f"Insert your {unsnake(param_names[0])} [Leave empty to skip]: ")
        else:
            apply = input(f"Do you want to {unsnake(action_name)}? [Yn] ") in ['', 'y', 'Y']

    if apply:
        with Halo(text=unsnake(action_name), spinner='bouncingBar'):
            if param_names:
                action(**{param_names[0]: apply})
            else:
                action()

    return apply


def add_action_toggle(self, fn: Union[Callable[[], None], Callable[[str], None]]):
    params = get_fn_parameters(fn)
    docs = getattr(fn, 'func', fn).__doc__
    name = getattr(fn, 'func', fn).__name__
    if params:
        self.add_argument(f'--{name}', help=docs, default=None, metavar=params[0])
    else:
        self.add_argument(f'--{name}', help=docs, action='store_true', default=None)


argparse.ArgumentParser.add_action_toggle = add_action_toggle
