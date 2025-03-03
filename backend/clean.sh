#!/bin/bash

# Define the root directory (default is current directory)
ROOT_DIR="${1:-.}"

# Find and delete all __pycache__ directories
find "$ROOT_DIR" -type d -name "__pycache__" -exec rm -rf {} +

echo "Deleted all __pycache__ directories under $ROOT_DIR"

# Find and delete all .pyc files
# find "$ROOT_DIR" -type f -name "*.pyc" -exec rm -f {} +

# echo "Deleted all .pyc files under $ROOT_DIR"