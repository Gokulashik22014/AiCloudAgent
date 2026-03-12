import subprocess
import os 
import json

TERRAFORM_PATH=os.path.join(os.getcwd(),"server","curr_terraform")

def initialize_terraform():
    try:
        result=subprocess.run(["terraform","init"],check=True,cwd=TERRAFORM_PATH,capture_output=True)
        return {
            "status": "success",
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }
    except subprocess.CalledProcessError as e:
        return {
            "status": "terraform_error",
            "stdout": e.stdout,
            "stderr": e.stderr,
            "returncode": e.returncode
        }
    except Exception as e:
        return {
            "status":"unexpected error",
            "message":str(e)
        }

def execute_terraform(plan_name):
    try:
        result = subprocess.run(
            ["terraform", "apply", plan_name, "-auto-approve"],
            cwd=TERRAFORM_PATH,
            capture_output=True,
            text=True,
            check=True
        )

        return {
            "status": "success",
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }

    except subprocess.CalledProcessError as e:
        return {
            "status": "terraform_error",
            "stdout": e.stdout,
            "stderr": e.stderr,
            "returncode": e.returncode
        }

    except Exception as e:
        return {
            "status": "unexpected_error",
            "message": str(e)
        }

def run_show(plan=""):
    try:
        result = subprocess.run(
            ["terraform", "show","-json",plan],
            cwd=TERRAFORM_PATH,
            capture_output=True,
            text=True,
            check=True
        )
        print("running run_show")
        data=json.loads(result.stdout)
        print(data)
        return {
            "status": "success",
            "stdout": data,
            "stderr": result.stderr,
            "returncode": result.returncode
        }

    except subprocess.CalledProcessError as e:
        return {
            "status": "terraform_error",
            "stdout": e.stdout,
            "stderr": e.stderr,
            "returncode": e.returncode
        }

    except Exception as e:
        return {
            "status": "unexpected_error",
            "message": str(e)
        }
def get_current_state():
    return run_show()

def get_desired_state(variables):
    cmd=["terraform","plan"]
    for key,value in variables.items():
        cmd.extend(["-var",f"{key}={value}"])
    cmd.append("-out=tfplan")
    try:
        result=subprocess.run(cmd,cwd=TERRAFORM_PATH,check=True)
        return run_show("tfplan")
    except subprocess.CalledProcessError as e:
        return {
            "status": "terraform_error",
            "stdout": e.stdout,
            "stderr": e.stderr,
            "returncode": e.returncode
        }

    except Exception as e:
        return {
            "status": "unexpected_error",
            "message": str(e)
        } 