import subprocess
import os
import shlex

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

def start_services_from_sh():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(script_dir))
    start_sh_path = os.path.join(project_root, "ServerScripts", "start-server.sh")
    if not os.path.exists(start_sh_path):
        print(f"{start_sh_path} not found.")
        return

    with open(start_sh_path, "r") as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        # Skip comments and placeholder
        if not line or line.startswith("#") or "#<ADD_SERVICE_START_HERE>" in line:
            continue
        if ".venv/bin/python3.12" in line:
            cmd = line.replace("&", "").strip()
            print(f"Starting: {cmd}")
            try:
                subprocess.Popen(shlex.split(cmd), cwd=project_root)
            except FileNotFoundError as e:
                print(f"ERROR: {e}. Check if the venv and service files exist.")

if __name__ == "__main__":
    check_env_file()
    run_docker_compose()
    start_services_from_sh()
