#!/bin/bash
# This script is used to run the tests in the project

# Set the pyton path
export PYTHONPATH="$(pwd)/src/"


pytest
