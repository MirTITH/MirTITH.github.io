# 🐑's Blog

网站链接：<https://mirtith.github.io>

## 说明

网站基于 [Hugo](https://gohugo.io/) 静态网站生成器构建，使用 [Hextra 主题](https://imfing.github.io/hextra)。

文章由 Markdown 编写，位于 `content` 目录下。  

## 本地运行

安装 Hugo, Go：

```bash
# Arch Linux
sudo pacman -S hugo go
```

然后在项目根目录运行：

```bash
hugo server --buildDrafts --disableFastRender
```

浏览器打开 <http://localhost:1313> 即可预览网站。

## 创建新文章

在项目根目录运行：

```bash
# 添加新知识库文档
hugo new content/docs/目录/文章名.md

# 添加新博客文章
hugo new content/blog/文章名.md
```
然后编辑生成的 Markdown 文件即可。

更多指南，请参考 [Hextra 主题文档](https://imfing.github.io/hextra/docs/guide/)。