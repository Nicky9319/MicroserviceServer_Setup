import socketio
from aiohttp import web
import asyncio

import asyncio
from fastapi import FastAPI, Response, Request
import uvicorn

import asyncio
import aio_pika
import json
import time


import sys
import os

from dotenv import load_dotenv
load_dotenv()


sys.path.append(os.path.join(os.path.dirname(__file__), "../ServiceTemplates/Basic"))


from HTTP_SERVER import HTTPServer
from MESSAGE_QUEUE import MessageQueue
from WS_SERVER import WebSocketServer


from fastapi.middleware.cors import CORSMiddleware


class Service:
    def __init__(self, wsServerHost, wsServerPort, httpServerHost, httpServerPort):
        self.messageQueue = MessageQueue("amqp://guest:guest@localhost/","/")
        self.httpServer = HTTPServer(httpServerHost, httpServerPort)
        self.wsServer = WebSocketServer(wsServerHost, wsServerPort)
        self.privilegedIpAddress = {"127.0.0.1"}


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
    

    async def ConfigureWSserverMethods(self):
    # Boilerplate Setup for the Ws Server
        @self.wsServer.sio.event
        async def connect(sid, environ , auth=None):
            print(f"A New User with ID {sid} Connected")

    
        @self.wsServer.sio.event
        async def disconnect(sid):
            print(f'Client {sid} disconnected')
        
        
        @self.wsServer.sio.on("GET_SID")
        async def get_sid(sid):
            return sid
    
    async def startService(self):
        await self.messageQueue.InitializeConnection()
        # How to Add a Queue and Map it to a Callback Function
        await self.messageQueue.AddQueueAndMapToCallback("queue1", self.sample_callback_1)
        
        await self.messageQueue.BoundQueueToExchange()
        await self.messageQueue.StartListeningToQueue()

        await self.ConfigureWSserverMethods()
        await self.wsServer.start()

        await self.ConfigureAPIRoutes()
        await self.httpServer.run_app()

async def start_service():
    service = Service('127.0.0.1',6000, '127.0.0.1', 8000)
    await service.startService()

if __name__ == "__main__":
    asyncio.run(start_service())