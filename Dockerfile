FROM ubuntu:bionic

RUN dpkg --add-architecture i386
RUN apt-get update &&									\
	apt-get install -y virtualenvwrapper python3-dev python3-pip build-essential libxml2-dev libxslt1-dev git libffi-dev cmake libreadline-dev libtool debootstrap debian-archive-keyring libglib2.0-dev libpixman-1-dev qtdeclarative5-dev binutils-multiarch nasm libc6:i386 libgcc1:i386 libstdc++6:i386 libtinfo5:i386 zlib1g:i386 vim libssl-dev openjdk-8-jdk

RUN useradd -s /bin/bash -m angr

RUN su - angr -c "git clone https://github.com/angr/angr-dev && cd angr-dev && ./setup.sh -w -e angr && ./setup.sh -w -p angr-pypy"
RUN su - angr -c "echo 'workon angr' >> /home/angr/.bashrc"
RUN su - angr -c "source /home/angr/.virtualenvs/angr/bin/activate && pip3 install pymongo flask"
WORKDIR /home/angr/server/
ADD ./ /home/angr/server/
CMD su - angr -c "source /home/angr/.virtualenvs/angr/bin/activate && python3 server/server.py"
