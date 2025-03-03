from fastapi import APIRouter, Request
from fastapi.encoders import jsonable_encoder
from typing import Union
from datetime import datetime
from pydantic import BaseModel
import json


#:custom import
from utils.resp_wrapper import auto_response
from utils.task import Task
from tools.datetime_tools import DateTimeTools
from utils.pydan_master import DefaultPayload


router = APIRouter(prefix="/TSK100")

@router.post("/TSK100")
@auto_response
async def TSK100(request: Request):
    send_data : dict = {}
    task : Task = None
    payload : dict = None
    curr_task_id : int = 0
    task_list : list = []

    try:
        data = await request.json()
        print(f">> data -> {data}")

        # task = Task()
        # status, body = task.get_tasks()

        if not isinstance(data, dict):
            payload = json.loads(data)
        else:
            payload = data

        payload_data = DefaultPayload(**payload)

        # print(f">> status -> {status}")
        # print(f">> body -> {body}")
        # if not status:
        #     raise Exception(101, "Failed to get task details.", body)

    except Exception as e:
        print(e)
        raise Exception(101, "Invalid Payload", str(e))

    else:
        try:
            task = Task()
            
            
            status, body = task.get_tasks(payload_data.task_id)
            if not status:
                raise Exception(102, "Failed to get task details.", body)


            datetool = DateTimeTools()
            #: loop through each record and generate the response
            for each_record in body:
                
                assassignment_date_temp = datetool.convert_to_def(each_record["assignment_date"])
                creation_date_temp = datetool.convert_to_def(each_record["creation_date"])
                deadline_temp = datetool.convert_to_def(each_record["deadline"])
                sub_deadline_temp = datetool.convert_to_def(each_record["sub_deadline"])
                sub_assignment_date_temp = datetool.convert_to_def(each_record["sub_assignment_date"])
                sub_creation_date_temp = datetool.convert_to_def(each_record["sub_creation_date"])

                if curr_task_id != each_record["task_id"]:
                    task_list.append(
                        {
                            "task_id": each_record["task_id"],
                            "parent_task_id": each_record["parent_task_id"] if each_record["parent_task_id"] else "",
                            "task_heading": each_record["task_heading"],
                            "task": each_record["task"],
                            "assignment_date": assassignment_date_temp[1],
                            "status_id": each_record["status_id"],
                            "status": each_record["status"],
                            "deadline": deadline_temp[1],
                            "fork_task_count" : each_record["fork_number"],
                            "assigned_user_count": each_record["assigned_user_count"],
                            "max_assigned_user_count": each_record["max_assigned_user_count"],
                            "finish_flag": each_record["finish_flag"],
                            "creation_date": creation_date_temp[1],
                            "delete_flag": each_record["delete_flag"],
                            "sub_task_list": []
                        }
                    )
                    curr_task_id = each_record["task_id"]
                
                if each_record["sub_task_id"]:
                    task_list[-1]["sub_task_list"].append(
                        {
                            "sub_task_id": each_record["sub_task_id"],
                            "sub_task_heading": each_record["sub_task_heading"],
                            "sub_task": each_record["sub_task"],
                            "sub_assignment_date": sub_assignment_date_temp[1],
                            "sub_status_id": each_record["sub_status_id"],
                            "sub_status": each_record["sub_status"],
                            "sub_deadline": sub_deadline_temp[1],
                            "sub_assigned_user_count": each_record["sub_assigned_user_count"],
                            "sub_max_assigned_user_count": each_record["sub_max_assigned_user_count"],
                            "sub_finish_flag": each_record["sub_finish_flag"],
                            "sub_creation_date": sub_creation_date_temp[1],
                            "sub_delete_flag": each_record["sub_delete_flag"]
                        }
                    )
        
        except Exception as e:
            raise Exception(102, "Failed to prepare response", str(e))

        else:
            send_data.update(
                {
                    "task_list": task_list
                }
            )


    if task:
        task.__del__()

    return send_data
    