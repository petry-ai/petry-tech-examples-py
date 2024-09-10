@echo off
REM This script is used to run the examples in the project
REM This works on Windows systems

REM Set the Python path
set PYTHONPATH=%cd%\src\

REM Run the specific example
REM Change this to the example you want to run
python .\src\examples\query_excel_using_llm\run_example.py
