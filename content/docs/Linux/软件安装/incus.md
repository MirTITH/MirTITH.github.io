---
title: Incus
type: docs
---

## 安装

看官方文档：<https://linuxcontainers.org/incus/docs/main/tutorial/first_steps>

## Troubleshooting

### Incus 和 Docker 同时安装时，Incus 容器上不了网

> 参考自：<https://linuxcontainers.org/incus/docs/main/howto/network_bridge_firewalld/#prevent-connectivity-issues-with-incus-and-docker>

因为 Docker 将全局的 FORWARD 策略设置为 DROP，导致 Incus 容器无法访问网络。推荐的解决方法为，修改 Docker 的配置，让它不要 drop 所有流量。具体方法如下：

1. 创建或编辑 Docker 的 daemon.json 文件：

   ```bash
   sudo mkdir -p /etc/docker
   sudo nano /etc/docker/daemon.json
   ```

2. 添加以下内容：

   ```json
   {
     "ip-forward-no-drop": true
   }
   ```

3. 重启电脑