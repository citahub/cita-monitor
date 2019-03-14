## 编译镜像
```buildoutcfg
docker build -t cita_agent:by_cita-cli .
```
## 创建容器
```buildoutcfg
docker run -d --name="cita-agent_from_192.168.2.161:1337" \
--pid="host" \
-p 1920:1920 \
-e Node="192.168.2.161:1337" \
cita_agent:by_cita-cli
```
## Tips
Dockerfile 中已经默认定义了 exporter 的端口号为 1920；
如果想变更端口号，请添加`-e OpenPort=****`，并且修改 `-p ****:****`的端口映射
例如：
```buildoutcfg
docker run -d --name="cita-agent_from_192.168.2.161:1337" \
--pid="host" \
-p 1921:1921 \
-e Node="192.168.2.161:1337" \
-e OpenPort=1921
cita_agent:by_cita-cli
```
