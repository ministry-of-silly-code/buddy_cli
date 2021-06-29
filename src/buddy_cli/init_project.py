import shutil
import subprocess
import traceback
from os.path import expanduser

import fabric
import paramiko
from git import Repo
import os
import venv
import argparse
from distutils.dir_util import copy_tree

from .init_framework import FatalException, WorkingDirectory, prompt_bool, prompt_string


def create_venv():
    """Create the experiment venv and initializes all the base dependencies"""
    venv.EnvBuilder(with_pip=True).create('venv')
    subprocess.check_output(f'venv/bin/python3 -m pip install --upgrade pip', shell=True)
    print(f"""
    
    Remember to source your new environment with:
        source {os.getcwd()}/venv/bin/activate
    """)


def create_git_repo():
    """Setups the git repo with the proper git ignores"""
    GIT_IGNORE = """venv"""

    Repo.init('./.git', bare=True)
    with open(".gitignore", "w") as gitignore:
        gitignore.write(GIT_IGNORE)


def create_base_structure():
    """initializes the base example"""
    base_skeleton_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'base_skeleton')
    copy_tree(base_skeleton_path, '.')
    subprocess.check_output(f'venv/bin/python3 -m pip install -r requirements.txt', shell=True)


def setup_mila_user(mila_user):
    try:
        fabric.Connection(host='login.server.mila.quebec', user=mila_user, connect_timeout=10).run("")
    except paramiko.ssh_exception.SSHException:
        print(f"""
Error while checking SSH connection, stopping
Did you:
 - double check that your username is '{mila_user}'?
 - setup the public and private key for you and for the mila cluster?
        """)
        raise FatalException()

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
    PreferredAuthentications publickey,keyboard-interactive
    Port 2222
    ServerAliveInterval 120
    ServerAliveCountMax 5
"""
    config_path = expanduser('~/.ssh/config')
    with open(config_path, mode='r') as config_file:
        current_config = config_file.read()

    if 'Host mila' not in current_config:
        shutil.copy(config_path, f'{config_path}_BACKUP')
        with open(config_path, mode='w') as config_file:
            config_file.write(current_config + mila_config)


def setup_wandb():
    subprocess.check_output(f'venv/bin/python3 -m pip install wandb', shell=True)
    subprocess.check_output(f'venv/bin/python3 -m wandb init', shell=True)


def init(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--destination", help="The destination of your epic project! :D", required=True)
    parser.add_argument('--force', help="Starts the project from scratch", action='store_true', default=False)

    parser.add_action_toggle(setup_mila_user)
    parser.add_action_toggle(create_venv)
    parser.add_action_toggle(create_git_repo)
    parser.add_action_toggle(create_base_structure)
    parser.add_action_toggle(setup_wandb)

    parsed = vars(parser.parse_args(args=args))

    base_dir = parsed['destination']

    with WorkingDirectory(path=base_dir, force=parsed['force']):
        os.mkdir("src")

        prompt_string(setup_mila_user, prompt='Insert your Mila username', parsed_args=parsed)
        prompt_bool(create_venv, parsed_args=parsed)
        prompt_bool(create_git_repo, parsed_args=parsed)
        prompt_bool(create_base_structure, parsed_args=parsed)
        prompt_bool(setup_wandb, parsed_args=parsed)


def sys_main():
    try:
        init()
        return 0
    except Exception:
        print(traceback.format_exc())
        return 1


if __name__ == '__main__':
    init()
