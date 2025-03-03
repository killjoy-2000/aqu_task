from pydantic import BaseModel, Field, field_validator, ConfigDict
from datetime import datetime

#: insert task payload
class TaskInsertUpdate(BaseModel):
    task_id : int | str
    parent_task_id : int | str
    task_heading : str = Field(min_length = 5)
    task : str = Field(min_length = 5)
    assignment_date : datetime
    status_id : int | str
    deadline : datetime
    assigned_user_count : int
    max_assigned_user_count : int
    delete_flag : bool
    sub_task_list : list

    model_config = ConfigDict(extra="forbid")

    @field_validator("task", "task_heading", mode="before")
    @classmethod
    def no_spaces_only(cls, value):
        if isinstance(value, str) and value.strip() == "":
            raise ValueError("Field cannot be empty or contain only spaces")
        return value

    @field_validator("task_id", "status_id", "parent_task_id",  mode="before")
    @classmethod
    def validate_task_id(cls, value):
        if isinstance(value, str) and value.strip() != "": 
            raise ValueError("Task ID cannot be string.")
        elif isinstance(value, str) and value.strip() == "":
            return value
        return value
    

#: sub task data
class SubTaskData(BaseModel):
    sub_task_id : int | str 
    sub_task_heading : str = Field(min_length = 5)
    sub_task : str = Field(min_length = 5)
    sub_assignment_date : datetime
    sub_status_id : int | str 
    sub_deadline : datetime
    sub_assigned_user_count : int
    sub_max_assigned_user_count : int
    sub_delete_flag : bool

    model_config = ConfigDict(extra="forbid")

    @field_validator("sub_task", "sub_task_heading", mode="before")
    @classmethod
    def no_spaces_only(cls, value):
        if isinstance(value, str) and value.strip() == "":
            raise ValueError("Field cannot be empty or contain only spaces")
        return value

    @field_validator("sub_task_id", "sub_status_id", mode="before")
    @classmethod
    def validate_task_id(cls, value):
        if isinstance(value, str) and value.strip() != "": 
            raise ValueError("Task ID cannot be string.")
        elif isinstance(value, str) and value.strip() == "":
            return value
        return value
    

#: only task_id payload
class DefaultPayload(BaseModel):
    task_id : int | str

    model_config = ConfigDict(extra="forbid")

    @field_validator("task_id", mode="before")
    @classmethod
    def validate_task_id(cls, value):
        if isinstance(value, str) and value.strip() != "": 
            raise ValueError("Task ID cannot be string.")
        elif isinstance(value, str) and value.strip() == "":
            return value
        return value
    

#: headers
class HeadersLogin(BaseModel):
    x_api_key : str

    # model_config = ConfigDict(extra="forbid")

#: login payload
class LoginPayload(BaseModel):
    user_name : str
    password : str 

    model_config = ConfigDict(extra="forbid")

