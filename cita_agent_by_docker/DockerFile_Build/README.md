## 编译镜像
```buildoutcfg
docker build -t cita_agent:by_cita-cli .
```
## 创建容器
```buildoutcfg
docker run -d --name="cita-agent_port1337" \
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
docker run -d --name="cita-agent_port1338" \
--pid="host" \
-p 2921:2921 \
-e Node="192.168.2.161:1338" \
-e OpenPort=2921 \
cita_agent:by_cita-cli
```
容器启动成功后，直接访问映射的端口即可，例如： http://192.168.2.161:2921/metrics
