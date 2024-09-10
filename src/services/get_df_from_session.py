import pandas as pd
from fastapi import HTTPException
from datetime import datetime
from models import Sessions
from services.set_session_data import set_session_data


"""_summary_
This function returns the DataFrame associated with a session ID.
If the session ID is not found in the sessions dictionary, a 400 error is raised.
"""


def get_df_from_session(session_id: str, sessions: Sessions, logger) -> pd.DataFrame:
    logger = logger.bind(func="get_df_from_session")
    logger.info(f"Retrieving DataFrame for session ID: {session_id}")

    session_data = sessions.get(session_id)

    if session_data is None:
        logger.error(f"Session ID {session_id} not found.")
        raise HTTPException(
            status_code=400, detail="No session with this ID has been found."
        )

    # Update the last accessed time
    set_session_data(session_id, session_data, sessions, logger)

    df = session_data.df

    return df
