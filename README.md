# 🐑 Blog

**网站地址：** <https://mirtith.github.io>

> 基于 [Hugo](https://gohugo.io/) 构建，使用 [Hextra](https://imfing.github.io/hextra) 主题。  
> 推送到 `main` 分支后，GitHub Actions 会自动构建并部署到 GitHub Pages。

## 目录结构

网站内容均为 Markdown 文件，位于 `content` 目录下：

```
content/
├── _index.md  # 首页
├── about.md   # 关于
├── blog/      # 博客文章
└── docs/      # 知识库文档
```

## 本地预览

1. 安装依赖：

   ```bash
   # Arch Linux
   sudo pacman -S hugo go
   ```

2. 启动开发服务器：

   ```bash
   hugo server --buildDrafts --disableFastRender
   ```

3. 在浏览器中打开 <http://localhost:1313> 即可预览。

## 编辑现有内容

- **方法一**：直接编辑 `content` 目录下的 Markdown 文件
- **方法二**：点击网站右侧的 `在 GitHub 上编辑此页 →`

## 新建内容

- **方法一**：通过 Hugo 命令行工具快速创建新的 Markdown 模板：

    ```bash
    # 新建知识库文档
    hugo new content/docs/<目录>/<文章名>.md

    # 新建博客文章
    hugo new content/blog/<文章名>.md
    ```

    编辑生成的 Markdown 文件，记得将 `draft: true` 删除，否则文章不会在生产环境中显示。

- **方法二**：直接参考已有的 Markdown 文件，复制并修改内容来创建新的文章。

更多用法请参阅 [Hextra 文档](https://imfing.github.io/hextra/docs/guide/)。