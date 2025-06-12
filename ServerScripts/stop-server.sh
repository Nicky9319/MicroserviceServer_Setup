clear

sudo docker-compose down
sleep 1

# Find the parent directory and services.json path
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PARENT_DIR="$(dirname "$SCRIPT_DIR")"
SERVICES_JSON="$PARENT_DIR/services.json"

if [ ! -f "$SERVICES_JSON" ]; then
    echo "Service JSON file not found at $SERVICES_JSON"
    exit 1
fi

# Install jq if not present
if ! command -v jq &> /dev/null; then
    echo "jq is required but not installed. Installing jq..."
    sudo apt-get update && sudo apt-get install -y jq
fi

# Extract ports using jq (requires jq installed)
PORTS=$(jq -r '.[] | [.ServiceHttpPort, .ServiceWsPort][] | select(. != null)' "$SERVICES_JSON")

echo "Ports to stop: $PORTS"

for PORT in $PORTS; do
    PID=$(lsof -ti :"$PORT")
    if [ -n "$PID" ]; then
        sudo kill -9 "$PID"
        echo "$PORT : Service Stopped"
    else
        echo "$PORT : No Service Found"
    fi
done

sleep 3