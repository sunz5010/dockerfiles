#!/bin/bash

#notice file will put in /www
#GIT_PULL_FOLDER only need set to project name ex.myWebsite
#SSH_IDENTITYFILE_PATH need set to full path

#you need following env
# export GIT_PULL_FOLDER=mysite
# export GIT_PULL_REPO=ssh://git-codecommit.us-east-1.amazonaws.com/v1/repos/mysite
# export SSH_HOST=git-codecommit.us-east-1.amazonaws.com
# export SSH_USER=myuser
# export SSH_IDENTITYFILE_PATH=/id_rsa

sudo mkdir /www

#check variavble
if [[ -z "${GIT_PULL_FOLDER}" ]]; then
	echo "GIT_PULL_FOLDER is unset"
	exit 0
else
	echo "GIT_PULL_FOLDER = ${GIT_PULL_FOLDER}"
fi

if [[ -z "${GIT_PULL_REPO}" ]]; then
	echo "GIT_PULL_REPO is unset"
	exit 0
else
	echo "GIT_PULL_REPO = ${GIT_PULL_REPO}"
fi

if [[ -z "${SSH_HOST}" ]]; then
	echo "SSH_HOST is unset"
	exit 0
else
	echo "SSH_HOST=${SSH_HOST}"
fi

if [[ -z "${SSH_USER}" ]]; then
	echo "SSH_USER is unset"
	exit 0
else
	echo "SSH_USER = ${SSH_USER}"
fi

if [[ -z "${SSH_IDENTITYFILE_PATH}" ]]; then
	echo "SSH_IDENTITYFILE_PATH is unset"
	exit 0
else
	echo "SSH_IDENTITYFILE_PATH = ${SSH_IDENTITYFILE_PATH}"
fi

#check ssh identity file exists
if [ ! -f "${SSH_IDENTITYFILE_PATH}" ]; then
	echo "ssh identity file if not exists."
	exit 0
fi

#check ~/.ssh/config file exists
if [ ! -f /root/.ssh/config ]; then
	echo "ssh config file if not exists. creating..."
	mkdir /root/.ssh/
	cat > /root/.ssh/config <<EOL
Host git-codecommit.us-east-1.amazonaws.com
  StrictHostKeyChecking no
  User ${SSH_USER}
  Port 22
  IdentityFile ${SSH_IDENTITYFILE_PATH}
EOL
fi

#check git_pull.sh file exists
if [ ! -f /git_pull.sh ]; then
	echo "git_pull.sh file if not exists. creating..."
	cat > /git_pull.sh <<EOL
#!/bin/bash
cd /www/${GIT_PULL_FOLDER}
git pull
EOL
	chmod +x /git_pull.sh
fi

#check this folder is git pull or not
if [ ! -d "/www/${GIT_PULL_FOLDER}/.git" ]; then
    echo "folder is not git pull yet, start git clone."
    rm -rf /www/${GIT_PULL_FOLDER}

    cd /www
    chmod 400 ${SSH_IDENTITYFILE_PATH}
    git clone --depth=1 ${GIT_PULL_REPO}
    
    #change owner
    chown www-data: -R /www
fi

#add crontab
echo "*/1 * * * * root /git_pull.sh > /tmp/git_pull.log" > /etc/cron.d/mycron
chmod 0644 /etc/cron.d/mycron

#start crond
touch /var/log/cron.log
cron && tail -f /var/log/cron.log
