import subprocess
import json
import re
import os

TEMPLATE_PATH = os.path.join(os.getcwd(),"agent\infra_templates\ec2_basic")

def check_terraform():
    try:
        subprocess.run(["terraform", "init"],cwd=TEMPLATE_PATH, check=True)
    except subprocess.CalledProcessError as e:
        return {"status": "error", "message": str(e)}
def get_current_state():
    try:
        print("Process CWD:", os.getcwd())
        print("Template Path:", TEMPLATE_PATH)
        print("Path Exists:", os.path.exists(TEMPLATE_PATH))
        result=subprocess.run(["terraform","show","-json"],cwd=os.path.abspath(TEMPLATE_PATH))
        if result.returncode!=0:
            return {"status": "error", "message": result.stderr}
    except subprocess.CalledProcessError as e:
        return {"status": "error", "message": str(e)}

def get_desired_state(plan):
    cmd=["terraform","plan"]
    for k,v in plan.items():
        cmd.append("-var")
        cmd.append(f"{k}={v}")
    cmd.append("-out=tfplan")
    try:
        subprocess.run(cmd,cwd=TEMPLATE_PATH)
        result =subprocess.run(["terraform","show","-json","tfplan"])
        if result.returncode!=0:
            return {"status": "error", "message": result.stderr}
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        return {"status": "error", "message": str(e)}