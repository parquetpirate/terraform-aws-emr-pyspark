# EMR Bootstrap Script — Python environment setup

# Download Miniconda
wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh \
    && /bin/bash ~/miniconda.sh -b -p $HOME/conda

# Add Miniconda to PATH
echo -e '\nexport PATH=$HOME/conda/bin:$PATH' >> $HOME/.bashrc && source $HOME/.bashrc

# Install packages via conda
conda install -y boto3 pendulum numpy scikit-learn

# Install packages via pip
pip install --upgrade pip
pip install findspark
pip install boto3
pip install numpy
pip install python-dotenv
pip install scikit-learn

# Create required directories
mkdir -p $HOME/pipeline
mkdir -p $HOME/logs
