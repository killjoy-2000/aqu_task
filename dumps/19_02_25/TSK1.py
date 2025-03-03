from fastapi import APIRouter, Request
from typing import Union
from pydantic import BaseModel
import json


#:custom import
from utils.resp_wrapper import auto_response
from utils.task import Task


router = APIRouter(prefix="/TSK1")

@router.post("/TSK1")
@auto_response
async def TSK1(request: Request):
    send_data : dict = {}

    try:
        data = await request.json()

    except Exception as e:
        print(e)
        raise Exception(100, "Error", str(e))

    
    return send_data
    