FROM python:3.11.2-buster

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get dist-upgrade -y

# Install dependencies and required tools
RUN apt-get install -y \
    git \
    libsodium-dev \
    python3-nacl

RUN python3 -m pip install --upgrade pip
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y

# ENV CARGO_ROOT /usr/local/cargo
# ENV PATH $PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH
# ENV PATH $POETRY_ROOT/bin:$PATH
# ENV PATH $CARGO_ROOT/bin:$PATH

run export PATH="$HOME/.cargo/bin:$PATH" && python3 -m pip install keri==0.6.8

WORKDIR /keri

# RUN if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
