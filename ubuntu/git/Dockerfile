FROM ubuntu:latest

#install crond
RUN apt-get update && apt-get -y install cron

#copy startup script
COPY ./start.sh /

ENTRYPOINT ["/start.sh"]
