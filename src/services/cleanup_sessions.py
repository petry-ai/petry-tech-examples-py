from fastapi import FastAPI
from datetime import datetime, timedelta

# Session expiration time (in minutes)
SESSION_EXPIRATION = 15


"""_summary_
This function removes expired sessions from the sessions dictionary.
"""


def cleanup_sessions(app: FastAPI, logger):
    logger = logger.bind(func="cleanup_sessions")
    logger.info("Cleaning up expired sessions...")
    # Get the current time
    current_time = datetime.now()
    sessions = app.state.sessions.get()

    # Find all session IDs that have expired
    expired_sessions = [
        session_id
        for session_id, session_data in sessions.items()
        if current_time - session_data.last_accessed
        > timedelta(minutes=SESSION_EXPIRATION)
    ]
    for session_id in expired_sessions:
        app.state.sessions.remove(session_id)

    logger.info("Expired sessions cleaned up.")
