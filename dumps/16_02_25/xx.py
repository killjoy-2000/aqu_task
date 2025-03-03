import uvicorn
import importlib
import pkgutil
import inspect
from pathlib import Path
from fastapi import FastAPI, HTTPException, Depends
from fastapi.routing import APIRoute
from typing import Union
from pydantic import BaseModel
import json
from routes import *


from utils import task


#: variables
routes_map : dict = {}
routes_functions : dict = {}
routes_package : str = "routes"
routes_path : Path = Path(__file__).parent / routes_package
print(routes_path)
# x = Path(routes_package).resolve()
# print(x)

app = FastAPI()

for _, module_name, _ in pkgutil.iter_modules([str(routes_path)]):
    module = importlib.import_module(f"{routes_package}.{module_name}")
    print(f">> module -> {module}")
    
    if hasattr(module, "router"):
        app.include_router(module.router)
        
        # Automatically map router endpoints to actions (assumes function names are unique)
        for route in module.router.routes:
            print(f">> route -> {route}")
            if hasattr(route, "endpoint"):
                print(f">> endpoint -> {route.endpoint}")
                # action_name = route.endpoint.__name__  # e.g., "get_data"
                # routes_map[action_name] = route.path  # Store path
                if isinstance(route, APIRoute) and hasattr(route.endpoint, "__name__"):
                    action_name = route.endpoint.__name__
                    print(f">> action_name -> {action_name}")
                    routes_map[action_name] = route.path
                    print(f">> routes_map -> {routes_map}")
                    routes_functions[action_name] = route.endpoint  # Store function reference
                    print(f">> routes_functions -> {routes_functions}")


print(f">> routes_map -> {routes_map}")

class Request_data(BaseModel):
    signature: dict
    payload: dict


@app.post("/")
async def root(request_data: Request_data):
    print(request_data)
    print(f">> type of request_data -> {type(request_data)}")
    # a = await request_data.json()
    sig = request_data.signature
    route_id = sig["route_id"]
    print(f">> sig -> {sig}")
    print(f">> route_id -> {route_id}")

    if not route_id or route_id not in routes_map:
        raise HTTPException(status_code=404, detail="Route not found")
    
    target_route = routes_map[route_id]
    print(f">> target_route -> {target_route}")
    # return target_route

    # resp = await routes_functions[route_id](request_data)
    if inspect.iscoroutinefunction(routes_functions[route_id]):
        print(">> iscoroutinefunction")
        print(f">> routes_functions[route_id] -> {routes_functions[route_id]}")
        # resp = await routes_functions[route_id](request_data.model_dump())
    else:
        print(">> not iscoroutinefunction")
        # resp = routes_functions[route_id](request_data)
    # print(f">> resp -> {resp}")

    return 1

    

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)