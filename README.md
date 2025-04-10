## NGINX配置
```bahs
    location /monitor/ {
        alias /usr/local/server_monitor/templates/;
        index index.html;
        try_files $uri $uri/ /monitor/index.html;    
    }
    location /monitor/api/ {
       proxy_pass http://127.0.0.1:8000/api/;
       proxy_set_header Host $host;
       proxy_set_header X-Real-IP $remote_addr;
       proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
       proxy_set_header X-Forwarded-Proto $scheme;
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
