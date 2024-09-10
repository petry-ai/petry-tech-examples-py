import os
import pandas as pd
from pydantic import BaseModel
from typing import Optional
from services.get_df_from_session import get_df_from_session
from models import Sessions


"""_summary_
This function returns the DataFrame associated with a session ID or from a local file.
 """


class GetDfFromFileOrSessionParams(BaseModel):
    file_path: Optional[str]
    session_id: Optional[str]


def get_df_from_file_or_session(
    params: GetDfFromFileOrSessionParams, sessions: Sessions, logger=None
) -> pd.DataFrame:
    logger = logger.bind(func="get_df_from_file_or_session")
    logger.info("Getting DataFrame from file or session")

    file_path = params.get("file_path", None)
    session_id = params.get("session_id", None)

    if file_path:
        logger.info(f"Reading DataFrame from file: {file_path}")
        if not os.path.exists(file_path):
            raise ValueError(f"File not found: {file_path}")
        return pd.read_excel(file_path)
    elif session_id:
        df = get_df_from_session(session_id, sessions, logger)

        return df
    else:
        raise ValueError("Either file_path or session_data must be provided")
