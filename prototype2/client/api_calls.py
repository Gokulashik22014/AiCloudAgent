import json
import requests

BASE_URL = "http://localhost:8000"

def execute_steps(plan_string: str):
    plan = json.loads(plan_string)

    for step in sorted(plan["steps"], key=lambda x: x["step"]):
        method, route = step["route"].split(" ", 1)
        url = BASE_URL + route
        payload = step.get("input", {})

        print(f"Executing Step {step['step']} -> {method} {route}")

        if method == "GET":
            response = requests.get(url, params=payload)

        elif method == "POST":
            response = requests.post(url, json=payload)

        else:
            raise ValueError(f"Unsupported HTTP method: {method}")

        print("Status:", response.status_code)
        print("Response:", response.text)
        print("-" * 40)

    print("Execution Completed")