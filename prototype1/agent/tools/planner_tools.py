import subprocess
import json
import re
import os

TEMPLATE_PATH = os.path.join(os.getcwd(),"agent\infra_templates\ec2_basic")

# Allowed AWS Regions
ALLOWED_REGIONS = [
    "ap-south-1",      # Mumbai
]

# Allowed EC2 Instance Types
ALLOWED_INSTANCE_TYPES = [
    "t2.micro",
    "t3.micro",
]

# Allowed AMIs (example IDs - replace with real ones)
ALLOWED_AMIS = [
    "ami-0abcdef1234567890",
]

# Instance Count Limits
MIN_INSTANCE_COUNT = 1
MAX_INSTANCE_COUNT = 3

# Volume Constraints
MIN_VOLUME_SIZE = 8          # GB
MAX_VOLUME_SIZE = 30         # GB
ALLOWED_VOLUME_TYPES = [
    "gp2",
    "gp3"
]

# Tag Constraints
REQUIRED_TAG_KEYS = [
    "Environment",
    "Owner"
]

# Naming Constraints
MAX_NAME_LENGTH = 20
ALLOWED_NAME_PATTERN = r"^[a-zA-Z0-9\-]+$"

# Security Restrictions
ALLOW_PUBLIC_IP = False

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

def check_valid_values(plan):
    try:
        # Required keys
        REQUIRED_KEYS = {
            "instance_type",
            "region",
            "ami",
            "count",
            "volume_size",
            "volume_type",
            "name",
            "tags",
            "associate_public_ip_address"
        }

        if set(plan.keys()) != REQUIRED_KEYS:
            return {
                "status": "error",
                "message": f"Invalid keys. Expected: {REQUIRED_KEYS}"
            }

        # Region validation
        if plan["region"] not in ALLOWED_REGIONS:
            return {"status": "error", "message": "Region not allowed"}

        # Instance type validation
        if plan["instance_type"] not in ALLOWED_INSTANCE_TYPES:
            return {"status": "error", "message": "Instance type not allowed"}

        # AMI validation
        if plan["ami"] not in ALLOWED_AMIS:
            return {"status": "error", "message": "AMI not allowed"}

        # Count validation
        if not isinstance(plan["count"], int):
            return {"status": "error", "message": "Count must be integer"}

        if not (MIN_INSTANCE_COUNT <= plan["count"] <= MAX_INSTANCE_COUNT):
            return {"status": "error", "message": "Instance count out of allowed range"}

        # Volume size validation
        if not (MIN_VOLUME_SIZE <= plan["volume_size"] <= MAX_VOLUME_SIZE):
            return {"status": "error", "message": "Volume size out of allowed range"}

        # Volume type validation
        if plan["volume_type"] not in ALLOWED_VOLUME_TYPES:
            return {"status": "error", "message": "Volume type not allowed"}

        # Name validation
        if len(plan["name"]) > MAX_NAME_LENGTH:
            return {"status": "error", "message": "Name too long"}

        if not re.match(ALLOWED_NAME_PATTERN, plan["name"]):
            return {"status": "error", "message": "Invalid name format"}

        # Required tag keys
        if not isinstance(plan["tags"], dict):
            return {"status": "error", "message": "Tags must be a dictionary"}

        for key in REQUIRED_TAG_KEYS:
            if key not in plan["tags"]:
                return {"status": "error", "message": f"Missing required tag: {key}"}

        # Public IP restriction
        if plan["associate_public_ip_address"] and not ALLOW_PUBLIC_IP:
            return {"status": "error", "message": "Public IP association not allowed"}

        return {"status": "ok"}

    except Exception as e:
        return {"status": "error", "message": str(e)}
