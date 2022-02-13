from fastapi import FastAPI, Header, Response, status, Request, File, UploadFile
import aiomysql
import asyncio
from typing import *
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv
import os

load_dotenv()
host = os.environ.get("HOST")
port = int(os.environ.get("PORT"))
db = os.environ.get("DATABASE")
user = os.environ.get("USER")
password = os.environ.get("PASSWORD")

app = FastAPI()

@app.get("/")
async def main(request: Request, response: Response):
   response = RedirectResponse(url='/docs')
   return response

@app.get("/files")
async def files(request:Request, response: Response, authorization: str = Header(None)):
    print(request.headers)
    
    con = await aiomysql.connect(autocommit=True, host=host, port=port, db=db, user=user, password=password)
    c = await con.cursor()
    await c.execute("SELECT * from apikeys WHERE apikey='"+ str(authorization)+"'")
    keys = await c.fetchall()
    if len(keys) == 0:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"error": True, "message": "Invalid token has been passed"}
    await c.execute("SELECT * FROM files")
    fls = await c.fetchall()
    return {"message": fls}


@app.post("/upload")
async def upload(request: Request, response: Response, authorization: str = Header(None), file: str = Header(None), name: str = Header(None)):
    print(request.headers)

    con = await aiomysql.connect(autocommit=True, host=host, port=port, db=db, user=user, password=password)
    c = await con.cursor()
    await c.execute("SELECT * from apikeys WHERE apikey='" + str(authorization)+"'")
    keys = await c.fetchall()
    if len(keys) == 0:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"error": True, "message": "Invalid token has been passed"}
    await c.execute("INSERT into files (name, url) VALUES ('"+str(name)+"', '"+str(file)+"')")
    return len(file)
    

@app.get("/tags")
async def files(request: Request, response: Response, authorization: str = Header(None)):
    print(request.headers)

    con = await aiomysql.connect(autocommit=True, host=host, port=port, db=db, user=user, password=password)
    c = await con.cursor()
    await c.execute("SELECT * from apikeys WHERE apikey='" + str(authorization)+"'")
    keys = await c.fetchall()
    if len(keys) == 0:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"error": True, "message": "Invalid token has been passed"}
    await c.execute("SELECT * FROM tags")
    fls = await c.fetchall()
    return {"message": fls}
