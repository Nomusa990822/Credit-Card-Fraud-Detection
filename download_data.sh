#!/bin/bash

# Exit on error
set -e

echo "Starting dataset download..."

# Create data directory if it doesn't exist
mkdir -p data/raw

# Check if Kaggle CLI is installed
if ! command -v kaggle &> /dev/null
then
    echo "Kaggle CLI not found. Installing..."
    pip install kaggle
fi

# Check if kaggle.json exists
if [ ! -f "$HOME/.kaggle/kaggle.json" ]; then
    echo "ERROR: Kaggle API key not found."
    echo "Please place your kaggle.json in ~/.kaggle/"
    exit 1
fi

# Set correct permissions
chmod 600 $HOME/.kaggle/kaggle.json

# Download dataset
echo "Downloading dataset..."
kaggle datasets download -d kaushalnandania/credit-card-fraud-detection -p data/raw

# Unzip dataset
echo "Extracting files..."
unzip -o data/raw/credit-card-fraud-detection.zip -d data/raw

# Remove zip file (optional)
rm data/raw/credit-card-fraud-detection.zip

echo "Download complete. Files saved in data/raw/"
