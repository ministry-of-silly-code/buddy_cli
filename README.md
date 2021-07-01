#Buddy cli

Onboarding tool for experiment buddy

## Installation
### From repo
```shell
git clone git@github.com:ministry-of-silly-code/buddy_cli.git
cd buddy_cli
pip install -e ./buddy-cli
```

### Directly from pip
```shell
pip install -e https://github.com/ministry-of-silly-code/buddy_cli.git
```

## Usage
### Interactive
```shell
buddy-init --destination <your_awesome_project>
cd <your_awesome_project>
```

### With options
```shell
buddy-init --destination sadafa -y --setup_mila_user <your_awesome_user>
cd <your_awesome_project>
```

### Help
```shell
buddy-init --help
```


### To test within a Docker container
```shell
docker build -t buddy-cli-install --build-arg ssh_prv_key="$(cat ~/.ssh/<private_key>)" --build-arg ssh_pub_key="$(cat ~/.ssh/<public_key>.pub)" --squash
docker run -it buddy-cli-install -v ~/.ssh:/root/.ssh
```