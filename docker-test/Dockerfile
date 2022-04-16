FROM ubuntu:20.04

LABEL org.opencontainers.image.authors="leah.lackner+github@gmail.com"

RUN apt-get update
RUN apt-get install -y git

RUN DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get install -y make build-essential libssl-dev zlib1g-dev \
    libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
    libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev

RUN useradd -m python_user
WORKDIR /home/python_user
USER python_user

RUN curl https://pyenv.run | bash
ENV HOME  /home/python_user
ENV PYENV_ROOT $HOME/.pyenv
ENV PATH $PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH

RUN git clone https://github.com/evyli/evalsys.git
RUN pyenv install $(cat evalsys/.python-version)
RUN pyenv global $(cat evalsys/.python-version)
RUN pyenv rehash