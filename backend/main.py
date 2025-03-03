import uvicorn
import importlib
import pkgutil
import httpx
from pathlib import Path
from typing import Annotated
from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.routing import APIRoute
from typing import Union
from pydantic import BaseModel
import json
from dotenv import load_dotenv
import os
from routes import *


from utils.pydan_master import HeadersLogin



#: variables
routes_map : dict = {}
routes_functions : dict = {}
routes_package : str = "routes"
routes_path : Path = Path(__file__).parent / routes_package
response = None
sig : dict
route_id : str

app = FastAPI()

for _, module_name, _ in pkgutil.iter_modules([str(routes_path)]):
    module = importlib.import_module(f"{routes_package}.{module_name}")
    print(f">> module -> {module}")
    
    if hasattr(module, "router"):
        app.include_router(module.router)
        print(f">> module.router -> {module.router}")
        
        # Automatically map router endpoints to actions (assumes function names are unique)
        for route in module.router.routes:
            print(f">> route -> {route}")
            if hasattr(route, "endpoint"):
                print(f">> endpoint -> {route.endpoint}")
                print(f">> route.path -> {route.path}")
                action_name = route.endpoint.__name__
                routes_map[action_name] = route.path
                

print(f">> routes_map -> {routes_map}")

class Request_data(BaseModel):
    signature: dict
    payload: dict


@app.post("/")
async def root(request_data: Request_data):
    print(request_data)
    # print(f">> type of request_data -> {type(request_data)}")
    sig = request_data.signature
    route_id = sig["route_id"]
    # print(f">> sig -> {sig}")
    # print(f">> route_id -> {route_id}")

    if not route_id or route_id not in routes_map:
        raise HTTPException(status_code=404, detail="Invalid API call")
    
    target_route = routes_map[route_id]
    print(f">> target_route -> {target_route}")
    # return target_route

    async with httpx.AsyncClient() as client:
        resp = await client.post(f"http://localhost:8000{target_route}", json=request_data.payload)
        # print(f">> type of resp -> {type(resp)}")
        # print(f">> resp -> {resp}") 

    return resp.json()

@app.post("/login")
async def login(request_data: Request_data, headers: Annotated[HeadersLogin, Header()]):    
    sig = request_data.signature
    route_id = sig["route_id"]
    

    if not route_id.startswith("LG"):
        raise HTTPException(status_code=403, detail="Access Denied")
    if not route_id or route_id not in routes_map:
        raise HTTPException(status_code=404, detail="Invalid API call")
    
    load_dotenv()
    if headers.x_api_key != os.getenv("X_API_KEY"):
        raise HTTPException(status_code=403, detail="Access Denied")
    
    target_route = routes_map[route_id]

    async with httpx.AsyncClient() as client:
        resp = await client.post(f"http://localhost:8000{target_route}", json=request_data.payload)

    return resp.json()

    

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)