############################################################
# Dockerfile for easy Raspberry Pi installation
############################################################

# This is a Debian-based image!
FROM continuumio/miniconda3

################## BEGIN INSTALLATION ######################

# Python service dependencies
RUN apt-get update && apt-get install -y sqlite3
RUN conda install -c conda-forge peewee -y
RUN conda install feedparser -y

# Lifted from linkerlab/rpi-omxplayer
#RUN apt-get update -y && apt-get -y install wget ca-certificates libpcre3 libfreetype6 fonts-freefont-ttf dbus libssl1.0.0 libsmbclient libssh-4 fbset libraspberrypi0 && wget https://archive.raspberrypi.org/debian/pool/main/o/omxplayer/omxplayer_0.3.6~git20160102~f544084_armhf.deb && dpkg -i  omxplayer_0.3.6~git20160102~f544084_armhf.deb

# Cron
RUN apt-get install -y cron

##################### INSTALLATION END #####################

# Cron setup from Ekito/docker-cron
ADD crontab /etc/cron.d/hello-cron
RUN chmod 0644 /etc/cron.d/hello-cron
RUN touch /var/log/cron.log

# Move code
WORKDIR /home
ADD . /home

# start a terminal
ENTRYPOINT python models.py && cron && bash
