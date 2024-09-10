import os
from openai import OpenAI
from typing import Dict, Optional
from pydantic import BaseModel
from fastapi import HTTPException
from dotenv import load_dotenv
from services.get_df_from_file_or_session import get_df_from_file_or_session
from services.set_session_data import set_session_data
from services.get_messages_from_session import get_messages_from_session


# Load environment variables
load_dotenv()


class QueryExcelUsingLlmParams(BaseModel):
    question: str
    file_path: Optional[str]
    session_id: Optional[str]


"""_summary_
This function queries the LLM with a question and the Excel data provided by the user.

@param params: A dictionary containing the question, file path (optional), and session ID (optional).
@param sessions: A dictionary containing the session IDs and associated DataFrames. Ignore this if running this script locally. This is only needed for the FastAPI implementation.
"""


async def query_excel_using_llm(
    params: QueryExcelUsingLlmParams, sessions: Optional[Dict] = {}, logger=None
) -> str:
    logger = logger.bind(func="query_excel_using_llm")
    logger.info(f"Querying excel using llm")

    # Initialize the OpenAI client
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    # Extract the parameters
    question = params.get("question")
    file_path = params.get("file_path", None)
    session_id = params.get("session_id", None)

    # Get the historical messages from the session if applicable
    messages = get_messages_from_session(
        session_id=session_id, sessions=sessions, logger=logger
    )

    # Get the DataFrame from the file or session
    df = get_df_from_file_or_session(
        params={"file_path": file_path, "session_id": session_id},
        sessions=sessions,
        logger=logger,
    )

    # Check if the DataFrame is empty
    if df is None:
        raise HTTPException(
            status_code=400,
            detail="No data found for the given session ID or file path",
        )

    # Setup the system content for the LLM. You can think of this as defining its role/character
    system_content = """
    You are a helpful assistant that answers questions about Excel data that the user provides.

    Rules:
    - Do not provide any information that is not present in the Excel data.
    - Do not make any assumptions about the data.
    - Do not provide any information that is not explicitly asked for.
    - Do not provide any information that is not directly supported by the data.
    - Do not use any profanity or offensive language.
    """

    # Convert the DataFrame to a string so we can include it in the prompt
    df_string = df.to_string()

    # Create the user prompt for the LLM
    # We provide the LLM with the Excel data and the question to answer
    initial_user_prompt = f"""
    Given the following Excel data: {df_string}

    Here is the question I would like answered: {question} based on the data provided.

    Please provide the answer in a text format.
    """

    # Add the system content and user prompt to the messages
    # Include any previous messages if they exist
    if len(messages) > 0:
        chat = messages + [{"role": "user", "content": question}]
    else:
        chat = [
            {"role": "system", "content": system_content},
            {"role": "user", "content": initial_user_prompt},
        ]

    # Update the session data with the latest chat messages
    if session_id:
        session_data = sessions.get(session_id)

        session_data.messages = chat

        set_session_data(session_id, session_data, sessions, logger)

    try:
        logger.info(f"Querying LLM with the following question: {question}")

        # Query the LLM with the prompt
        response = client.chat.completions.create(model="gpt-3.5-turbo", messages=chat)

        answer = response.choices[0].message.content.strip()

        logger.info(f"LLM response: {answer}")
        return answer
    except Exception as e:
        logger.error(f"Error querying excel using llm: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error querying excel using llm! {str(e)}"
        )
