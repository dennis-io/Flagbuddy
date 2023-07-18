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

# Check if the ctfbuddy folder exists
if [ -d "ctfbuddy" ] ; then
    echo "ctfbuddy exists, updating now..."
    cd ctfbuddy
    git checkout . && git pull
else
    echo "ctfbuddy does not exist, cloning now..."
    git clone https://github.com/neutronsec/ctfbuddy.git
    cd ctfbuddy
fi

# Create and activate virtual environment
python3 -m venv env
source env/bin/activate

# Install requirements
pip3 install -r requirements.txt

# Make the Python script executable
chmod +x buddy.py

# Create an alias
echo "alias ctfbuddy='$(pwd)/buddy.py'" >> ~/.bashrc
source ~/.bashrc

# Deactivate the virtual environment
deactivate

# Inform the user that they should restart their shell
echo "Installation complete. Please restart your shell or run 'source ~/.bashrc'."
