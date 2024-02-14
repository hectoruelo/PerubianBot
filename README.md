## dockerfile:

##### FROM selenium/standalone-firefox:4.17.0-20240123
##### ARG DEBIAN_FRONTEND=noninteractive
##### RUN sudo apt-get update && \
#####     sudo apt-get install -y python3 python3-pip git tor && \
#####     sudo git clone https://github.com/hectoruelo/PerubianBot.git
##### WORKDIR PerubianBot
##### RUN sudo pip3 install -r requirements.txt 
##### RUN nohup tor & 
##### RUN /usr/bin/python3 perubianbot-tor.py 

## docker run
##### docker run -itd --rm \
##### -p 4444:4444 \
##### -p 7900:7900 \
##### --shm-size="2g" \
##### --name perubianbot \
##### perubian
