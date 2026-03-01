import re

ALLOWED_INSTANCE_TYPES = [
    "t2.micro",
    "t3.micro",
]

MIN_INSTANCE_COUNT = 1
MAX_INSTANCE_COUNT = 3

MAX_NAME_LENGTH = 20
ALLOWED_NAME_PATTERN = r"^[a-zA-Z0-9\-]+$"

def check_valid_values(plan):
    try:
        REQUIRED_KEYS = {
            "instance_type",
            "instance_name",
            "instance_count",
        }

        # Check required keys exist
        if not REQUIRED_KEYS.issubset(plan.keys()):
            return {
                "status": "error",
                "message": f"Missing required keys. Required: {REQUIRED_KEYS}"
            }

        # Instance type validation
        if plan["instance_type"] not in ALLOWED_INSTANCE_TYPES:
            return {
                "status": "error",
                "message": "Instance type not allowed"
            }

        # Instance count validation
        if not isinstance(plan["instance_count"], int):
            return {
                "status": "error",
                "message": "Instance count must be an integer"
            }

        if not (MIN_INSTANCE_COUNT <= plan["instance_count"] <= MAX_INSTANCE_COUNT):
            return {
                "status": "error",
                "message": "Instance count out of allowed range"
            }

        # Instance name validation
        name = plan["instance_name"]

        if not isinstance(name, str):
            return {
                "status": "error",
                "message": "Instance name must be a string"
            }

        if len(name) > MAX_NAME_LENGTH:
            return {
                "status": "error",
                "message": "Instance name too long"
            }

        if not re.match(ALLOWED_NAME_PATTERN, name):
            return {
                "status": "error",
                "message": "Invalid instance name format"
            }

        return {"status": "ok"}

    except Exception as e:
        return {"status": "error", "message": str(e)}