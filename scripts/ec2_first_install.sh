echo "Starting installation of Python and Poetry..."

curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
sudo apt-get install unzip
unzip awscliv2.zip
sudo ./aws/install

# Update package list
sudo apt-get update -y

# Install Python 3.11 and pip
sudo apt-get install -y software-properties-common
sudo add-apt-repository -y ppa:deadsnakes/ppa
sudo apt-get update -y
sudo apt-get install -y python3.11 python3.11-venv python3.11-dev python3-pip

# Install build dependencies
sudo apt-get install -y build-essential libssl-dev libffi-dev

# Set Python 3.11 as default python3
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1

# Verify Python installation
python3 --version
pip3 --version

# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
export PATH="$HOME/.local/bin:$PATH"
echo 'export PATH="$HOME/.local/bin:$PATH"' | sudo tee -a /etc/profile

# Verify Poetry installation
poetry --version

echo "Python and Poetry installation completed successfully!"
