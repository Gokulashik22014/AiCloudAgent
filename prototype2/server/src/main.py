from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict
from utility.terraform_utility import *
from utility.curr_terr_utility import *

app=FastAPI()

class TerraformVariables(BaseModel):
    variables: Dict[str, str]
class Resource(BaseModel):
    value: str
@app.get("/")
def hello():
    return {"message":"hello world"}
@app.get("/terraform/state")
def current_state():
    return get_current_state()
@app.post("/terraform/plan")
def create_plan(payload: TerraformVariables):
    return get_desired_state(payload.variables)
@app.post("/terraform/apply")
def apply_plan(plan_name: str = "tfplan"):
    return execute_terraform(plan_name)
@app.post("/addresource")
def add_resource(resource:Resource):
    res=add_to_curr_terraform(resource.value)
    return {"message":"success" if res else "failed"}