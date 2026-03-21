from api_calls import execute_steps
static_data="""{
  "steps":[
    {
        "step":1,
        "route":"POST /terraform/destroy",
        "input":{
            "plan_name": "tfplan"
        }
    }
  ]
}"""

execute_steps(static_data)