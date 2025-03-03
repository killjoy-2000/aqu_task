 #~ Register

from fastapi import APIRouter, Request
from fastapi.encoders import jsonable_encoder
from typing import Union
from datetime import datetime
from pydantic import BaseModel
import json


#:custom import
from utils.resp_wrapper import auto_response
from utils.login import Login
from utils.pydan_master import LoginPayload
# from tools.datetime_tools import DateTimeTools


router = APIRouter(prefix="/LG101")

@router.post("/LG101")
@auto_response
async def LG101(request: Request):
    send_data : dict = {}
    payload : dict = None
    login : Login = None

    try:
        data = await request.json()

        if not isinstance(data, dict):
            payload = json.loads(data)
        else:
            payload = data

        payload_data = LoginPayload(**payload)

    except Exception as e:
        print(e)
        raise Exception(101, "Invalid payload", str(e))

    else:
        login = Login()
        status, body = login.register(payload_data)
        if not status:
            if body == "EXISTSUSER":
                raise Exception(501, "You have already registered", body)
            
            raise Exception(102, "Failed to complete your registration", body)

        login.commit_transactions()
        send_data = body
    
    if login:
        login.__del__()

    return send_data
    