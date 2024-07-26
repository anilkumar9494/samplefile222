FROM python:3.6
RUN  export DEBIAN_FRONTEND=noninteractive
ENV  DEBIAN_FRONTEND noninteractive
RUN apt-get update && apt-get -y install vim
RUN curl -sL https://deb.nodesource.com/setup_10.x | bash -
RUN apt-get -y update && apt-get -y install nodejs
RUN apt-get -y update && apt-get install -y build-essential
COPY docker_files/req.txt req.txt
RUN pip3 install --no-cache-dir -r req.txt
RUN pip3 install --upgrade pip
