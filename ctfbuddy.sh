#!/bin/bash

# Checking if directory exists
if [ -d "$HOME/ctfbuddy" ]; then
    echo "💼 ctfbuddy directory already exists."
    while true; do
        read -p "Do you want to remove the old directory and make a fresh installation? [y/n]: " yn
        case $yn in
            [Yy]* ) rm -rf $HOME/ctfbuddy; break;;
            [Nn]* ) echo "Aborting installation."; exit;;
            * ) echo "Please answer yes or no.";;
        esac
    done
fi

echo "📥 Cloning the CTF Buddy repository..."
git clone https://github.com/neutronsec/ctfbuddy.git $HOME/ctfbuddy

cd $HOME/ctfbuddy

echo "🔧 Updating and upgrading the system..."
sudo apt-get update
sudo apt-get upgrade -y

echo "🔨 Installing necessary tools..."
sudo apt-get install -y samba-common-bin smbclient smbmap enum4linux crackmapexec evil-winrm sqlmap python3-dev

echo "🐍 Creating a Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "📦 Installing required Python packages..."
pip install -r requirements.txt

# Check if ctfbuddy already exists in /usr/local/bin
if [ -L "/usr/local/bin/ctfbuddy" ]; then
    echo "🔄 ctfbuddy file already exists in /usr/local/bin. Removing for fresh installation..."
    sudo rm /usr/local/bin/ctfbuddy
fi

echo "🔗 Creating a symlink to /usr/local/bin..."
sudo ln -s "$(pwd)/buddy.py" /usr/local/bin/ctfbuddy
sudo chmod +x /usr/local/bin/ctfbuddy

echo "🎉 Installation complete. You can run the script using the command 'ctfbuddy'."
