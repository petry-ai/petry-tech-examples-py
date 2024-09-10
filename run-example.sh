#!/bin/bash
# This script is used to run the examples in the project
# This works on UNIX based systems (Mac, Linux)

# Set the pyton path
export PYTHONPATH="$(pwd)/src/"

# Run the specific example
# Change this to the example you want to run
python ./src/examples/query_excel_using_llm/run_example.py
