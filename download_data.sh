#!/bin/bash

echo "Starting dataset download using kagglehub..."

python3 - <<EOF
import kagglehub
import shutil
import os

# Download dataset
path = kagglehub.dataset_download("kaushalnandania/credit-card-fraud-detection")

print("Downloaded to:", path)

# Create project data folder
os.makedirs("data/raw", exist_ok=True)

# Copy files into project structure
for file in os.listdir(path):
    shutil.copy(os.path.join(path, file), "data/raw")

print("Dataset copied to data/raw/")
EOF

echo "Download complete."
