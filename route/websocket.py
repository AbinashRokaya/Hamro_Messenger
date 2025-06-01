from fastapi import APIRouter,WebSocket,WebSocketDisconnect,Depends,HTTPException
from fastapi.responses import HTMLResponse
from auth.current_user import get_current_user
from schemas.token_schema import AuthenticateUser
from uuid import UUID
from sqlalchemy.orm import Session
from route.message_route import send_message_from_sender
from database.database import get_db
import asyncio
from typing import Annotated

route=APIRouter(
    prefix="/websocket",
    tags=["Webscoket"]
)


class ConnectionManager:
    def __init__(self):
        self.active_connection:list[WebSocket]=[]

    async def connection(self,websocket:WebSocket):
        await websocket.accept()
        self.active_connection.append(websocket)

    def disconnect(self,websocket:WebSocket):
        self.active_connection.remove(websocket)

    async def send_personal_message(self,message:str,websocket:WebSocket):
        await websocket.send_text(message)

    async def broadcast(self,message:str):
        for connection in self.active_connection:
            await connection.send_text(message)


manager=ConnectionManager()



@route.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket:WebSocket,client_id:int):
    await manager.connection(websocket)

    try:


        while True:
            data=await websocket.receive_text()
            asyncio.create_task(send_message_from_sender(user_id=friend_id, message_value=data,sender_id=current_user.user_id))
            
            await manager.send_personal_message(f"You wrote:{data}",websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}")
            

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"clent #{client_id} has left the chat")