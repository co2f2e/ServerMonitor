#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import psutil
import uvicorn
import datetime
import platform
import socket

app = FastAPI()

# 跨域支持
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载模板文件夹
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/status")
async def get_status():
    return {
        "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "hostname": socket.gethostname(),
        "system": platform.system(),
        "release": platform.release(),
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory": {
            "total": round(psutil.virtual_memory().total / (1024**3), 2),
            "used": round(psutil.virtual_memory().used / (1024**3), 2),
            "percent": psutil.virtual_memory().percent,
        },
        "disk": {
            "total": round(psutil.disk_usage('/').total / (1024**3), 2),
            "used": round(psutil.disk_usage('/').used / (1024**3), 2),
            "percent": psutil.disk_usage('/').percent,
        },
        "net": {
            "bytes_sent": round(psutil.net_io_counters().bytes_sent / (1024**2), 2),
            "bytes_recv": round(psutil.net_io_counters().bytes_recv / (1024**2), 2),
        }
    }

if __name__ == "__main__":
    uvicorn.run("status_api:app", host="127.0.0.1", port=8000, reload=True)
