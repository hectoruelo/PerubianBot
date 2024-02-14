# dockerfile:

FROM selenium/standalone-firefox:4.17.0-20240123
ARG DEBIAN_FRONTEND=noninteractive
RUN sudo apt-get update && \
    sudo apt-get install -y python3 python3-pip git vim tor && \
    sudo git clone https://github.com/hectoruelo/PerubianBot.git
WORKDIR PerubianBot
RUN tor
RUN sudo pip3 install -r requirements.txt

# docker run
docker run -d -p 4444:4444 -p 7900:7900 --shm-size="2g" perubian
