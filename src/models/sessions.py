import pandas as pd
from datetime import datetime
from threading import Lock
from openai.types.chat import ChatCompletionMessageParam
from typing import Dict, List


# Define a class to store the DataFrame and the last access time
class SessionData:
    def __init__(
        self, df: pd.DataFrame, messages: List[ChatCompletionMessageParam] = []
    ):
        # The df of the excel data that was uploaded
        self.df = df

        # The message history between the user and llm
        self.messages = messages

        # The last time the session was accessed
        self.last_accessed = datetime.now()


# Thread safe sessions with a basic in memory implementation
class Sessions:
    def __init__(self):
        self._sessions: Dict[str, SessionData] = {}
        self._lock = Lock()

    def get(self, key, default=None):
        with self._lock:
            return self._sessions.get(key, default)

    def set(self, key, value):
        with self._lock:
            self._sessions[key] = value

    def clear(self):
        with self._lock:
            self._sessions.clear()

    def remove(self, key):
        with self._lock:
            if key in self._sessions:
                del self._sessions[key]
