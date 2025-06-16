import subprocess
import os
import shlex

def stop_docker_compose():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(script_dir))
    compose_file_yml = os.path.join(project_root, "docker-compose.yml")
    compose_file_yaml = os.path.join(project_root, "docker-compose.yaml")
    if os.path.exists(compose_file_yml) or os.path.exists(compose_file_yaml):
        subprocess.run(["sudo", "docker-compose", "down"], cwd=project_root)
    else:
        print(f"docker-compose.yml or docker-compose.yaml not found in {project_root}. Skipping docker-compose down.")

def run_docker_compose():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(script_dir))
    compose_file_yml = os.path.join(project_root, "docker-compose.yml")
    compose_file_yaml = os.path.join(project_root, "docker-compose.yaml")
    if os.path.exists(compose_file_yml) or os.path.exists(compose_file_yaml):
        subprocess.run(["sudo", "docker-compose", "up", "-d"], cwd=project_root)
    else:
        print(f"docker-compose.yml or docker-compose.yaml not found in {project_root}. Skipping docker-compose up.")

def stop_services():
    # Import and call stopServer from stop-server.py
    import sys
    import importlib.util
    script_dir = os.path.dirname(os.path.abspath(__file__))
    stop_server_path = os.path.join(script_dir, "stop-server.py")
    spec = importlib.util.spec_from_file_location("stop_server", stop_server_path)
    stop_server = importlib.util.module_from_spec(spec)
    sys.modules["stop_server"] = stop_server
    spec.loader.exec_module(stop_server)

def start_services():
    # Import and call start_services_from_sh from start-server.py
    import sys
    import importlib.util
    script_dir = os.path.dirname(os.path.abspath(__file__))
    start_server_path = os.path.join(script_dir, "start-server.py")
    spec = importlib.util.spec_from_file_location("start_server", start_server_path)
    start_server = importlib.util.module_from_spec(spec)
    sys.modules["start_server"] = start_server
    spec.loader.exec_module(start_server)

if __name__ == "__main__":
    stop_docker_compose()
    stop_services()
    run_docker_compose()
    start_services()
