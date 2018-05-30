FROM ubuntu:latest

#install crond
RUN apt-get update && apt-get -y install cron

# Add crontab file in the cron directory
ADD crontab /etc/cron.d/mycron

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/mycron

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

#copy startup script
COPY start.sh /

ENTRYPOINT ["/start.sh"]
