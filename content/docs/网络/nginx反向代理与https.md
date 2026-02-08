---
title: nginx反向代理与https
type: docs
prev: docs/网络/免费ssl证书/
---


借助nginx，我们可以轻松实现反向代理和HTTPS功能，从而提升网站的安全性和性能。本文将介绍如何配置nginx以实现这些功能。

## 前置条件

拥有域名和 SSL 证书（可以参考[免费SSL证书](../免费ssl证书/)一文获取）。

## 1. 安装 nginx

在 Arch Linux 上，可以使用以下命令安装 nginx：

```bash
sudo pacman -S nginx
sudo systemctl enable --now nginx
```

## 2. 配置反向代理

### 2.1 修改 nginx.conf

打开 nginx.conf：

```bash
sudo nano /etc/nginx/nginx.conf
```

把自带的 server 配置注释掉，或者删除：

```nginx
# server {
#     listen       80;
#     server_name  localhost;
#     ...
# }
```

找到 `http { ... }`，确认里面包含这一行：

```nginx
include /etc/nginx/sites-enabled/*;
```

如果没有，加进去（放在 http 块最后即可）：

```nginx
http {
    ...
    include /etc/nginx/sites-enabled/*;
}
```

{{% details title="点击展开最终配置文件" closed="true" %}}

```nginx

#user http;
worker_processes  1;

#error_log  logs/error.log;
#error_log  logs/error.log  notice;
#error_log  logs/error.log  info;

#pid        logs/nginx.pid;


# Load all installed modules
include modules.d/*.conf;

events {
    worker_connections  1024;
}


http {
    include       mime.types;
    default_type  application/octet-stream;

    #log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
    #                  '$status $body_bytes_sent "$http_referer" '
    #                  '"$http_user_agent" "$http_x_forwarded_for"';

    #access_log  logs/access.log  main;

    sendfile        on;
    #tcp_nopush     on;

    #keepalive_timeout  0;
    keepalive_timeout  65;

    #gzip  on;

    # server {
    #     listen       80;
    #     server_name  localhost;

    #     #charset koi8-r;

    #     #access_log  logs/host.access.log  main;

    #     location / {
    #         root   /usr/share/nginx/html;
    #         index  index.html index.htm;
    #     }

    #     #error_page  404              /404.html;

    #     # redirect server error pages to the static page /50x.html
    #     #
    #     error_page   500 502 503 504  /50x.html;
    #     location = /50x.html {
    #         root   /usr/share/nginx/html;
    #     }

    #     # proxy the PHP scripts to Apache listening on 127.0.0.1:80
    #     #
    #     #location ~ \.php$ {
    #     #    proxy_pass   http://127.0.0.1;
    #     #}

    #     # pass the PHP scripts to FastCGI server listening on 127.0.0.1:9000
    #     #
    #     #location ~ \.php$ {
    #     #    root           html;
    #     #    fastcgi_pass   127.0.0.1:9000;
    #     #    fastcgi_index  index.php;
    #     #    fastcgi_param  SCRIPT_FILENAME  /scripts$fastcgi_script_name;
    #     #    include        fastcgi_params;
    #     #}

    #     # deny access to .htaccess files, if Apache's document root
    #     # concurs with nginx's one
    #     #
    #     #location ~ /\.ht {
    #     #    deny  all;
    #     #}
    # }


    # another virtual host using mix of IP-, name-, and port-based configuration
    #
    #server {
    #    listen       8000;
    #    listen       somename:8080;
    #    server_name  somename  alias  another.alias;

    #    location / {
    #        root   html;
    #        index  index.html index.htm;
    #    }
    #}


    # HTTPS server
    #
    #server {
    #    listen       443 ssl;
    #    server_name  localhost;

    #    ssl_certificate      cert.pem;
    #    ssl_certificate_key  cert.key;

    #    ssl_session_cache    shared:SSL:1m;
    #    ssl_session_timeout  5m;

    #    ssl_ciphers  HIGH:!aNULL:!MD5;
    #    ssl_prefer_server_ciphers  on;

    #    location / {
    #        root   html;
    #        index  index.html index.htm;
    #    }
    #}
    include /etc/nginx/sites-enabled/*;
}
```

{{% /details %}}

### 2.2 创建站点配置文件

创建站点配置文件：

```bash
sudo nano /etc/nginx/sites-available/my-site.conf
```

添加以下内容，替换 `example.com` 为你的域名，`9876` 为你想要代理的服务端口：

```nginx
server {
    listen 80;
    server_name example.com;

    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    http2 on;
    server_name example.com;

    ssl_certificate     /etc/nginx/ssl/example.com/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/example.com/key.pem;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers  HIGH:!aNULL:!MD5;

    location / {
        proxy_pass http://127.0.0.1:9876;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        proxy_http_version 1.1;
        proxy_buffering off;
    }
}
```

### 2.3 启用站点配置

创建符号链接以启用站点配置：

```bash
sudo ln -s /etc/nginx/sites-available/my-site.conf /etc/nginx/sites-enabled/
```

### 2.4 测试并重载 nginx
测试配置是否正确：

```bash
sudo nginx -t
```

如果没有错误，重载 nginx 以应用更改：

```bash
sudo systemctl reload nginx
```
