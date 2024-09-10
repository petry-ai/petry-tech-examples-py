import pandas as pd
from fastapi import File, UploadFile, HTTPException


"""_summary_
This function reads an uploaded Excel file and returns a DataFrame.
"""


async def read_uploaded_excel_file(
    file: UploadFile = File(...), logger=None
) -> pd.DataFrame:
    logger = logger.bind(func="read_uploaded_excel_file")

    try:
        logger.info(f"Reading uploaded excel file")
        contents = await file.read()
        df = pd.read_excel(contents)

        logger.info(f"Excel file read successfully")
        return df

    except Exception as e:
        logger.error(f"Could not read excel file: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Could not read excel file")
