from fastapi import FastAPI, WebSocket
import psutil
import datetime
import platform
import socket
import uvicorn
import asyncio

app = FastAPI()

@app.websocket("/ws/status")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()  # 接受 WebSocket 连接

    # 初始化上一次的网络数据
    net_io = psutil.net_io_counters()
    last_bytes_sent = net_io.bytes_sent
    last_bytes_recv = net_io.bytes_recv

    try:
        while True:
            await asyncio.sleep(1)  # 每秒采集一次

            net_io = psutil.net_io_counters()
            bytes_sent_per_sec = net_io.bytes_sent - last_bytes_sent
            bytes_recv_per_sec = net_io.bytes_recv - last_bytes_recv

            # 更新上一次的数据
            last_bytes_sent = net_io.bytes_sent
            last_bytes_recv = net_io.bytes_recv

            # 获取服务器状态
            status = {
                "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "hostname": socket.gethostname(),
                "system": platform.system(),
                "release": platform.release(),
                "cpu_percent": psutil.cpu_percent(interval=None),  # interval=None 更实时
                "memory": {
                    "total": round(psutil.virtual_memory().total / (1024 ** 3), 2),
                    "used": round(psutil.virtual_memory().used / (1024 ** 3), 2),
                    "percent": psutil.virtual_memory().percent,
                },
                "disk": {
                    "total": round(psutil.disk_usage('/').total / (1024 ** 3), 2),
                    "used": round(psutil.disk_usage('/').used / (1024 ** 3), 2),
                    "percent": psutil.disk_usage('/').percent,
                },
                "net": {
                    "bytes_sent_per_sec": round(bytes_sent_per_sec / 1024, 2),  # 单位 KB/s
                    "bytes_recv_per_sec": round(bytes_recv_per_sec / 1024, 2),  # 单位 KB/s
                }
            }
            
            # 确保连接仍然打开时才发送消息
            if websocket.client_state == WebSocket.CONNECTED:
                await websocket.send_json(status)

    except Exception as e:
        print(f"WebSocket 断开：{e}")
    finally:
        try:
            # 在关闭前确保连接是打开的
            if websocket.client_state == WebSocket.CONNECTED:
                await websocket.close()
        except Exception as e:
            print(f"关闭 WebSocket 连接失败: {e}")
            
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
