import psycopg as postgres

class DBConn:
    db_conn = None
    host : str = None
    dbname : str = None
    user : str = None
    password : str = None
    port : int = None

    def __init__(self):
        self.host = "192.168.29.161"
        self.dbname = "aquazoid_task"
        self.user = "aquazoid_usr_01"
        self.password = "Aquazoid@2023"
        self.port = 5432
    
    def db_get_connection(self):
        self.db_conn = postgres.connect(
                host = self.host,
                dbname = self.dbname,
                user = self.user,
                password = self.password,
                port  = self.port,
                row_factory=postgres.rows.dict_row        
            )

        print("Connected to DB")
        
        return self.db_conn       

    def db_commit(self):
        self.db_conn.commit()
    
    def db_rollback(self):
        self.db_conn.rollback()

    def db_close(self):
        self.db_conn.close()    
        print("DB connection closed")
    