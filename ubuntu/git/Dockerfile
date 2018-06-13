FROM ubuntu:latest

#install crond
RUN apt-get update && apt-get -y install cron git

#copy startup script
COPY start.sh /
RUN chmod +x /start.sh

RUN usermod -u 33 www-data

ENTRYPOINT ["/start.sh"]
