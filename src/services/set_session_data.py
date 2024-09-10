from datetime import datetime
from models import Sessions, SessionData


"""_summary_
Updates the session_data on sessions with the data provided.
This also updates the last_accessed field of the session_data.
"""


def set_session_data(
    session_id: str,
    session_data: SessionData,
    sessions: Sessions,
    logger,
) -> SessionData:
    logger = logger.bind(func="set_session_data")

    logger.info(f"Setting session data for session_id: {session_id}")

    session_data.last_accessed = datetime.now()
    sessions.set(session_id, session_data)

    return session_data
