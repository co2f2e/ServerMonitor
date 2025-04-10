#!/bin/bash
clear
export LANG="en_US.UTF-8"
red='\033[0;31m'
green='\033[0;32m'
yellow='\033[0;33m'
blue='\033[0;36m'
nc='\033[0m'

red() {
	echo -e "${red}$1${nc}"
}

green() {
	echo -e "${green}$1${nc}"
}

yellow() {
	echo -e "${yellow}$1${nc}"
}

blue() {
	echo -e "${blue}$1${nc}"
}

PROJECT_DIR="/usr/local/ServerMonitor"
SERVICE_NAME="servermonitor"
clear

stop_and_disable_service() {
    green "停止并禁用服务 $SERVICE_NAME..."
    sudo systemctl stop $SERVICE_NAME.service
    sudo systemctl disable $SERVICE_NAME.service
}

remove_service_and_reload() {
    green "删除 systemd 服务文件..."
    sudo rm -f /etc/systemd/system/$SERVICE_NAME.service
    green "重新加载 systemd 配置..."
    sudo systemctl daemon-reload
}

remove_project() {
    green "删除 ServerMonitor 项目..."
    sudo rm -rf $PROJECT_DIR
}

    stop_and_disable_service
    remove_service_and_reload
    remove_project

    green "卸载完成！"
