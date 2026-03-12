from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict
from server.src.utility.terraform_utility import *
from server.src.utility.curr_terr_utility import *

app=FastAPI()

class TerraformVariables(BaseModel):
    input: Dict[str, str]
class Resource(BaseModel):
    resource: str
@app.get("/")
def hello():
    return {"message":"hello world"}
@app.get("/terraform/init")
def init_terraform():
    return initialize_terraform()
@app.get("/terraform/state")
def current_state():
    return get_current_state()
@app.post("/terraform/plan")
def create_plan(payload: TerraformVariables):
    return get_desired_state(payload.input)
@app.post("/terraform/apply")
def apply_plan(plan_name: str = "tfplan"):
    return execute_terraform(plan_name)
@app.post("/addresource")
def add_resource(resource:Resource):
    res=add_to_curr_terraform(resource.resource)
    return {"message":"success" if res else "failed"}