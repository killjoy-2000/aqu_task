import importlib
import pkgutil
from fastapi import FastAPI, Request, HTTPException, Depends
from pathlib import Path
from fastapi.routing import APIRoute

app = FastAPI()

ROUTE_MAPPING = {}  # Stores action-to-endpoint mappings
ROUTER_FUNCTIONS = {}  # Stores function references

# Dynamically load all routers from the "routers" directory
def load_routers():
    routers_package = "routers"
    routers_path = Path(routers_package).resolve()
    
    for _, module_name, _ in pkgutil.iter_modules([str(routers_path)]):
        module = importlib.import_module(f"{routers_package}.{module_name}")
        
        if hasattr(module, "router"):
            app.include_router(module.router)
            
            # Map actions to router function references
            for route in module.router.routes:
                if isinstance(route, APIRoute) and hasattr(route.endpoint, "__name__"):
                    action_name = route.endpoint.__name__
                    ROUTE_MAPPING[action_name] = route.path
                    ROUTER_FUNCTIONS[action_name] = route.endpoint  # Store function reference

# Load routers dynamically
load_routers()

@app.post("/gateway")
async def api_gateway(request: Request):
    payload = await request.json()
    action = payload.get("action")

    if not action or action not in ROUTER_FUNCTIONS:
        raise HTTPException(status_code=400, detail="Invalid action")

    # Call the appropriate function directly and return the response
    response_data = await ROUTER_FUNCTIONS[action](payload)
    return response_data
