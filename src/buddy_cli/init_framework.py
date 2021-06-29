import argparse
import inspect
import os
from typing import Optional, Callable, Union, Dict, Any

from halo import Halo


class FatalException(Exception):
    pass


def exec_in_venv(python_command):
    os.system(f'venv/bin/python {python_command}')


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


def prompt_bool(action: Callable[[], None], parsed_args: Dict[str, Any]):
    force_to = parsed_args[action.__name__]

    if force_to is None:
        apply = input(f"Do you want to {action.__name__.replace('_', ' ')}? [Yn] ") in ['', 'y', 'Y']
    else:
        apply = force_to

    if apply:
        with Halo(text=action.__name__.replace('_', ' '), spinner='dots'):
            action()

    return apply


def prompt_string(action: Callable[[str], None], prompt: str, parsed_args: Dict[str, Any]):
    force_to = parsed_args[action.__name__]

    if force_to is None:
        param = input(f"Do you want to {action.__name__.replace('_', ' ')}? {prompt} [Leave empty to skip]")
    else:
        param = force_to

    if param:
        with Halo(text=action.__name__.replace('_', ' '), spinner='dots'):
            action(param)

    return param


def add_action_toggle(self, fn: Union[Callable[[], None], Callable[[str], None]]):
    params = list(inspect.signature(fn).parameters.keys())
    if params:
        self.add_argument(f'--{fn.__name__}', help=fn.__doc__, default=None)
    else:
        self.add_argument(f'--{fn.__name__}', help=fn.__doc__, action='store_true', default=None)


argparse.ArgumentParser.add_action_toggle = add_action_toggle
