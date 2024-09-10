# Welcome to petry-tech 👋

Welcome to Petry!🎉 Petry sits at the intersection between Tech and and the Oil & Gas industry.
We're building the Excel Copilot for the Oil & Gas industry with AI at its core. You can learn more at https://petry.tech.

We understand that there is a lot of noise within our industry around "tech"/"ai".

This focus of this open source repo is to show case real tangible tech examples that can be used within our industry.
The code is fully open source so you can clone it and try it out for yourself.

You can also try out any of the tech examples on our site at https://petry.tech/newsletter through an interactive UI.
Each example has an associated newsletter for a detailed walk through and explanation.

If you would like to reach out or have any questions, feel free to contact info@petry.tech

## How can you access the examples

- Navigate to the examples directory under src
- Each example will have its own folder with all the code and date you might need to get started
- Refer to the run_example.py file and additional .py files to see how the example works
- Refer to the README.md for a link to the newsletter
- To run the example locally on your computer, open the run-example file and make sure the path points to the example you want to run
  - Update any of the parameters in the run_example.py file
  - If you are on Max/Linux, use the run-example.sh
  - If you are on Windows, use the run-example.bat
  - In your terminal simply run run-example.sh or run-example.bat
  - You'll see a log of everything that is happening including the output in your terminal

## Technical Requirements

- python v3.12+

## Local Setup

- Copy the contents of sample.env to .env
- Fill out the required environment variables
  - You can create a free account with OpenAI to get an api key if you don't have one
- If you would like to setup a virtual env, run `python -m venv venv`
- Install all the required packagers by running `pip install -r requirements.txt`
- You can then run the entire app by running ``./entrypoint.sh` in your terminal
  - The app has custom routes that can run all the examples through an api endpoint
  - Look at the router subdirectory to see the names of all the routes and how to access them

## Directory Structure

- errors: custom errors for the app
- examples: code for all the examples from our newsletter
- models: specific object models used in the app, like sessions
- routes: routes of the app
- services: individual pieces of business logic
- tests: tests for the app using pytest
- utils: general utilities for the app

# Important Files

- app.py: where the app is initialized and setup
- docker-build.sh: script to build a docker image locally
- entrypoint.sh: the entrypoint file used by Docker when starting a container
- run-example: script to run any of the examples under the examples directory
- run-tests.sh: script to run the app tests

## Important Closing

- We use OpenAI for the core LLM for the tech examples. It is your responsibility to not share any sensitive company data.
- We do our best to make sure the examples are technically sound but we are not responsible for how the outputs of the examples are used.
