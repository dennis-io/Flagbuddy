#!/bin/bash

# Cloning the repo
if [ ! -d "ctfbuddy" ]; then
    git clone https://github.com/neutronsec/ctfbuddy
else
    cd ctfbuddy
    git pull origin main
    cd ..
fi

cd ctfbuddy

# Checking if virtualenv is installed
if ! command -v virtualenv &> /dev/null
then
    echo "Virtualenv not found, installing..."
    apt-get install -y virtualenv
fi

# Create and activate a virtual environment
virtualenv venv
source venv/bin/activate

# Install the required packages
pip install -r requirements.txt

# Making the script executable and placing it in /usr/local/bin
chmod +x buddy.py
cp buddy.py /usr/local/bin/ctfbuddy
deactivate

echo "Installation complete. You can run the script using the command 'ctfbuddy'."

# Clean up
cd ..
rm -rf ctfbuddy
