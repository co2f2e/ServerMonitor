from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import psutil
import datetime
import platform
import socket
import uvicorn
import asyncio

app = FastAPI()

@app.websocket("/ws/status")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("WebSocket connection accepted")

    # 初始化上一次的网络数据
    net_io = psutil.net_io_counters()
    last_bytes_sent = net_io.bytes_sent
    last_bytes_recv = net_io.bytes_recv

    try:
        while True:
            await asyncio.sleep(1)  # 每秒采集一次

            # 获取服务器状态
            net_io = psutil.net_io_counters()
            bytes_sent_per_sec = net_io.bytes_sent - last_bytes_sent
            bytes_recv_per_sec = net_io.bytes_recv - last_bytes_recv

            # 更新上一次的数据
            last_bytes_sent = net_io.bytes_sent
            last_bytes_recv = net_io.bytes_recv

            status = {
                "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "hostname": socket.gethostname(),
                "system": platform.system(),
                "release": platform.release(),
                "cpu_percent": psutil.cpu_percent(interval=None),
                "memory": psutil.virtual_memory()._asdict(),
                "disk": psutil.disk_usage('/')._asdict(),
                "bytes_sent_per_sec": bytes_sent_per_sec,
                "bytes_recv_per_sec": bytes_recv_per_sec,
            }

            print(f"Sending status: {status}")  # 增加日志打印

            try:
                await websocket.send_json(status)
                print("Status sent")
            except WebSocketDisconnect:
                print("WebSocket disconnected")
                break  

    except Exception as e:
        print(f"Connection closed due to exception: {e}")
    finally:
        await websocket.close()
        print("Connection closed")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
