import os
import asyncio
from app import logger
from examples.query_excel_using_llm.query_excel_using_llm import query_excel_using_llm


# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the full path to the Excel file
# Change this to the full path of your Excel file
excel_file = os.path.join(current_dir, "example_data.xlsx")

params = {
    "question": "What is being showing in the excel sheet I gave you?",  # Change this to your question
    "file_path": excel_file,
}


async def main():
    # Run the example
    answer = await query_excel_using_llm(params=params, sessions={}, logger=logger)
    logger.info(f"Answer: {answer}")


if __name__ == "__main__":
    # Run the example
    asyncio.run(main())
