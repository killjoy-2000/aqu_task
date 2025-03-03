import traceback
from functools import wraps
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse

def auto_response(func):
    
    @wraps(func)
    async def wrapper(*args, **kwargs):
        func_name = func.__name__.upper()  # Get function name for error codes
        rmsg : str = "Unhandled Exception"
        ercode: int = 500
        error_data = None

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
            err_args = tuple(e.args)
            try:
                ercode = err_args[0]
            except:
                ercode = ercode
            try:
                rmsg = err_args[1]
            except:
                rmsg = rmsg
            try:
                error_data = err_args[2]
            except:
                error_data = str(e)

            error_code = f"{func_name}-{ercode}"

            print(f">> Error code -> {error_code}")
            print(f">> Error - > {error_data}")

            return {
                "respstatus": {
                    "rcode": error_code,
                    "rmsg": rmsg,
                    "ermsg": error_data
                },
                "respbody": {}
            }
    return wrapper
