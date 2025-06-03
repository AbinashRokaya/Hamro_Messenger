from fastapi import FastAPI,WebSocket,WebSocketDisconnect,Depends
import uvicorn
from database.database import engine,Base
from route import friend_route,notification_route,message_route,websocket,media_route
import model
from auth import register,login
from fastapi.responses import HTMLResponse
from schemas.token_schema import AuthenticateUser
from route.message_route import send_message_from_sender
import asyncio
from auth.current_user import get_current_user
from fastapi.middleware.cors import CORSMiddleware
from uuid import UUID
from model.user_model import UserModel
import jwt
from uuid import UUID
from auth.jwt import SECRET_KEY, ALGORITHM
from schemas.token_schema import AuthenticateUser,TokenPayload
from database.database import get_db
import asyncio
app=FastAPI()

Base.metadata.create_all(bind=engine)
app.include_router(register.route)
app.include_router(login.route)
app.include_router(friend_route.route)
app.include_router(notification_route.route)
app.include_router(message_route.route)
app.include_router(media_route.route)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or your frontend origin like "http://localhost:3000"
    allow_credentials=True,
    allow_methods=["*"],  # Or ["GET", "POST", "OPTIONS", ...]
    allow_headers=["*"],
)


# class ConnectionManager:
#     def __init__(self):
#         self.active_connection:list[WebSocket]=[]

#     async def connection(self,websocket:WebSocket):
#         await websocket.accept()
#         self.active_connection.append(websocket)

#     def disconnect(self,websocket:WebSocket):
#         self.active_connection.remove(websocket)

#     async def send_personal_message(self,message:str,websocket:WebSocket):
#         await websocket.send_text(message)

#     async def broadcast(self,message:str):
#         for connection in self.active_connection:
#             await connection.send_text(message)

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[UUID, WebSocket] = {}

    async def connect(self, user_id: UUID, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user_id] = websocket
        print(f"User {user_id} connected.")

    def disconnect(self, user_id: UUID):
        if user_id in self.active_connections:
            del self.active_connections[user_id]
            print(f"User {user_id} disconnected.")

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def send_to_friend(self, friend_id: UUID, message: str):
        friend_ws = self.active_connections.get(friend_id)
        if friend_ws:
            try:
                await friend_ws.send_text(message)
            except Exception as e:
                print(f"Error sending message to friend {friend_id}: {e}")
                self.disconnect(friend_id)

    async def broadcast(self, message: str):
        for user_id, connection in self.active_connections.items():
            try:
                await connection.send_text(message)
            except Exception as e:
                print(f"Error broadcasting to user {user_id}: {e}")
                self.disconnect(user_id)


manager=ConnectionManager()

@app.get("/api/user/me")
async def get_current_user_info(current_user: AuthenticateUser = Depends(get_current_user)):
    return {"user_id": current_user.user_id, "username": current_user.username}

async def get_current_user_webscoket(websocket: WebSocket) -> AuthenticateUser:
    with get_db() as db:
        token = websocket.query_params.get("token")
        if not token:
            await websocket.close(code=1008)
            raise WebSocketDisconnect()

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            token_data=TokenPayload(**payload)
            authenticate_user=db.query(UserModel).filter(UserModel.email==token_data.sub).first()
            
            return authenticate_user
        except :
            await websocket.close(code=1008)
            raise WebSocketDisconnect()

@app.websocket("/ws/{friend_id}")
async def websocket_endpoint(websocket: WebSocket, friend_id: UUID,  current_user: AuthenticateUser = Depends(get_current_user_webscoket),):
    # await websocket.accept()

    # # Step 1: Extract token from query params
    # token = websocket.query_params.get("token")
    # if not token:
    #     await websocket.close(code=1008, reason="Authentication token missing")
    #     return

    # # Step 2: Decode and verify JWT
    # try:
    #     payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    #     token_data=TokenPayload(**payload)
      
    #     current_user = get_user_by_id(token_data.user_id)
    #     print(current_user)
    # except :
    #     await websocket.close(code=1008, reason="Invalid or expired token")
    #     return

    # # Step 3: Check if they are friends
    # if not friend_id:
    #     await websocket.close(code=1008, reason="You are not friends with this user")
    #     return

    # Step 4: Connect
    await manager.connect(websocket=websocket,user_id=current_user.user_id)

    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            asyncio.create_task(send_message_from_sender(sender_id=current_user.user_id,receiver_id=friend_id,message_text=data))
            await manager.send_to_friend(friend_id=friend_id, message=data)
            # await manager.broadcast(f"{current_user.username} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket,current_user.user_id)
        await manager.broadcast(f"{current_user.username} has left the chat")
# @app.websocket("/ws/{friend_id}")
# async def websocket_endpoint(websocket:WebSocket,friend_id:UUID):
  
#     await manager.connection(websocket)

#     try:


#         while True:
#             data=await websocket.receive_text()
            
#             # asyncio.create_task(send_message_from_sender(user_id=friend_id, message_value=data,sender_id=current_user.user_id))
#             await manager.send_personal_message(f"You wrote:{data}",websocket)
#             print(f"ws data:{data}")
#             await manager.broadcast(f"Client #{friend_id} says: {data}")
            

#     except WebSocketDisconnect:
#         manager.disconnect(websocket)
#         await manager.broadcast(f"clent #{friend_id} has left the chat")


if __name__=="__main__":
    uvicorn.run("main:app",host="127.0.0.1",port=8000,reload=True,loop="asyncio")