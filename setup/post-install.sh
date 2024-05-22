#!/usr/bin/env bash
set -x

#############
# Variables #
#############
username=$USER
devtools=false
ovpn='physical-twin.ovpn' # OpenVPN conf file, assumed to be in same directory

#############################
# Install Required Software #
#############################
# Things to be installed:
# unattended-upgrades - for automatic security updates
# docker - dw-pong is containerized
# nvidia-container-toolkit - give access to the GPU
# ubuntu-desktop - GUI for pong
# RealSense SDK - For camera support

# Download package information 
sudo apt-get update

# Install additional software we need
sudo apt-get install -y \
	chromium-broswer \  # Chrome is easier to move around the screen than firefox
	xdotool \           # Used for moving widnows, emulating keypresses
	openvpn \           # allowing remote-in
	unattended-upgrades # automatic security updates

# Install optional development tools
if $devtools ; then
	sudo apt-get install -y \
		neovim \
		inotify-tools
fi

# Enable unattended-upgrades
sudo unattended-upgrades -d

# Docker
for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do sudo apt-get remove $pkg; done
sudo snap remove docker

# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo usermod -aG docker dwpong

# Add Nvidia container toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | \
	sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
	&& curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
	sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
	sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker

# Do the desktop seperate, we don't want all the extras and it's a big install
sudo apt-get install -y \
	--no-install-recommends ubuntu-desktop

# Install Realsense Builder
sudo mkdir /opt/realsense
sudo chown dwpong:dwpong realsense/
cd realsense/
git clone https://github.com/IntelRealSense/librealsense.git
cd librealsense/
sudo ./scripts/setup_udev_rules.sh
sudo apt install libdpkg-perl=1.21.1ubuntu2.1 libusb-1.0-0=2:1.0.25-1ubuntu1
sudo ./scripts/patch-realsense-ubuntu-lts-hwe.sh
cd ~

#######################
# Remote Access Setup #
#######################
autostart="AUTOSTART=\"$ovpn\""

sudo mv $ovpn /etc/openvpn/$ovpn.conf

if [ $(grep -o $autostart /etc/default/openvpn | wc -l) -lt 1 ]; then
	echo $autostart | sudo tee -a /etc/default/openvpn
fi
sudo systemctl daemon-reload
sudo systemctl enable openvpn
sudo systemctl start openvpn

########################
# Source Code Download #
########################
# Check if we need to generate a new key
if [ ! -f ~/.ssh/dw_deploy.pub ]; then
	# Generate deploy key
	ssh-keygen \
		-N '' \
		-a 128 \
		-C 'Discovery World Pong GitHub Deploy Key' \
		-f ~/.ssh/dw_deploy \
		-t ed25519
fi
echo '```'
cat ~/.ssh/dw_deploy.pub
echo '```'

echo "Please enter the above-printed key into the git repository as a deploy key. Once complete hit enter to continue"
read

# Configure git
git config --global core.sshCommand "ssh -i ~/.ssh/dw_deploy"
git config --global init.defaultBranch main
ssh-keyscan -H github.com >> ~/.ssh/known_hosts

# Create space for repo
sudo mkdir /opt/pong
sudo chown $USER:$USER /opt/pong 
cd /opt/pong

# avoid nested dirs
# https://stackoverflow.com/a/16900010
git init
git remote add origin git@github.com:Rockwell-Automation-Inc/Discovery-World-Pong.git
git fetch origin
git checkout -b main --track origin/main # origin/master is clone's default

# Add Firefox profiles to use in open_windows.sh
/opt/pong/setup/create_profiles.sh 

# Setup auto-start functionality
sudo cp /opt/setup/pong.service /etc/systemd/system/pong.service
sudo systemctl daemon-reload
sudo systemctl enable my-custom-script.service

# Automatic System Restart
config_file='/etc/apt/apt.conf.d/50unattended-upgrades'

config_line='Unattended-Upgrade::Automatic-Reboot '
sudo grep -q "^$config_line" $config_file; greprc=$?
if [[ $greprc -eq 1 ]]; then
	echo "Appending Automatic reboot option to $config_file"
	echo 'Unattended-Upgrade::Automatic-Reboot "true";' | sudo tee -a $config_file
else
	echo "Automatic reboot already configured. Not touching that configuration"
fi

config_line='Unattended-Upgrade::Automatic-Reboot-WithUsers '
sudo grep -q "^$config_line" $config_file; greprc=$?
if [[ $greprc -eq 1 ]]; then
	echo "Appending Automatic Reboot With Users option to $config_file"
	echo 'Unattended-Upgrade::Automatic-Reboot-WithUsers "true";' | sudo tee -a $config_file
else
	echo "Automatic reboot with users already configured. Not touching that configuration"
fi

config_line='Unattended-Upgrade::Automatic-Reboot-Time '
sudo grep -q "^$config_line" $config_file; greprc=$?
if [[ $greprc -eq 1 ]]; then
	echo "Appending Automatic Reboot time option to $config_file"
	# UTC - 9pm local (central US) time
	echo 'Unattended-Upgrade::Automatic-Reboot-Time "02:00";' | sudo tee -a $config_file
else
	echo "Automatic reboot time already configured. Not touching that configuration"
fi


########
# TODO #
#######
# Auto-login
# /etc/gdm/custom.conf

# Package update check setup frequency


# Auto-sleep
# /home/dwpong/.config/dconf/user

# 
