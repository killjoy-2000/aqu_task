from utils import db_conn

def main():
    db_conn = db_conn.DBConn()
    print(db_conn)



if __name__ == "__main__":
    main()