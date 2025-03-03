 #~ 

from fastapi import APIRouter, Request
from fastapi.encoders import jsonable_encoder
from typing import Union
from datetime import datetime
from pydantic import BaseModel
import json


#:custom import
from utils.resp_wrapper import auto_response
from utils.task import Task
# from tools.datetime_tools import DateTimeTools


router = APIRouter(prefix="/TSK1")

@router.post("/TSK1")
@auto_response
async def TSK1(request: Request):
    send_data : dict = {}
    payload : dict = None
    task : Task = None

    try:
        data = await request.json()
        
        if not isinstance(data, dict):
            payload = json.loads(data)
        else:
            payload = data

        # payload_data = TaskInsertUpdate(**payload)

    except Exception as e:
        print(e)
        raise Exception(101, "Invalid payload", str(e))

    else:
        pass
    
    if task:
        task.__del__()

    return send_data
    