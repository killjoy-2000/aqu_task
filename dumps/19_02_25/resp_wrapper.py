import traceback
from functools import wraps
import ast

def auto_response(func):
    
    @wraps(func)
    async def wrapper(*args, **kwargs):
        func_name = func.__name__.upper()  # Get function name for error codes
        rmsg : str = "error"
        ercode: int = 0

        try:
            response = await func(*args, **kwargs)
            
            return {
                "respstatus": {
                    "rcode": "000",
                    "rmsg": "SUCCESS",
                    "ermsg": ""
                },
                "respbody": response if response else {}
            }
            
        except Exception as e:
            # error_code = f"{func_name}-100"  # You can increment this dynamically if needed
            # err = traceback.format_exc()
            error_info = getattr(e, "args", [{}])[0]  # Get the first argument (should be a dict)
            print(f">> error_info -> {error_info}")
            # if isinstance(error_info, dict):
            #     rmsg = error_info.get("rmsg", "ERROR")
            #     ercode = error_info.get("error_number", 100)
            # else:
            #     rmsg = "Unhandled Exception"
            #     ercode = 100

            # err = kwargs.get("err", {})
            # rmsg = err.get("rmsg", "ERROR")
            # rmsg = getattr(func, "rmsg", "ERROR")
            # ercode = getattr(func, "ercode", "100")
            # ercode = err.get("ercode", "100")
            # ercode, rmsg, error = func.__code__.co_consts

            # print(f">> ercode -> {ercode}, rmsg -> {rmsg}, error -> {error}")
            # x = ast.literal_eval(str(e))
            # print(f">> x -> {x}")
            # print(e)
            # print(f">> type of e -> {type(e)}")
            err_args = tuple(e.args)
            try:
                ercode = err_args[0]
            except:
                ercode = 100
            try:
                rmsg = err_args[1]
            except:
                rmsg = "ERROR"
            # print(f">> err_args -> {err_args}")
            # print(f">> c -> {c}")
            error_code = f"{func_name}-{ercode}"
            return {
                "respstatus": {
                    "rcode": error_code,
                    "rmsg": rmsg,
                    "ermsg": str(e)
                },
                "respbody": {}
            }
    return wrapper
