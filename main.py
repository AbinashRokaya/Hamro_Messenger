from fastapi import FastAPI,WebSocket,WebSocketDisconnect,Depends
import uvicorn
from database.database import engine,Base
from route import friend_route,notification_route,message_route,websocket
import model
from auth import register,login
from fastapi.responses import HTMLResponse
from schemas.token_schema import AuthenticateUser
from route.message_route import send_message_from_sender
import asyncio
from auth.current_user import get_current_user
from fastapi.middleware.cors import CORSMiddleware
from uuid import UUID


app=FastAPI()

Base.metadata.create_all(bind=engine)
app.include_router(register.route)
app.include_router(login.route)
app.include_router(friend_route.route)
app.include_router(notification_route.route)
app.include_router(message_route.route)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or your frontend origin like "http://localhost:3000"
    allow_credentials=True,
    allow_methods=["*"],  # Or ["GET", "POST", "OPTIONS", ...]
    allow_headers=["*"],
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

@app.get("/api/user/me")
async def get_current_user_info(current_user: AuthenticateUser = Depends(get_current_user)):
    return {"user_id": current_user.user_id, "username": current_user.username}

@app.websocket("/ws/{friend_id}")
async def websocket_endpoint(websocket:WebSocket,friend_id:UUID):
  
    await manager.connection(websocket)

    try:


        while True:
            data=await websocket.receive_text()
            
            # asyncio.create_task(send_message_from_sender(user_id=friend_id, message_value=data,sender_id=current_user.user_id))
            await manager.send_personal_message(f"You wrote:{data}",websocket)
            print(f"ws data:{data}")
            await manager.broadcast(f"Client #{friend_id} says: {data}")
            

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"clent #{friend_id} has left the chat")


if __name__=="__main__":
    uvicorn.run("main:app",host="127.0.0.1",port=8000,reload=True,loop="asyncio")