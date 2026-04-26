---
title: SSH
type: docs
---

## 安装服务端

### Windows

参考：<https://cloud.tencent.com/developer/article/1611035>

### Linux

```bash
sudo apt install openssh-server
```

## 启动与状态

### Windows

```powershell
Start-Service sshd
```

### Linux

```bash
sudo service ssh start
sudo service ssh restart
sudo service ssh status
```

## 免密登录

以下操作在客户端执行：

```bash
# 检查是否已有密钥
ls ~/.ssh

# 如果没有密钥，生成一对 ed25519 密钥
ssh-keygen -t ed25519 -C "your_email@example.com"

# 将公钥上传到服务器
ssh-copy-id -i ~/.ssh/id_ed25519.pub root@IP
```

## 目录与权限

- `~/.ssh` 目录建议权限为 `700`
- `authorized_keys` 和私钥文件建议权限为 `600`
- 公钥文件通常为 `644`
- 服务端配置与主机密钥位于 `/etc/ssh`

## 端口转发

### 常用参数

- `-f`：在后台执行
- `-N`：不执行远程命令，只做转发
- `-R`：远程端口转发
- `-L`：本地端口转发
- `-D`：动态端口转发（SOCKS 代理）
- `-C`：启用压缩
- `-p`：指定 SSH 端口

### 远程端口转发

```bash
ssh -R [监听接口:]监听端口:目标主机:目标端口 username@hostname
```

场景示例：A 为公网机器，B 为内网机器。若想通过访问 A 的端口来访问 B 上的服务，可以在 B 上执行：

```bash
ssh -NfR A_port:localhost:B_port A_username@A_IP -p 22
```

如果终端被占用，可改用：

```bash
nohup ssh -NfR A_port:localhost:B_port A_username@A_IP -p 22
```

效果：访问 A 的 `A_port`，等价于访问 B 的 `B_port`。

注意事项：

- 在 A 的 `/etc/ssh/sshd_config` 中启用 `GatewayPorts yes`
- 确保 A 的防火墙已放行对应端口

### 本地端口转发

```bash
ssh -L [监听接口:]监听端口:目标主机:目标端口 username@hostname
```

#### 主机 A 通过主机 B 访问主机 C

```bash
ssh -NfL A_port:C_ip:C_port B_user@B_ip -p 22
```

效果：访问 A 的 `A_port`，等价于访问 C 的 `C_port`。

#### 主机 A 访问主机 B 上的服务

```bash
ssh -NfL A_port:localhost:B_port B_user@B_ip -p 22
```

或：

```bash
ssh -NfL A_port:B_ip:B_port B_user@B_ip -p 22
```

### 动态端口转发

```bash
ssh -ND [监听接口:]监听端口 username@hostname
```

这会在本地创建一个 SOCKS 代理。应用只要把代理指向该端口，就能通过 SSH 隧道访问远端网络。

### 链式端口转发

本地端口转发和远程端口转发可以组合使用。例如：A 在公司内网，B 在家里，C 是公网云主机。想让 B 访问 A 上的服务，可以这样做：

在 B 上登录 C，并把 B 的 `3000` 转发到 C 的 `2000`：

```bash
ssh -L localhost:3000:localhost:2000 root@C_IP
```

在 A 上登录 C，并把 C 的 `2000` 转发到 A 的 `3000`：

```bash
ssh -R localhost:2000:localhost:3000 root@C_IP
```

这样 B 访问 `http://localhost:3000`，就等价于访问 A 上的 `3000` 服务。

## autossh

前提：已经能够免密登录服务器。

```bash
sudo apt install autossh
autossh -M 8888 -NCfR 1111:localhost:22 -o ServerAliveInterval=60 user@公网IP -p 22
```

`autossh` 会定期探活并在连接断开后自动重连，适合长期保持 SSH 隧道。

## 参考资料

- <https://zhuanlan.zhihu.com/p/94871997>
- <https://blog.csdn.net/dliyuedong/article/details/49804825>
- <https://zhuanlan.zhihu.com/p/148825449>
- <https://zhuanlan.zhihu.com/p/26547381>