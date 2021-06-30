import pathlib
import shutil
import subprocess
import traceback
from functools import partial

import fabric
import paramiko
from git import Repo
import os
import venv
import argparse
from distutils.dir_util import copy_tree

from .init_framework import FatalException, WorkingDirectory, prompt


def create_venv():
    """Create the experiment venv and initializes all the base dependencies"""
    venv.EnvBuilder(with_pip=True).create('venv')
    subprocess.check_output(f'venv/bin/python3 -m pip install --upgrade pip', shell=True)
    print(f"""\n\nRemember to source your new environment with:
        source {os.getcwd()}/venv/bin/activate\n\n""")


def create_git_repo():
    """Setups the git repo with the proper git ignores"""
    Repo.init('./.git', bare=True)


def create_base_structure():
    """initializes the base example"""
    base_skeleton_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'base_skeleton')
    copy_tree(base_skeleton_path, '.')
    res = subprocess.check_output(f'venv/bin/python3 -m pip install -r requirements.txt', shell=True)
    print(res)


def setup_mila_user(mila_user: str):
    """One time setup to connect with the Mila servers"""
    try:
        fabric.Connection(host='login.server.mila.quebec', user=mila_user, connect_timeout=10, port=2222).run("")
    except paramiko.ssh_exception.SSHException:
        raise FatalException(f"""
Error while checking SSH connection, stopping
Did you:
 - double check that your username is '{mila_user}'?
 - setup the public and private key for you and for the mila cluster?
""")

    mila_config = f"""
Host mila1
    Hostname login-1.login.server.mila.quebec
Host mila2
    Hostname login-2.login.server.mila.quebec
Host mila3
    Hostname login-3.login.server.mila.quebec
Host mila4
    Hostname login-4.login.server.mila.quebec
Host mila
    Hostname         login.server.mila.quebec
Host mila*
    Port 2222

Match host *.mila.quebec,*.umontreal.ca
    User {mila_user}
    PreferredAuthentications publickey
    Port 2222
    ServerAliveInterval 120
    ServerAliveCountMax 5
"""
    config_path = os.path.expanduser('~/.ssh/config')
    pathlib.Path(config_path).touch()

    current_config = pathlib.Path(config_path).read_text()

    if 'Host mila' not in current_config:
        shutil.copy(config_path, f'{config_path}_BACKUP')
        pathlib.Path(config_path).write_text(f'{current_config}\n{mila_config}')


def setup_wandb(project_name: str, wand_db_key: str):
    """Initialize the wandb project in the current directory"""
    subprocess.check_output(f'venv/bin/python3 -m pip install wandb', shell=True)
    subprocess.check_output(f'venv/bin/python3 -m wandb init -p {project_name}', shell=True)


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
