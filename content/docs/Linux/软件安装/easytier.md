---
title: EasyTier
type: docs
---

## Ubuntu 24.04 安装 EasyTier

### 1. 安装依赖

```bash
sudo apt update
sudo apt install -y curl unzip
```

### 2. 安装 EasyTier

```bash
wget -O /tmp/easytier.sh "https://raw.githubusercontent.com/EasyTier/EasyTier/main/script/install.sh" && sudo bash /tmp/easytier.sh install --gh-proxy https://ghfast.top/
```

### 3. 修改配置

```bash
sudo mv /opt/easytier/config/default.conf /opt/easytier/config/default.conf.bak
sudo nano /opt/easytier/config/default.conf
```

写入以下内容（将 `<你的服务器公网IP>`、`<你的网络名称>`、`<你的网络密钥>` 替换为自己的）：

```toml
dhcp = true
# routes = [] # 如果不希望在本机添加其他主机子网代理网段的路由，可以把这个注释去掉
listeners = ["tcp://0.0.0.0:11010", "udp://0.0.0.0:11010"]

[[peer]]
uri = "tcp://<你的服务器公网IP>:11010"

[network_identity]
network_name = "<你的网络名称>"
network_secret = "<你的网络密钥>"

[flags]
enable_encryption = true
accept_dns = true
```

### 4. 启动服务

```bash
sudo systemctl enable easytier@default
sudo systemctl restart easytier@default
```

检查运行状态：

```bash
sudo systemctl status easytier@default
easytier-cli node
easytier-cli peer
```

### 5. 允许 SSH 访问

如果尚未安装 SSH 服务：

```bash
sudo apt install -y openssh-server
sudo systemctl enable --now ssh
```

## CachyOS 安装 EasyTier

```bash
paru -S easytier
```

然后配置 `/etc/easytier/config.toml`（内容与 Ubuntu 相同，替换为上面提到的占位符对应的实际值），再启动服务：

```bash
sudo systemctl enable --now easytier@default
sudo systemctl status easytier@default
```
