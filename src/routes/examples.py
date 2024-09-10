from pydantic import BaseModel
from fastapi.responses import JSONResponse
from openai.types.chat import ChatCompletionMessageParam
from typing import List, Optional
from fastapi import HTTPException, APIRouter, Depends, Request
from examples import query_excel_using_llm
from utils import get_app_sessions


examples_router = APIRouter(
    prefix="/examples",
    tags=["examples"],
    responses={404: {"description": "Not found"}},
)


class QueryExcelFileUsingLlmParams(BaseModel):
    question: str


@examples_router.post("/query-excel-using-llm")
async def ask_question(
    request: Request,
    params: QueryExcelFileUsingLlmParams,
    sessions=Depends(get_app_sessions),
):
    logger = request.state.logger
    logger = logger.bind(route="/query-excel-using-llm")

    req_params = params.model_dump()
    question = req_params.get("question")
    session_id = request.state.session_id

    if not session_id:
        raise HTTPException(status_code=401, detail="Unauthorized")

    params = {"question": question, "session_id": session_id}

    try:
        answer = await query_excel_using_llm(params, sessions, logger)

        return JSONResponse(
            content={"answer": answer},
            status_code=200,
        )
    except Exception as e:
        logger.error(f"Error querying excel using llm: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error querying excel using llm")
