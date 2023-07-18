#!/bin/bash
# ctfbuddy.sh

# Move to the home directory
cd ~

# Clone the GitHub repository
git clone https://github.com/neutronsec/ctfbuddy

# Move into the cloned directory
cd ctfbuddy

# Check for Python 3 and pip3 installation
if ! command -v python3 &> /dev/null
then
    echo "Python3 could not be found. Installing now..."
    sudo apt-get install -y python3
fi

if ! command -v pip3 &> /dev/null
then
    echo "pip3 could not be found. Installing now..."
    sudo apt-get install -y python3-pip
fi

# Check for venv module in Python3
python3 -c "help('modules venv')" > /dev/null
if [ $? -ne 0 ]; then
    echo "Python3 venv module not found. Installing python3-venv now..."
    sudo apt-get install -y python3-venv
fi

# Create a Python virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install required Python libraries
pip3 install python-nmap

# Make the script executable
chmod +x buddy.py

# Add an alias to .bashrc or .zshrc for the `ctfbuddy` command
if [[ "$SHELL" == *"zsh"* ]]; then
    echo "alias ctfbuddy='`pwd`/buddy.py'" >> ~/.zshrc
    source ~/.zshrc
else
    echo "alias ctfbuddy='`pwd`/buddy.py'" >> ~/.bashrc
    source ~/.bashrc
fi

# Deactivate the virtual environment
deactivate

echo "CTFBuddy is set up! You can now use it by typing 'ctfbuddy' in the terminal."
