import subprocess
import os
import json

def find_pid_by_port(port):
    """Find the PID of the process running on the specified port."""
    result = subprocess.run(["lsof", "-i", f":{port}"], capture_output=True, text=True)
    lines = result.stdout.splitlines()
    if len(lines) > 1:
        # Extract the PID from the output
        pid = int(lines[1].split()[1])
        return pid
    return None

def stop_service_on_port(port):
    """Stop the service running on the specified port."""
    pid = find_pid_by_port(port)
    if pid:
        subprocess.run(["sudo", "kill", "-9", str(pid)])
        print(f"{port} : Service Stopped")
    else:
        print(f"{port} : No Service Found")



def discover_ports():
    """Discover the ports that are currently in use and print their parent addresses."""
    parent_address = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    print(f"Parent folder absolute address: {parent_address}")

    service_json_file_path = os.path.join(parent_address, "services.json")
    if not os.path.exists(service_json_file_path):
        print(f"Service JSON file not found at {service_json_file_path}")
        return []
    
    # Here you would implement the logic to read the service.json file
    # and extract the ports you want to stop.

    services_data = {}
    with open(service_json_file_path, "r") as f:
        services_data = json.load(f)

    # Example: return a list of ports to stop (replace with your logic)
    httpPorts = [service["ServiceHttpPort"] for service in services_data if service["ServiceHttpPort"] is not None]
    wsPorts = [service["ServiceWsPort"] for service in services_data if service["ServiceWsPort"] is not None]

    return httpPorts + wsPorts

def stopServer():
    # Mention the Ports you want to stop
    portList = discover_ports()
    print(portList)

    for ports in portList:
        stop_service_on_port(ports)


stopServer()
