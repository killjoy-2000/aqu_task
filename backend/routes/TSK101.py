 #~ Create a new task/ Create a fork of existing task/ Edit existing task

from fastapi import APIRouter, Request
from fastapi.encoders import jsonable_encoder
from typing import Union
from datetime import datetime
from pydantic import BaseModel, Field, field_validator, ConfigDict
import json


#:custom import
from utils.resp_wrapper import auto_response
from utils.task import Task
from utils.pydan_master import TaskInsertUpdate, SubTaskData
# from tools.datetime_tools import DateTimeTools


router = APIRouter(prefix="/TSK101")

@router.post("/TSK101")
@auto_response
async def TSK101(request: Request):
    send_data : dict = {}
    task : Task = None
    payload : dict = None

    try:
        data = await request.json()
        
        if not isinstance(data, dict):
            payload = json.loads(data)
        else:
            payload = data

        payload_data = TaskInsertUpdate(**payload)
        
    except Exception as e:
        print(e)
        raise Exception(101, "Invalid payload", str(e))

    else:
        try:
            task = Task()

            task_id = payload_data.task_id
            parent_task_id = payload_data.parent_task_id
            task_body = payload_data.task
            print(f">> task body -> {task_body}")
            
            if (task_id is None or task_id == "") and (parent_task_id is None or parent_task_id == ""):
                status, body = task.insert_task_subtask(payload_data)

                if not status:
                    raise Exception(body)
            
            elif (task_id is not None and task_id != "") and (parent_task_id is None or parent_task_id == ""):
                status, body = task.update_task_subtask(payload_data)

                if not status:
                    raise Exception(body)
            
            elif (task_id is None or task_id == "") and (parent_task_id is not None and parent_task_id != ""):
                status, body = task.create_fork_task(payload_data)

                if not status:
                    raise Exception(f"Fork rask error -> {body}")

        except Exception as e:
            print(f">> top level error -> {e}")
            raise Exception(102, "Failed to create task", str(e))
        
        else:
            if task is not None:
                task.commit_transactions()

    if task:
        task.__del__()

    return send_data
    