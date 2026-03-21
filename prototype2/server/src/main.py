from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from server.src.utility.terraform_utility import *
from server.src.utility.curr_terr_utility import *

app=FastAPI()

class TerraformVariables(BaseModel):
    region: Optional[str]
    instance_type: Optional[str]
    ami: Optional[str]
    instance_name: Optional[str]
class Resource(BaseModel):
    type: str
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
    return get_desired_state(payload.model_dump())
@app.post("/terraform/apply")
def apply_plan(plan_name: str = "tfplan"):
    return execute_terraform(plan_name)
@app.post("/terraform/destroy")
def destroy_resource(targets=None):
    return destroy_terraform(targets)
@app.post("/addresource")
def add_resource(resource:Resource):
    res=add_to_curr_terraform(resource.type)
    return {"message":"success" if res else "failed"}