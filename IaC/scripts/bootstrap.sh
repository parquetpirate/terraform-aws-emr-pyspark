#!/bin/bash
set -euo pipefail
# EMR Bootstrap Script — Python environment setup

# Download Miniconda
wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh
/bin/bash ~/miniconda.sh -b -p $HOME/conda

# Add Miniconda to PATH directly
export PATH="$HOME/conda/bin:$PATH"

# Install packages via pip (absolute path for reliability)
$HOME/conda/bin/pip install --upgrade pip
$HOME/conda/bin/pip install findspark boto3 numpy pendulum python-dotenv scikit-learn

# Create required directories
mkdir -p $HOME/pipeline
mkdir -p $HOME/logs
