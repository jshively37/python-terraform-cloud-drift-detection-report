FROM python:3.10.4-slim-buster

LABEL maintainer="jeffrey.shively@hashicorp.com"

ARG USERNAME=devuser
RUN useradd --create-home $USERNAME

RUN apt update && apt -y install git

COPY requirements*.txt /home/$USERNAME/

RUN pip install -r /home/$USERNAME/requirements-dev.txt

USER $USERNAME

WORKDIR /home/${USERNAME}

ENTRYPOINT ["/bin/bash"]
