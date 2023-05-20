#!/bin/bash

# Activate the virtual environment
cd /home/mararkarp/projects/crypto_newsletter
source env/bin/activate

# Run the script
python crypto_hermes.py

# Deactivate venv
deactivate