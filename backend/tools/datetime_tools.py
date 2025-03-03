from datetime import datetime

class DateTimeTools:

    date_time : datetime = None
    __curr_date_time : datetime = None

    def __init__(self):
        self.__curr_date_time = datetime.now()

    def convert_to_def(self, date_time = None):
        status : bool = False
        body : str | list | dict = None

        try:
            if date_time is None:
                date_time = self.__curr_date_time
            # print(f">> date_time -> {date_time}")
            # print(f">> date_time -> {date_time}")
            # print(f">> type of date_time -> {type(date_time)}")
            
            if not isinstance(date_time, datetime):
                try:
                    date_time = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")

                except Exception as e:
                    status = False
                    body = str(e)
            # print(f">> date_time -> {date_time}")
            # print(f">> type of date_time -> {type(date_time)}")
            if date_time.tzinfo is not None:
                date_time = date_time.astimezone(datetime.utc).replace(tzinfo=None)
            # print(f">> date_time -> {date_time}")
            # print(f">> type of date_time -> {type(date_time)}")

            # date_time = date_time.replace(tzinfo=None).replace(microsecond=0)

            try:
                # date_time = date_time.strftime("%Y-%m-%d %H:%M:%S").strptime("%Y-%m-%d %H:%M:%S")
                date_time = date_time.replace(microsecond=0)                
            except Exception as e:
                status = False
                body = str(e)
            # print(f">> date_time -> {date_time}")
            # print(f">> type of date_time -> {type(date_time)}")
        
        except Exception as e:
            status = False
            body = str(e)

        else:
            status = True
            body = date_time

        finally:
            return status, body

if __name__ == "__main__":
    dt = DateTimeTools()
    dt.convert_to_def("2023-02-25")