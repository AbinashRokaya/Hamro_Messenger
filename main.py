from fastapi import FastAPI
import uvicorn
from database.database import engine,Base
from route import friend_route
import model
from auth import register,login


app=FastAPI()

Base.metadata.create_all(bind=engine)
app.include_router(register.route)
app.include_router(login.route)
app.include_router(friend_route.route)

@app.get("/")
def index():
    return {"surver is running"}



if __name__=="__main__":
    uvicorn.run("main:app",host="127.0.0.1",port=8000,reload=True,loop="asyncio")