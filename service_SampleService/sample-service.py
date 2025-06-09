import asyncio
from fastapi import FastAPI, Response, Request
import uvicorn

import asyncio
import aio_pika


import sys
import os

from dotenv import load_dotenv
load_dotenv()

sys.path.append(os.path.join(os.path.dirname(__file__), "../ServiceTemplates/Basic"))


from HTTP_SERVER import HTTPServer
from MESSAGE_QUEUE import MessageQueue

from fastapi.middleware.cors import CORSMiddleware

class Service():
    def __init__(self,httpServerHost, httpServerPort):
        self.messageQueue = MessageQueue("amqp://guest:guest@localhost/","/")
        self.httpServer = HTTPServer(httpServerHost, httpServerPort)

        # How to Declare Priviledged Ip Address to Restrict the API hits.
        self.privilegedIpAddress = {"127.0.0.1"}

        # How to Add Cors to an Http Server
        self.httpServer.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # How to create a CallBack Function for a particular Queue
    async def sample_callback_1(self, message: aio_pika.IncomingMessage):
        msg = message.body.decode()
        print("Smaple Callback Function 1 Message : " , msg)
    
    async def ConfigureAPIRoutes(self):
        # How to Make a Single Simple Endpoint
        @self.httpServer.app.get("/")
        async def read_root():
            print("Running Through Someone Else")
            return {"message": "Hello World"}
        
        # How to Make a Restricted Endpoint but Limited privileges to Certain Ip Addresses Only.
        @self.httpServer.app.get("/restricted_endpoint")
        async def restricted_endpoint(request: Request):
            client_ip = request.client.host
            if client_ip not in self.privilegedIpAddress:
                return Response(status_code=403, content="Forbidden")
            return {"message": "This is a restricted endpoint accessible only to privileged IPs."}
    

    async def startService(self):
        # await self.messageQueue.InitializeConnection()

        # # How to Add a Queue and Map it to a Callback Function
        # await self.messageQueue.AddQueueAndMapToCallback("sample-queue", self.sample_callback_1)
        
        # await self.messageQueue.BoundQueueToExchange()
        # await self.messageQueue.StartListeningToQueue()

        await self.ConfigureAPIRoutes()
        await self.httpServer.run_app()

        
async def start_service():
    service = Service('127.0.0.1', 8080)
    await service.startService()

if __name__ == "__main__":
    asyncio.run(start_service())
