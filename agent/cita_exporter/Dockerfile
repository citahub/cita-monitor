## 一个基础的 python 运行环境
FROM python:3
## 设置工作目录
WORKDIR /config
## 将当前系统文件夹内容复制到容器的 app 目录
ADD . /config
## 安装必要的依赖包
RUN pip3 install -r requirements.txt
RUN mv cita-cli /bin/cita-cli && chmod +x /bin/cita-cli
ENV PORT=1920
## 运行命令
CMD "python3" "cita_monitor_agent.py" "$NODE_IP_PORT" "$PORT" "$NODE_DIR"
