FROM python:3-slim

RUN apt-get update
RUN apt-get install git openssh-client -y
RUN mkdir ~/.ssh && chmod 700 ~/.ssh

# Speed up install process
RUN pip install halo paramiko fabric gitpython

COPY . ./buddy-cli
RUN pip install -e ./buddy-cli

CMD buddy-init --destination sadafa -y --setup_mila_user delvermm --setup_wandb fbb3578351190bb4ccdac3796ed941df8297f936