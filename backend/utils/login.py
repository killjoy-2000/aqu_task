from dotenv import load_dotenv
import os

from utils.db_conn import DBConn
from tools.authenticator import Authenticator


class Login:
    __db = None
    __db_conn = None
    __auth = None
    __hashed_user_id = None
    __hashed_password = None

    def __init__(self):
        self.__db = DBConn()
        self.__db_conn = self.__db.db_get_connection()
        self.__auth = Authenticator()
        # load_dotenv()
        # self.hask_key = os.getenv("HASH_KEY")
    
    def __record_login(self, data):
        status : bool = False
        body : str | list | dict = None
        login_session_id : int = None

        try:
            with self.__db_conn.cursor() as cursor:
                try:
                    qry = """
                            INSERT INTO login_record (user_name) VALUES (%s) RETURNING login_session_id;
                        """
                    qry_data = (data,)
                    cursor.execute(qry, qry_data)
                    qry_result = cursor.fetchone()
                    login_session_id = qry_result["login_session_id"]
                
                except Exception as e:
                    raise Exception(e)
            
        except Exception as e:
            status = False
            body = str(e)

        else:
            status = True
            body = login_session_id

        finally:
            return status, body
    
    def login(self, data):
        status : bool = False
        body : str | list | dict = None

        try:
            print(f">> data -> {data}")
            try:
                self.__hashed_user_id = self.__auth.hash_it(data.user_name)
            except Exception as e:
                print(e)
                raise Exception(e)
            try:
                self.__hashed_password = self.__auth.hash_it(data.password)
            except Exception as e:
                print(e)
                raise Exception(e)

            print(f">> self.__hashed_user_id -> {self.__hashed_user_id}")
            print(f">> self.__hashed_password -> {self.__hashed_password}")

        except Exception as e:
            status = False
            body = str(e)

        else:
            status = True
            body = "Success"

        finally:
            return status, body
    

    def register(self, data):
        status : bool = False
        body : str | list | dict = None
        user_login_id : int = None
        login_session_id : int = None

        try:
            print(f">> data -> {data}")
            try:
                self.__hashed_user_id = self.__auth.hash_it(data.user_name)
            except Exception as e:
                print(e)
                raise Exception(e)
            try:
                self.__hashed_password = self.__auth.hash_it(data.password)
            except Exception as e:
                print(e)
                raise Exception(e)

        except Exception as e:
            status = False
            body = str(e)

        else:
            try:
                with self.__db_conn.cursor() as cursor:
                    try:
                        qry = """
                                SELECT 1 FROM login_details where user_name = %s;
                            """
                        qry_data = (self.__hashed_user_id,)
                        cursor.execute(qry, qry_data)
                        qry_result = cursor.fetchone()
                        if qry_result is not None:
                            raise Exception("EXISTSUSER")
                    
                    except Exception as e:
                        raise Exception(e)
                    
                    try:
                        qry = """
                                INSERT INTO login_details (user_name, user_password) VALUES (%s, %s) RETURNING user_login_id;
                            """
                        qry_data = (self.__hashed_user_id, self.__hashed_password)
                        cursor.execute(qry, qry_data)
                        qry_result = cursor.fetchone()
                        user_login_id = qry_result["user_login_id"]
                    
                    except Exception as e:
                        raise Exception(e)

                    fn_status, fn_body = self.__record_login(self.__hashed_user_id)
                    if not fn_status:
                        raise Exception(fn_body)

                    login_session_id = fn_body
                    

            except Exception as e:
                status = False
                body = str(e)

            else:
                status = True
                body = {
                    "user_login_id" : user_login_id,
                    "login_session_id" : login_session_id
                } 

        finally:
            return status, body
        
    
    def commit_transactions(self):
        self.__db.db_commit()
    
    def __del__(self):
        if self.__db_conn:
            self.__db.db_close()
    