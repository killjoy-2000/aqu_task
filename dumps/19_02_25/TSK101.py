from fastapi import APIRouter, Request
from typing import Union
from pydantic import BaseModel
import json

router = APIRouter(prefix="/TSK101")

class Request_data(BaseModel):
    signature: dict
    payload: dict


class Response_data(BaseModel):
    status: bool
    body: Union[str, list, dict]


@router.post("/TSK101")
async def TSK101(request: Request):
    data = await request.json()
    print(data)
    
    return True