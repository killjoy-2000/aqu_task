from utils.db_conn import DBConn
from utils.pydan_master import SubTaskData

class Task:
    db = None
    db_conn = None


    def __init__(self):
        self.db = DBConn()
        self.db_conn = self.db.db_get_connection()

    def get_tasks(self ,task_id = ""):
        status = False
        body = None
        try:
            with self.db_conn.cursor() as cursor:
                qry = """
                        SELECT td.task_id, td.parent_task_id, td.task_heading, td.task, td.assignment_date, td.status_id, sm.status,
                        td.deadline, td.assigned_user_count, td.max_assigned_user_count, td.finish_flag, td.creation_date, td.delete_flag, count(td1.task_id) as fork_number,
                        std.sub_task_id, std.sub_task_heading, std.sub_task, std.assignment_date as sub_assignment_date, std.status_id as sub_status_id, sm.status as sub_status,
                        std.deadline as sub_deadline, std.assigned_user_count AS sub_assigned_user_count, std.max_assigned_user_count AS sub_max_assigned_user_count, std.finish_flag AS sub_finish_flag, std.creation_date as sub_creation_date, std.delete_flag as sub_delete_flag
                        FROM task_details td
                        LEFT JOIN sub_task_details std ON std.task_id = td.task_id
                        LEFT JOIN status_master sm on sm.status_id = td.status_id or sm.status_id = std.status_id
                        LEFT JOIN task_details td1 on td1.parent_task_id = td.task_id
                        {}
                        GROUP BY td1.parent_task_id, td.task_id, sm.status, std.sub_task_id
                        ORDER BY deadline DESC, sub_deadline DESC;
                    """.format("WHERE td.task_id = %s" if task_id != "" else "")
                qry_data = (task_id,) if task_id != "" else ()
                cursor.execute(qry, qry_data)
                qry_result = cursor.fetchall()
        
        except Exception as e:
            status = False
            body = str(e)
            
        else:
            status = True
            body = qry_result
        
        finally:            
            return status, body
    
    def insert_task_subtask(self, data):
        status : bool = False
        body : str | list | dict = None

        task_id : int = None
        sub_task_list : list = []
        sub_task_qry_data : list = []

        try:
            with self.db_conn.cursor() as cursor:
                qry = """
                        INSERT INTO task_details (task_heading, task, assignment_date, status_id, deadline, assigned_user_count, max_assigned_user_count) 
                        VALUES
                        (%s, %s, %s, %s, %s, %s, %s) RETURNING task_id;
                    """
                qry_data = (data.task_heading, data.task, data.assignment_date, data.status_id, data.deadline, data.assigned_user_count, data.max_assigned_user_count)
                cursor.execute(qry, qry_data)
                qry_result = cursor.fetchone()
                task_id = qry_result["task_id"]
                
                print(f">> qry result -> {qry_result}")

                sub_task_list = data.sub_task_list

                if len(sub_task_list) > 0:
                    try:
                        for each_sub_task in sub_task_list:
                            # print(f">> each_sub_task -> {each_sub_task}")
                            each_sub_task = SubTaskData(**each_sub_task)
                            sub_task_qry_data.append(
                                (
                                    task_id,
                                    each_sub_task.sub_task_heading, 
                                    each_sub_task.sub_task, 
                                    each_sub_task.sub_assignment_date, 
                                    each_sub_task.sub_status_id, 
                                    each_sub_task.sub_deadline, 
                                    each_sub_task.sub_assigned_user_count,
                                    each_sub_task.sub_max_assigned_user_count,
                                )
                            )
                    except Exception as e:                    
                        raise Exception(e)
                    
                    try:
                        qry = """
                                INSERT INTO sub_task_details (task_id, sub_task_heading, sub_task, assignment_date, status_id, deadline, assigned_user_count, max_assigned_user_count) 
                                VALUES
                                (%s, %s, %s, %s, %s, %s, %s, %s);
                            """
                        cursor.executemany(qry, sub_task_qry_data)
                    
                    except Exception as e:                    
                        raise Exception(e)
        
        except Exception as e:
            self.db.db_rollback()
            status = False
            body = str(e)
            
        else:
            status = True
            body = task_id
        
        finally:            
            return status, body
        
    
    #: update task
    def update_task_subtask(self, data):
        status : bool = False
        body : str | list | dict = None

        task_id : int = None
        sub_task_list : list = []
        sub_task_qry_data : list = []

        try:
            with self.db_conn.cursor() as cursor:
                qry = """
                        UPDATE task_details SET task_heading = %s, task = %s, assignment_date = %s, status_id = %s, deadline = %s, assigned_user_count = %s, 
                        max_assigned_user_count = %s WHERE task_id = %s RETURNING task_id;
                    """
                qry_data = (data.task_heading, data.task, data.assignment_date, data.status_id, data.deadline, data.assigned_user_count, 
                            data.max_assigned_user_count, data.task_id)
                cursor.execute(qry, qry_data)
                qry_result = cursor.fetchone()
                task_id = qry_result["task_id"]
                
                # print(f">> qry result -> {qry_result}")

                sub_task_list = data.sub_task_list

                if len(sub_task_list) > 0:
                    try:                    
                        for each_sub_task in sub_task_list:
                            # print(f">> each_sub_task -> {each_sub_task}")
                            each_sub_task = SubTaskData(**each_sub_task)
                            if each_sub_task.sub_task_id == "" or each_sub_task.sub_task_id is None:
                                raise Exception("Sub Task ID cannot be empty.")
                            sub_task_qry_data.append(
                                (
                                    each_sub_task.sub_task_heading, 
                                    each_sub_task.sub_task, 
                                    each_sub_task.sub_assignment_date, 
                                    each_sub_task.sub_status_id, 
                                    each_sub_task.sub_deadline, 
                                    each_sub_task.sub_assigned_user_count,
                                    each_sub_task.sub_max_assigned_user_count,
                                    task_id
                                )
                            )
                    except Exception as e:                    
                        raise Exception(e)
                    
                    try:
                        qry = """
                                UPDATE sub_task_details SET sub_task_heading = %s, sub_task = %s, assignment_date = %s, status_id = %s, deadline = %s, assigned_user_count = %s,
                                max_assigned_user_count = %s WHERE sub_task_id = %s;
                            """
                        cursor.executemany(qry, sub_task_qry_data)
                    
                    except Exception as e:
                        raise Exception(e)
        
        except Exception as e:
            self.db.db_rollback()
            status = False
            body = str(e)
            
        else:
            status = True
            body = task_id
        
        finally:            
            return status, body
        
    
    #: create fork task
    def create_fork_task(self, data):
        status : bool = False
        body : str | list | dict = None

        task_id : int = None
        sub_task_list : list = []
        sub_task_qry_data : list = []

        try:
            with self.db_conn.cursor() as cursor:
                print(">> inserting parent task")
                qry = """
                        INSERT INTO task_details (parent_task_id, task_heading, task, assignment_date, status_id, deadline, assigned_user_count, max_assigned_user_count) 
                        VALUES
                        (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING task_id;
                    """
                qry_data = (data.parent_task_id, data.task_heading, data.task, data.assignment_date, data.status_id, data.deadline, data.assigned_user_count, 
                            data.max_assigned_user_count)
                cursor.execute(qry, qry_data)
                qry_result = cursor.fetchone()
                task_id = qry_result["task_id"]
                
                print(f">> qry result -> {qry_result}")
                
                # print(f">> qry result -> {qry_result}")

                sub_task_list = data.sub_task_list

                if len(sub_task_list) > 0:
                    try:                    
                        for each_sub_task in sub_task_list:
                            # print(f">> each_sub_task -> {each_sub_task}")
                            each_sub_task = SubTaskData(**each_sub_task)
                            sub_task_qry_data.append(
                                (
                                    task_id,
                                    each_sub_task.sub_task_heading, 
                                    each_sub_task.sub_task, 
                                    each_sub_task.sub_assignment_date, 
                                    each_sub_task.sub_status_id, 
                                    each_sub_task.sub_deadline, 
                                    each_sub_task.sub_assigned_user_count,
                                    each_sub_task.sub_max_assigned_user_count
                                    # task_id
                                )
                            )
                    except Exception as e:                    
                        raise Exception(e)
                    
                    try:
                        qry = """
                                INSERT INTO sub_task_details (task_id, sub_task_heading, sub_task, assignment_date, status_id, deadline, assigned_user_count, max_assigned_user_count) 
                                VALUES
                                (%s, %s, %s, %s, %s, %s, %s, %s);
                            """
                        cursor.executemany(qry, sub_task_qry_data)
                    
                    except Exception as e:
                        raise Exception(e)
        
        except Exception as e:
            self.db.db_rollback()
            status = False
            body = str(e)
            
        else:
            status = True
            body = task_id
        
        finally:            
            return status, body
        
        
    def commit_transactions(self):
        self.db.db_commit()
    
    def __del__(self):
        if self.db_conn:
            self.db.db_close()