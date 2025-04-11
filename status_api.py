from fastapi import FastAPI, WebSocket
import psutil
import datetime
import platform
import socket
import uvicorn

app = FastAPI()

@app.websocket("/ws/status")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()  # 接受 WebSocket 连接
    try:
        while True:
            # 获取服务器状态
            status = {
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
        await websocket.send_json(status)  # 向客户端发送状态数据
        await asyncio.sleep(5)  # 每5秒更新一次
    excetp Exception as e:
        print(f"WebSocket 断开: {e}")
    finally:
        await websocket.close()
if __name__ == "__main__":
    uvicorn.run("status_api:app", host="127.0.0.1", port=8000, reload=True)
