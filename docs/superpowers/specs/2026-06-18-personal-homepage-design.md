# 个人主页设计文档

**日期**：2026-06-18
**目标**：基于 typst 简历（`/home/nros/_XY/大学相关/简历/typst/`），为现有 Hugo + Hextra 站点（mirtith.github.io）编写个人主页。

## 背景

- 站点技术栈：Hugo + Hextra 主题（v0.11.1），通过 Hugo Modules 引入，推送 `main` 分支后 GitHub Actions 自动部署到 GitHub Pages。
- 现状：首页 `content/_index.md` 仅有两张卡片（博客 / 知识库）；`content/about.md` 为空占位页（`type: about`）。
- 简历主体：谢阳（Yang Xie），哈工大（深圳）控制科学与工程硕士在读（网络机器人与系统实验室 NRS），方向为机器人与具身智能（双臂操作、VLA、模仿学习）。简历含教育、三段实习（RoboSense / 华为 2012 / 百度）、竞赛、科研项目、技能。
- 简历照片：`/home/nros/_XY/大学相关/简历/typst/photo.png`（约 4MB）。

## 已确认的设计决策

| 维度 | 决策 |
|---|---|
| 页面位置 | 两者结合：首页加个人 Hero + 卡片入口；另建独立的精选「关于」页 |
| 内容深度 | 精选高亮（非全文搬运简历） |
| 联系方式 | 仅展示 GitHub、邮箱、实验室主页；**不展示手机号** |
| 照片 | 使用照片（首页头像 + 关于页共用，需压缩） |
| 语言 | 全中文（与站点 `zh-cn` 一致），姓名可附英文 |
| 实现方式 | 仅用 Hextra 原生 shortcode，不引入额外依赖 |

## 文件改动总览

| 文件 | 改动 |
|---|---|
| `content/_index.md` | 改为 `layout: hextra-home`，加入 Hero（头像 + 姓名 + 定位 + 按钮）与 feature 卡片 |
| `content/about/index.md` | **新建**（页面包），精选关于页正文 |
| `content/about/avatar.jpg` | **新建**，由 `photo.png` 压缩而来 |
| `content/about.md` | **删除**（空的旧占位页，被 `about/index.md` 取代） |
| `hugo.yaml` | 导航栏 `menu.main` 增加「关于」入口 |

## 详细设计

### 1. 首页 `content/_index.md`

- front matter：`layout: hextra-home`，保留 `title`、`toc: false`。
- 结构（自上而下）：
  1. 圆形头像：raw `<img>`（goldmark 已启用 `unsafe: true`），居中，引用 `about/avatar.jpg` 或站点可访问路径。
  2. `{{< hextra/hero-headline >}}`：`谢阳 / Yang Xie`
  3. `{{< hextra/hero-subtitle >}}`：一句话定位，例如「机器人与具身智能方向硕士在读 · 哈工大（深圳）」
  4. `{{< hextra/hero-button >}}` ×2：
     - `了解更多 →` → `link="about"`
     - `GitHub ↗` → `link="https://github.com/MirTITH"`
  5. `{{< hextra/feature-grid >}}` 内三张 `feature-card`：
     - 关于我 → `/about`
     - 博客 → `/blog`
     - 知识库 → `/docs`
- 说明：`hero-button` 仅在着陆页（`hextra-home`）内部使用，符合主题作者建议。

### 2. 关于页 `content/about/index.md`

普通内容页（页面包），front matter 含 `title: 关于`。正文按 markdown 标题分节：

1. **个人简介**：2–3 句，概括研究方向（具身智能、双臂操作、VLA / 模仿学习）、学校与实验室。
2. **教育经历**：
   - 哈工大（深圳）控制科学与工程硕士（2024–至今，NRS 实验室），学业奖学金特等奖。
   - 哈工大（深圳）自动化本科（2020–2024），综合排名 24/237，CET-6 537。
3. **精选经历**（仅取代表性条目，每条 1–3 行要点，非全文）：
   - 实习：RoboSense 速腾聚创（VLA 系统链路 / 双臂遥操作 / 控制延迟 150ms→35ms）；华为 2012 实验室（UMI 数据采集 + Diffusion Policy）。
   - 项目：具身智能双臂移动机器人（导师组科研平台核心软硬件）；本科毕设——复杂环境机械臂自主避障与抓取（实机抓取成功率 >80%）。
   - 竞赛：全国大学生智能车竞赛全国总决赛一等奖（一行点到）。
4. **技能**：分四类（编程语言 / 机器人开发 / 模型与算法 / 工程工具），列表呈现，可用少量 `{{< badge >}}` 点缀关键技术。
5. **联系方式**：GitHub（github.com/MirTITH）、邮箱（1023515576@qq.com）、实验室主页（nrs-lab.com）。**不含手机号**。用卡片或普通 markdown 链接（不使用 `hero-button`）。

### 3. 照片处理

- 源：`/home/nros/_XY/大学相关/简历/typst/photo.png`（约 4MB）。
- 目标：压缩为约 500px 宽的 `avatar.jpg`，体积 <150KB，放入 `content/about/`（页面包资源）。
- 工具：优先 ImageMagick（`magick` / `convert`），缺失时用 `ffmpeg` 兜底。
- 首页与关于页共用同一张图。首页通过可访问路径引用（如经 Hugo 处理或置于 `assets`/`static`，实现阶段确认引用路径正确）。

### 4. 导航与配置 `hugo.yaml`

`menu.main` 增加（放在「知识库」weight: 2 之后）：

```yaml
- name: 关于
  pageRef: /about
  weight: 3
```

现有 `Search`（weight 4）、`GitHub`（weight 5）顺序不变。

### 5. 语言与语气

全中文，姓名附英文；语气简洁、客观、专业，采用简历式陈述。

## 验收标准

- `hugo server` 本地启动无报错，首页与 `/about` 正常渲染。
- 首页显示头像、姓名、定位、按钮与三张卡片；按钮与卡片链接可达。
- 关于页五个分节内容完整、精炼，不含手机号。
- 导航栏出现「关于」入口并可跳转。
- 头像图片体积显著减小（<150KB），加载正常，无明显失真。
- 旧 `content/about.md` 已删除，无重复路由冲突。

## 不做的事（YAGNI）

- 不搬运简历全文（实习/竞赛/项目的每一条都列）。
- 不展示手机号、QQ 等隐私敏感信息。
- 不引入新主题、新 JS/CSS 依赖或自定义 layout 覆盖（除非实现阶段发现 Hextra 原生能力不足，再单独讨论）。
- 暂不做 PDF 简历下载入口、双语切换、动效等扩展（如需可后续单独立项）。
