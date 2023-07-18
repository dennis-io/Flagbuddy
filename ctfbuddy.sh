#!/bin/bash
# ctfbuddy.sh

# Get current working directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Check if required tools are installed and install them if not
for tool in git python3 pip curl; do
    command -v $tool >/dev/null 2>&1 || { echo >&2 "$tool is required but it's not installed. Installing now..."; sudo apt-get install -y $tool; }
done

# Clone the repository
git clone https://github.com/neutronsec/ctfbuddy.git

# Go to the cloned repository directory
cd ctfbuddy

# Create a python virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install Python dependencies (replace 'requirements.txt' with actual filename if different)
pip install -r requirements.txt

# Create a bash script to make the python script globally runnable
echo "#!/bin/bash
source $SCRIPT_DIR/ctfbuddy/venv/bin/activate
python3 $SCRIPT_DIR/ctfbuddy/buddy.py" > ctfbuddy.sh

# Move the bash script to /usr/local/bin/ and make it executable
sudo cp ctfbuddy.sh /usr/local/bin/ctfbuddy
sudo chmod +x /usr/local/bin/ctfbuddy

# Install system-wide dependencies
sudo apt-get update
sudo apt-get install -y nmap hydra

# Let the user know that the setup has finished
echo "ctfbuddy setup completed. You can now run 'ctfbuddy' from anywhere."
