import argparse
from typing import Optional, Callable


class WorkingDirectory():
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


def prompt(name, action: Callable, force_to: Optional[bool] = None):
    if force_to is None:
        apply = input(f"Do you want to {name.replace('_', ' ')}? [Yn] ") in ['', 'y', 'Y']
    else:
        apply = force_to

    if apply:
        action()


def add_function_toggle(self, fn):
    self.add_argument(f'--{fn.__name__}', help=fn.__doc__, action='store_true', default=False)


argparse.ArgumentParser.add_function_toggle = add_function_toggle
