import subprocess
import os
import shlex
import json

def run_docker_compose():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(script_dir))
    compose_file_yml = os.path.join(project_root, "docker-compose.yml")
    compose_file_yaml = os.path.join(project_root, "docker-compose.yaml")
    if os.path.exists(compose_file_yml) or os.path.exists(compose_file_yaml):
        subprocess.run(["sudo", "docker-compose", "up", "-d"], cwd=project_root)
    else:
        print(f"docker-compose.yml or docker-compose.yaml not found in {project_root}. Skipping docker-compose up.")

def check_env_file():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(script_dir))
    env_path = os.path.join(project_root, ".env")
    if os.path.exists(env_path):
        with open(env_path) as f:
            for i, line in enumerate(f, 1):
                line = line.strip()
                if line and not line.startswith("#") and "=" not in line:
                    print(f"WARNING: .env file syntax error at line {i}: {line}")

def load_env_vars(env_path):
    """Load environment variables from a .env file into a dict."""
    env_vars = {}
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                env_vars[key.strip()] = value.strip()
    return env_vars

def start_services_from_services_json():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(script_dir))
    services_json_path = os.path.join(project_root, "services.json")
    env_path = os.path.join(project_root, ".env")
    venv_python = os.path.join(project_root, ".venv", "bin", "python3.12")

    if not os.path.exists(services_json_path):
        print(f"{services_json_path} not found.")
        return

    # Load environment variables from .env
    env_vars = os.environ.copy()
    env_vars.update(load_env_vars(env_path))

    with open(services_json_path, "r") as f:
        try:
            services = json.load(f)
        except Exception as e:
            print(f"Error reading {services_json_path}: {e}")
            return

    for service in services:
        folder = service.get("ServiceFolderName")
        filename = service.get("ServiceFileName")
        if not folder or not filename:
            continue
        service_path = os.path.join(project_root, folder, filename)
        if not os.path.exists(service_path):
            print(f"Service file {service_path} not found. Skipping.")
            continue
        cmd = f"{venv_python} {folder}/{filename}"
        print(f"Starting: {cmd}")
        try:
            subprocess.Popen(
                shlex.split(cmd),
                cwd=project_root,
                env=env_vars
            )
        except FileNotFoundError as e:
            print(f"ERROR: {e}. Check if the venv and service files exist.")

if __name__ == "__main__":
    check_env_file()
    run_docker_compose()
    start_services_from_services_json()
