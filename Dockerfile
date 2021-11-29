FROM ubuntu:20.04 
RUN apt-get -y update \ 
    && apt-get -y install --no-install-recommends \
    build-essential \
    python3-dev \
    python3-pip \
    libffi-dev \
    libssl-dev \
    openssh-client \
    rsync \
    git \
    unzip
RUN pip3 install --upgrade pip setuptools \
    && ln -sf pip3 /usr/bin/pip \
    && ln -sf /usr/bin/python3 /usr/bin/python
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
COPY webexteamssdk /webexteamssdk
RUN pip install /webexteamssdk
ADD https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip /tmp/ngrok.zip
RUN set -x \
    && unzip -o /tmp/ngrok.zip -d /bin
WORKDIR network_assistant_bot
ENTRYPOINT ["bash"]
