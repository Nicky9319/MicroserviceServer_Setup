#!/bin/bash

set -e

# Prompt for service name with validation
while true; do
    read -p "Enter the Service Name (no spaces, dashes, slashes, commas): " SERVICE_NAME
    SERVICE_NAME=$(echo "$SERVICE_NAME" | xargs) # trim
    if [[ -z "$SERVICE_NAME" ]]; then
        echo "Service Name cannot be empty."
        continue
    fi
    if [[ "$SERVICE_NAME" =~ [\ ,/-] ]]; then
        echo "Service Name should not contain spaces, dashes, slashes, or commas."
        continue
    fi
    break
done

SERVICE_FOLDER="service_${SERVICE_NAME}Service"
SERVICE_FILE="${SERVICE_NAME,,}-service.py"

# Prompt for HTTP server
read -p "Do you want to add an HTTP Server? (yes/no) [Default = no]: " NEED_HTTP
if [[ "$NEED_HTTP" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    read -p "HTTP Host (default: localhost): " HTTP_HOST
    HTTP_HOST=${HTTP_HOST:-localhost}
    read -p "HTTP Port (default: random): " HTTP_PORT
    if [ -z "$HTTP_PORT" ]; then
        HTTP_PORT=$(( ( RANDOM % 64512 )  + 1024 ))
    fi
else
    HTTP_HOST=""
    HTTP_PORT="null"
fi

# Prompt for WS server
read -p "Do you want to add a WS Server? (yes/no) [Default = no]: " NEED_WS
if [[ "$NEED_WS" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    read -p "WS Host (default: localhost): " WS_HOST
    WS_HOST=${WS_HOST:-localhost}
    read -p "WS Port (default: random): " WS_PORT
    if [ -z "$WS_PORT" ]; then
        WS_PORT=$(( ( RANDOM % 64512 )  + 1024 ))
    fi
else
    WS_HOST=""
    WS_PORT="null"
fi

# Prompt for Message Queue
read -p "Do you want to add a Message Queue? (yes/no) [Default = no]: " NEED_MQ
if [[ "$NEED_MQ" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    MESSAGE_QUEUE="true"
else
    MESSAGE_QUEUE="false"
fi

# Infer service type (simple logic)
if [[ "$HTTP_HOST" != "" && "$WS_HOST" != "" && "$MESSAGE_QUEUE" == "true" ]]; then
    SERVICE_TYPE="WS_HTTP_QUEUE_MERGE"
elif [[ "$HTTP_HOST" != "" && "$WS_HOST" != "" ]]; then
    SERVICE_TYPE="NONE"
elif [[ "$HTTP_HOST" != "" && "$MESSAGE_QUEUE" == "true" ]]; then
    SERVICE_TYPE="HTTP_QUEUE_MERGE"
elif [[ "$WS_HOST" != "" && "$MESSAGE_QUEUE" == "true" ]]; then
    SERVICE_TYPE="NONE"
elif [[ "$HTTP_HOST" != "" ]]; then
    SERVICE_TYPE="HTTP_SERVER"
elif [[ "$WS_HOST" != "" ]]; then
    SERVICE_TYPE="WS_SERVER"
else
    SERVICE_TYPE="NONE"
fi

if [[ "$SERVICE_TYPE" == "NONE" ]]; then
    echo "No Service Available for the Following Type"
    exit 1
fi

# Paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PARENT_DIR="$(dirname "$SCRIPT_DIR")"
SERVICE_FOLDER_PATH="$PARENT_DIR/$SERVICE_FOLDER"
SERVICE_FILE_PATH="$SERVICE_FOLDER_PATH/$SERVICE_FILE"
SERVICES_JSON="$PARENT_DIR/services.json"
URL_MAPPING_JSON="$PARENT_DIR/ServiceURLMapping.json"
START_SH="$SCRIPT_DIR/start-server.sh"

# Create service folder and file
mkdir -p "$SERVICE_FOLDER_PATH"
touch "$SERVICE_FILE_PATH"
echo "Created $SERVICE_FILE_PATH"

# Update ServiceURLMapping.json
if [ "$HTTP_HOST" == "localhost" ]; then HTTP_HOST="127.0.0.1"; fi
if [ "$HTTP_PORT" != "null" ]; then
    SERVICE_URL="$HTTP_HOST:$HTTP_PORT"
    KEY="${SERVICE_NAME^^}_SERVICE"
    if [ ! -f "$URL_MAPPING_JSON" ]; then echo "{}" > "$URL_MAPPING_JSON"; fi
    jq --arg k "$KEY" --arg v "$SERVICE_URL" '. + {($k): $v}' "$URL_MAPPING_JSON" > "$URL_MAPPING_JSON.tmp" && mv "$URL_MAPPING_JSON.tmp" "$URL_MAPPING_JSON"
    echo "Updated $URL_MAPPING_JSON"
fi

# Update start-server.sh
if grep -q "#<ADD_SERVICE_START_HERE>" "$START_SH"; then
    sed -i "s|#<ADD_SERVICE_START_HERE>|.venv/bin/python3.12 $SERVICE_FOLDER/$SERVICE_FILE \& \n#<ADD_SERVICE_START_HERE>|" "$START_SH"
    echo "Updated $START_SH"
fi

# Update services.json (build JSON string in Bash, then append with jq)
SERVICE_HTTP_HOST_JSON=null
SERVICE_HTTP_PORT_JSON=null
SERVICE_WS_HOST_JSON=null
SERVICE_WS_PORT_JSON=null

if [[ "$HTTP_HOST" != "" && "$HTTP_PORT" != "null" ]]; then
    SERVICE_HTTP_HOST_JSON="\"$HTTP_HOST\""
    SERVICE_HTTP_PORT_JSON="$HTTP_PORT"
fi
if [[ "$WS_HOST" != "" && "$WS_PORT" != "null" ]]; then
    SERVICE_WS_HOST_JSON="\"$WS_HOST\""
    SERVICE_WS_PORT_JSON="$WS_PORT"
fi

SERVICE_JSON=$(cat <<EOF
{
    "ServiceLanguage": "Python",
    "ServiceName": "$SERVICE_NAME",
    "ServiceFolderName": "$SERVICE_FOLDER",
    "ServiceFileName": "$SERVICE_FILE",
    "ServiceHttpHost": $SERVICE_HTTP_HOST_JSON,
    "ServiceHttpPort": $SERVICE_HTTP_PORT_JSON,
    "ServiceWsHost": $SERVICE_WS_HOST_JSON,
    "ServiceWsPort": $SERVICE_WS_PORT_JSON,
    "ServiceMessageQueue": $MESSAGE_QUEUE,
    "ServiceType": "$SERVICE_TYPE"
}
EOF
)

if [ ! -f "$SERVICES_JSON" ]; then echo "[]" > "$SERVICES_JSON"; fi
jq ". += [$SERVICE_JSON]" "$SERVICES_JSON" > "$SERVICES_JSON.tmp" && mv "$SERVICES_JSON.tmp" "$SERVICES_JSON"
echo "Updated $SERVICES_JSON"

# Optionally, copy template and replace placeholders
TEMPLATE_PATH="$SCRIPT_DIR/ServiceTemplates/python/${SERVICE_TYPE}.txt"
if [ -f "$TEMPLATE_PATH" ]; then
    cp "$TEMPLATE_PATH" "$SERVICE_FILE_PATH"
    # Replace placeholders in the new file
    sed -i "s|{HTTP_SERVER_HOST}|'$HTTP_HOST'|g" "$SERVICE_FILE_PATH"
    sed -i "s|{HTTP_SERVER_PORT}|$HTTP_PORT|g" "$SERVICE_FILE_PATH"
    sed -i "s|{WS_SERVER_HOST}|'$WS_HOST'|g" "$SERVICE_FILE_PATH"
    sed -i "s|{WS_SERVER_PORT}|$WS_PORT|g" "$SERVICE_FILE_PATH"
    echo "Populated $SERVICE_FILE_PATH from template."
fi

echo "Service added successfully."
