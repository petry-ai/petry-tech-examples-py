import pandas as pd
from fastapi import Request
from io import BytesIO
from pydantic import BaseModel
from fastapi import File, UploadFile, HTTPException, APIRouter, Depends
from fastapi.responses import JSONResponse
from models.sessions import SessionData
from utils import get_app_sessions, create_session_id
from errors import InvalidFileFormatError

upload_router = APIRouter(
    prefix="/upload",
    tags=["upload"],
    responses={404: {"description": "Not found"}},
)


@upload_router.post("/excel-file")
async def upload_excel(
    request: Request, file: UploadFile = File(...), sessions=Depends(get_app_sessions)
) -> JSONResponse:
    logger = request.state.logger
    logger = logger.bind(route="/excel-file")

    try:
        logger.info(f"Uploading excel file")
        if not file.filename.endswith((".xls", ".xlsx")):
            raise InvalidFileFormatError("excel file")

        # Read the contents of the uploaded file
        contents = await file.read()

        # Read the Excel file into a DataFrame
        df = pd.read_excel(BytesIO(contents))

        # Generate a new session ID
        session_id = create_session_id()

        # Store the DataFrame in the sessions dictionary
        sessions.set(session_id, SessionData(df))

        logger.info(f"File uploaded successfully for session ID: {session_id}")

        return JSONResponse(
            content={"message": "File uploaded successfully", "session_id": session_id},
            status_code=200,
            headers={"petry-session-id": session_id},
        )
    except Exception as e:
        logger.error(f"Error uploading excel file: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Could not upload file: {str(e)}")
