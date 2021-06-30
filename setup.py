from setuptools import setup

setup(
    name="buddy-cli",
    package_dir={'': 'src'},
    packages=['buddy_cli'],
    version="0.0.1",
    install_requires=['halo', 'paramiko', 'fabric', 'gitpython'],
    entry_points={"console_scripts": ["buddy-init=buddy_cli.init_project:sys_main"]}
)
