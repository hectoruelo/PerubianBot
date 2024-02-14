## dockerfile:

##### FROM selenium/standalone-firefox:4.17.0-20240123
##### ENV PATH /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
##### ARG DEBIAN_FRONTEND=noninteractive
##### RUN sudo apt-get update && \
#####     sudo apt-get install -y python3 python3-pip git tor && \
#####     sudo git clone https://github.com/hectoruelo/PerubianBot.git
##### WORKDIR PerubianBot
##### RUN sudo pip3 install -r requirements.txt 
##### CMD ["nohup", "tor", "&"]
##### CMD ["python3", "perubian-tor.py"]

## docker run
##### docker run -itd \
##### -p 4444:4444 \
##### -p 7900:7900 \
##### --shm-size="2g" \
##### --name perubianbot \
##### perubian
