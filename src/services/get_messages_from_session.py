import pandas as pd
from openai.types.chat import ChatCompletionMessageParam
from typing import List
from services.set_session_data import set_session_data
from models import Sessions


"""_summary_
This function returns the messages associated with a session ID.
If the session ID is not found in the sessions dictionary, a 400 error is raised.
"""


def get_messages_from_session(
    session_id: str, sessions: Sessions, logger
) -> List[ChatCompletionMessageParam]:
    logger = logger.bind(func="get_messages_from_session")
    logger.info(f"Getting historical messages for session_id: {session_id}")

    session_data = sessions.get(session_id)

    if session_data is None:
        logger.warning(
            f"Session ID {session_id} not found. Returning empty list for messages."
        )
        return []

    # Update the last accessed time
    set_session_data(session_id, session_data, sessions, logger)

    messages = session_data.messages

    return messages
