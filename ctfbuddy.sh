#!/bin/bash

# Check if Git is installed
if ! command -v git >/dev/null 2>&1; then
    echo "Git is not installed, installing now..."
    sudo apt-get install git
else
    echo "Git is installed, moving on..."
fi

# Check if Python3 is installed
if ! command -v python3 >/dev/null 2>&1; then
    echo "Python3 is not installed, installing now..."
    sudo apt-get install python3
else
    echo "Python3 is installed, moving on..."
fi

# Check if pip is installed
if ! command -v pip3 >/dev/null 2>&1; then
    echo "pip3 is not installed, installing now..."
    sudo apt-get install python3-pip
else
    echo "pip3 is installed, moving on..."
fi

# Check if virtualenv is installed
if ! command -v virtualenv >/dev/null 2>&1; then
    echo "virtualenv is not installed, installing now..."
    sudo pip3 install virtualenv
else
    echo "virtualenv is installed, moving on..."
fi

# Check if the ctfbuddy directory exists
if [ -d "ctfbuddy" ]; then
    echo "ctfbuddy directory exists, pulling latest changes..."
    cd ctfbuddy && git pull origin main
else
    echo "Cloning ctfbuddy repository..."
    git clone https://github.com/neutronsec/ctfbuddy.git
    cd ctfbuddy
fi

# Create a Python virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install required Python libraries
pip3 install python-nmap

# Deactivate the virtual environment
deactivate

# Add execution permission to the buddy.py script
chmod +x buddy.py

# Create a symbolic link to run the buddy.py from anywhere
if [ -L "/usr/local/bin/ctfbuddy" ]; then
    echo "Symbolic link already exists..."
else
    echo "Creating symbolic link..."
    sudo ln -s "$(pwd)/buddy.py" /usr/local/bin/ctfbuddy
fi

# Print success message
echo "Setup completed. You can now use 'ctfbuddy' to run the script."
