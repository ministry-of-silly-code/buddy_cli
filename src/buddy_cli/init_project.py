import traceback
from git import Repo
import os
import venv
import argparse

from . import init_framework


class Init:
    @staticmethod
    def create_venv():
        '''Create the experiment venv and initializes all the base dependiencies'''
        venv.EnvBuilder().create('venv')

    @staticmethod
    def create_git_repo():
        '''Setups the git repo with the proper git ignores'''
        GIT_IGNORE = """venv"""

        Repo.init('./.git', bare=True)
        with open(".gitignore", "w") as gitignore:
            gitignore.write(GIT_IGNORE)

    @staticmethod
    def create_base_structure():
        '''initializes the base example'''
        os.mkdir("src")


opt_in_functions = {k: v for k, v in Init.__dict__.items() if "staticmethod" in str(v)}


def init(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--destination", help="The destination of your epic project! :D", required=True)
    parser.add_argument('--force', help="Starts the project from scratch", action='store_true', default=False)
    for action in opt_in_functions.values():
        parser.add_function_toggle(action)

    parsed = vars(parser.parse_args(args=args))

    base_dir = parsed['destination']

    with WorkingDirectory(path=base_dir, force=parsed['force']):
        for name, action in opt_in_functions.items():
            prompt(name, create_base_structure, force=parsed[name])


    print(f'Hello {parsed.destination}')


def sys_main():
    try:
        init()
        return 0
    except Exception:
        print(traceback.format_exc())
        return 1


if __name__ == '__main__':
    init()
