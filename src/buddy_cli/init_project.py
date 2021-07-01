from functools import partial

import argparse

from .init_actions import *
from .init_framework import WorkingDirectory, prompt


def init(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--destination", help="The destination of your epic project! :D", required=True)
    parser.add_argument('--force', help="Starts the project from scratch", action='store_true', default=False)
    parser.add_argument('--yes', '-y', help="Forces all boolean options to true", action='store_true', default=None)

    parser.add_action_toggle(setup_mila_user)
    parser.add_action_toggle(create_venv)
    parser.add_action_toggle(create_git_repo)
    parser.add_action_toggle(create_base_structure)
    parser.add_action_toggle(partial(setup_wandb, project_name=""))

    parsed = vars(parser.parse_args(args=args))

    base_dir = parsed['destination']

    prompt_with_args = partial(prompt, parsed_args=parsed)

    with WorkingDirectory(path=base_dir, force=parsed['force']):
        os.mkdir("src")

        prompt_with_args(setup_mila_user)
        prompt_with_args(partial(setup_wandb, project_name=base_dir))

        prompt_with_args(create_git_repo, force=parsed['yes'])
        prompt_with_args(create_venv, force=parsed['yes'])
        prompt_with_args(create_base_structure, force=parsed['yes'])


def sys_main():
    try:
        init()
        return 0
    except Exception as e:
        print(e)
        return 1


if __name__ == '__main__':
    init()
