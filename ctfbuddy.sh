#!/bin/bash

# Checking if directory exists
if [ -d "ctfbuddy" ]; then
    echo "💼 ctfbuddy directory already exists. Removing for fresh installation..."
    rm -rf ctfbuddy
fi

echo "📥 Cloning the CTF Buddy repository..."
git clone https://github.com/neutronsec/ctfbuddy.git

cd ctfbuddy

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
