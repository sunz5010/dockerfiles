#notice file will put in /www
#GIT_PULL_FOLDER only need set to project name ex.myWebsite
#SSH_IDENTITYFILE_PATH need set to full path

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
	sudo cat > /root/.ssh/config <<EOL
Host git-codecommit.us-east-1.amazonaws.com
  StrictHostKeyChecking no
  User ${SSH_USER}
  Port 22
  IdentityFile ${SSH_IDENTITYFILE_PATH}
EOL
fi

#check this folder is git pull or not
if [ ! -d "/www/${GIT_PULL_FOLDER}/.git" ]; then
    echo "folder is not git pull yet, start git clone."
    rm -rf /www/${GIT_PULL_FOLDER}

    cd /www
    sudo chmod 400 ${SSH_IDENTITYFILE_PATH}
    sudo git clone ${GIT_PULL_REPO}
fi
