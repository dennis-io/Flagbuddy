#!/bin/bash
# Clone the project if it doesn't already exist
if [ ! -d "ctfbuddy" ]; then
  git clone https://github.com/neutronsec/ctfbuddy.git
  echo "Cloned the CTFBuddy repository."
else
  cd ctfbuddy
  git reset --hard
  git pull
  echo "Updated the CTFBuddy repository."
  cd ..
fi

# Create a virtual environment and activate it
python3 -m venv ctfbuddy/venv
source ctfbuddy/venv/bin/activate

# Install the Python dependencies
pip install -r ctfbuddy/requirements.txt

# Link the CTFBuddy script to /usr/local/bin for global usage
ln -sf $(pwd)/ctfbuddy/buddy.py /usr/local/bin/ctfbuddy
chmod +x /usr/local/bin/ctfbuddy

echo "CTFBuddy has been installed! You can run it with the 'ctfbuddy' command."
