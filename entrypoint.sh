#!/bin/bash

# Set the pyton path
export PYTHONPATH="$(pwd)/src/"

# Run the app
uvicorn src.app:app --proxy-headers --reload --host 0.0.0.0 --port 8080
