#Copy from phalcon
#reference: https://github.com/phalcon/dockerfiles/blob/master/nginx/Dockerfile

# Pull base image
FROM ubuntu:latest

# Adding repositories
RUN apt update && \
    apt install -y nginx && \


# Cleanup package manager
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Add files
RUN mkdir /etc/nginx/global && \
    mkdir /etc/nginx/certs

# Apply Nginx configuration
ADD conf/restrict.conf /etc/nginx/global/restrict.conf

RUN usermod -u 1000 www-data

RUN chown -R www-data:www-data /var/lib/nginx && \
    rm -rf /etc/nginx/sites-enabled/*

# Forward request and error logs to docker log collector
RUN ln -sf /dev/stdout /var/log/nginx/access.log && \
    ln -sf /dev/stderr /var/log/nginx/error.log

# Expose ports
EXPOSE 80

# Define default command
CMD ["nginx", "-g", "daemon off;"]
