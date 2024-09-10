from services import cleanup_sessions
from fastapi import FastAPI
import asyncio


"""_summary_
This function periodically cleans up expired sessions.
"""


async def periodic_cleanup(app: FastAPI, logger):
    while True:
        await asyncio.sleep(300)  # Sleep for 5 minutes
        cleanup_sessions(app, logger)
