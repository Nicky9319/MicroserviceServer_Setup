clear

sudo docker-compose down
sleep 1

sudo docker-compose up -d
sleep 10

cd ../


# Mention the Environment you want to start along with the Services
# Example: /home/Avatar/Avatar_Env/bin/python3.12 service_MainServer/mainServer.py &
#          /home/Avatar/Avatar_Env/bin/python3.12 service_LogService/loggingService.py 

# Example: ../.venv/bin/python3.12 service_MainServer/mainServer.py (When Trying to Run from Local venv)



.venv/bin/python3.12 service_MainService/main-service.py & 
#<ADD_SERVICE_START_HERE>
