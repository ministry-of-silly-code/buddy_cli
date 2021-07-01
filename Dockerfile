FROM python:3-slim

ARG ssh_prv_key
ARG ssh_pub_key

RUN mkdir /root/.ssh && chmod 700 /root/.ssh
RUN echo "$ssh_prv_key" > /root/.ssh/id_rsa && \
    echo "$ssh_pub_key" > /root/.ssh/id_rsa.pub && \
    chmod 600 /root/.ssh/id_rsa && \
    chmod 600 /root/.ssh/id_rsa.pub

RUN apt-get update
RUN apt-get install git openssh-client -y

# Speed up install process
RUN pip install halo paramiko fabric gitpython

COPY . ./buddy-cli
RUN pip install -e ./buddy-cli

CMD buddy-init --destination sadafa -y --setup_mila_user delvermm --setup_wandb fbb3578351190bb4ccdac3796ed941df8297f936