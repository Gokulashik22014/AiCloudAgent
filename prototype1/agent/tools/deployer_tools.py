# executor.py

import subprocess
import json

TEMPLATE_PATH = "../infra_templates/ec2_basic"

def deploy_ec2(instance_type: str, instance_name: str) -> dict:

    try:
        subprocess.run(
            [
                "terraform",
                "apply",
                "-auto-approve",
                "-var", f"instance_type={instance_type}",
                "-var", f"instance_name={instance_name}"
            ],
            cwd=TEMPLATE_PATH,
            check=True
        )

        result = subprocess.run(
            ["terraform", "output", "-json"],
            cwd=TEMPLATE_PATH,
            capture_output=True,
            text=True,
            check=True
        )

        return {
            "status": "success",
            "outputs": json.loads(result.stdout)
        }

    except subprocess.CalledProcessError as e:
        return {"status": "error", "message": str(e)}