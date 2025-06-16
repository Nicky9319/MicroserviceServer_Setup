import asyncio

from fastapi import FastAPI, Response, Request
from fastapi.middleware.cors import CORSMiddleware

import uvicorn

import asyncio
import aio_pika


import sys
import os

from dotenv import load_dotenv
load_dotenv()




class HTTP_SERVER():
    def __init__(self, httpServerHost, httpServerPort, httpServerPrivilegedIpAddress=["127.0.0.1"], data_class_instance=None):
        self.app = FastAPI()
        self.host = httpServerHost
        self.port = httpServerPort

        self.privilegedIpAddress = httpServerPrivilegedIpAddress

        #<HTTP_SERVER_CORS_ADDITION_START>
        self.app.add_middleware(CORSMiddleware, allow_origins=["*"],allow_credentials=True,allow_methods=["*"],allow_headers=["*"],)
        #<HTTP_SERVER_CORS_ADDITION_END>

        self.data_class = data_class_instance  # Reference to the Data class instance

    async def configure_routes(self):

        #<HTTP_SERVER_API_{/api/sample/}_START>

        #<HTTP_SERVER_ENDPOINT_{/api/sample/}_START>
        @self.app.get("/api/sample/")
        #<HTTP_SERVER_ENDPOINT_{/api/sample/}_END>

        #<HTTP_SERVER_FUNCTION_{/api/sample/}_START>
        async def get_api_sample():
            print("Running Through Someone Else")
            return {"message": "Hello World"}
        #<HTTP_SERVER_FUNCTION_{/api/sample/}_END>

        #<HTTP_SERVER_API_{/api/sample/}_END>

        #<HTTP_SERVER_NEW_API_START>
        #<HTTP_SERVER_NEW_API_END>

    async def run_app(self):
        config = uvicorn.Config(self.app, host=self.host, port=self.port)
        server = uvicorn.Server(config)
        await server.serve()

class Data():
    def __init__(self):
        self.value = None

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value

class Service():
    def __init__(self, httpServer = None):
        self.httpServer = httpServer

    async def startService(self):
        await self.httpServer.configure_routes()
        await self.httpServer.run_app()

        
async def start_service():
    dataClass = Data()

    #<HTTP_SERVER_INSTANCE_INTIALIZATION_START>

    #<HTTP_SERVER_PORT_START>
    httpServerPort = 8080
    #<HTTP_SERVER_PORT_END>

    #<HTTP_SERVER_HOST_START>
    httpServerHost = "127.0.0.1"
    #<HTTP_SERVER_HOST_END>

    #<HTTP_SERVER_PRIVILEGED_IP_ADDRESS_START>
    httpServerPrivilegedIpAddress = ["127.0.0.1"]
    #<HTTP_SERVER_PRIVILEGED_IP_ADDRESS_END>

    http_server = HTTP_SERVER(httpServerHost=httpServerHost, httpServerPort=httpServerPort, httpServerPrivilegedIpAddress=httpServerPrivilegedIpAddress, data_class_instance=dataClass)
    #<HTTP_SERVER_INSTANCE_INTIALIZATION_END>

    service = Service(http_server)
    await service.startService()

if __name__ == "__main__":
    asyncio.run(start_service())
