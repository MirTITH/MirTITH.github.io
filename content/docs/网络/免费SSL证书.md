---
title: 免费SSL证书
type: docs
prev: docs/网络/ddns/
next: docs/网络/nginx反向代理与https/
---

## 获取免费SSL证书

这里使用 [acme.sh](https://github.com/acmesh-official/acme.sh) 脚本来申请免费的 SSL 证书。

对于不在公网的服务器，可以使用 DNS 验证的方式来申请证书。这种方式要求你添加一条指定的 DNS 记录以证明域名确实属于自己，在验证完成后可以删除这条记录。为了自动化这个过程（由 acme.sh 实现），需要域名提供商的 API 访问权限。

对于阿里云域名，可以创建一个仅拥有 DNS 操作权限的 RAM 用户，然后使用这个用户的 AccessKey 来实现自动化 DNS 验证。方法请参考 [基于阿里云 AccessKey 的 DDNS](../ddns/#基于阿里云-accesskey-的-ddns)。

得到 AccessKey 后，按照以下步骤操作：

### 1. 安装 acme.sh

acme.sh 依赖 cronie 服务来定时续签证书，先安装 cronie：

```bash
# Arch Linux
sudo pacman -S cronie
```

然后安装 acme.sh，方法如下：

```bash
git clone https://gitee.com/neilpang/acme.sh.git
cd acme.sh
# 以 root 用户安装
sudo su
./acme.sh --install -m my@example.com
```

> [!NOTE] 
> 虽然官网表示*普通用户和 root 用户都可以安装使用*，但**建议以 root 用户安装**，原因如下：
> - **更安全**：acme.sh 缓存的 AccessKey 和得到的证书文件会存放在家目录下。如果以 root 用户安装，其他用户无法访问，降低泄露风险。
> - **避免权限问题**：证书通常需要安装到系统目录（如 /etc/nginx/ssl/），然后执行需要 root 权限的命令（如 `systemctl reload nginx`）。以 root 用户运行 acme.sh 可以避免权限问题。

邮箱可以不填。GPT 说：
> 这个 email 是用来作为 ACME 账户的联系邮箱，这个邮箱会被注册到 ACME 证书颁发机构（如 Let's Encrypt / ZeroSSL），作为你的证书账户邮箱，用途包括：
> 1. **证书到期提醒**：当你的证书即将到期时，证书颁发机构会发送提醒邮件到这个邮箱，提示你续签证书。
> 2. **证书异常 / 安全警告通知**：例如：私钥泄露风险、证书被吊销、签发异常
> 3. **账户恢复 / 合规通知**：例如 ACME 账户变更、服务条款更新、CA 合规提醒

上面的脚本会将 acme.sh 安装到 `~/.acme.sh/` 目录下，但似乎没有自动添加到系统 PATH 中。因此后面使用绝对路径。

### 2. 申请证书

> [!NOTE] 以下命令均需以 root 用户运行

```bash
# 假设你的域名是 example.com，托管在阿里云
export Ali_Key="<key>"
export Ali_Secret="<secret>"
export MY_DOMAIN="example.com"
~/.acme.sh/acme.sh --issue --dns dns_ali -d "$MY_DOMAIN" -d "*.$MY_DOMAIN"
```

acme.sh 默认使用的 CA 机构是 ZeroSSL，该机构需要提供邮箱（在安装 acme.sh 时已指定）。也可以使用 Let's Encrypt，这个不需要提供邮箱：

```bash
~/.acme.sh/acme.sh --issue --server letsencrypt --dns dns_ali -d "$MY_DOMAIN" -d "*.$MY_DOMAIN"
```

申请完成后，acme.sh 会记住这些信息，后续续签时不需要再提供 AccessKey。可以删除 .bash_history 中的 Ali_Key 和 Ali_Secret 变量，防止泄露。

### 3. 为 nginx 安装证书

首先安装 nginx：

```bash
# Arch Linux
sudo pacman -S nginx
sudo systemctl enable --now nginx
```

> [!NOTE] 以下命令均需以 root 用户运行

```bash
mkdir -p /etc/nginx/ssl/$MY_DOMAIN

~/.acme.sh/acme.sh --install-cert -d "$MY_DOMAIN" \
--key-file       /etc/nginx/ssl/$MY_DOMAIN/key.pem  \
--fullchain-file /etc/nginx/ssl/$MY_DOMAIN/cert.pem \
--reloadcmd     "systemctl reload nginx"
```

这样，证书和私钥会被安装到 `/etc/nginx/ssl/example.com/` 目录下，并且在续签后会自动重载 nginx。

