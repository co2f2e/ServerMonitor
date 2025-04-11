<h1 align="center">
  ServerMonitor
</h1>
ServerMonitor 是一个简单的 Web 服务，用于监控服务器状态。

<hr>

## NGINX配置
```bash
    location /monitor/ {
        alias /usr/local/ServerMonitor/templates/;
        index index.html;
        try_files $uri $uri/ /monitor/index.html;
    }
    location /ws/ {
        proxy_pass http://127.0.0.1:8000/ws/;  # 直接把请求转发到你的 FastAPI 服务器
        proxy_http_version 1.1;  # WebSocket 
        proxy_set_header Upgrade $http_upgrade;  
        proxy_set_header Connection "upgrade";  
        proxy_set_header Host $host;
    }
```
## 安装
```bash
bash <(curl -Ls https://raw.githubusercontent.com/co2f2e/ServerMonitor/main/install_servermonitor.sh)
```
## 卸载
```bash
bash <(curl -Ls https://raw.githubusercontent.com/co2f2e/ServerMonitor/main/uninstall_servermonitor.sh)
```
### 服务管理命令
| 操作         | 命令                                                        |
|--------------|-------------------------------------------------------------|
| 启动服务     | ```sudo systemctl start servermonitor```                      |
| 停止服务     | ```sudo systemctl stop servermonitor```                       |
| 重启服务     | ```sudo systemctl restart servermonitor```                    |
| 查看状态     | ```sudo systemctl status servermonitor```                     |
| 查看日志     | ```sudo journalctl -u servermonitor -f```                     |
| 开机自启动   | ```sudo systemctl enable servermonitor```                     |
| 关闭开机启动 | ```sudo systemctl disable servermonitor```                    |
## 访问
`https://域名/monitor/`
## 测试环境
* Debian12
* NGINX
* SSL
