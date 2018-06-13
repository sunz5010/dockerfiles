FROM ubuntu:latest

#install crond
RUN apt-get update && apt-get -y install cron git

#copy startup script
COPY start.sh /

#modify user
RUN usermod -u 33 www-data

#start script
RUN chmod +x /start.sh

ENTRYPOINT ["/start.sh"]
