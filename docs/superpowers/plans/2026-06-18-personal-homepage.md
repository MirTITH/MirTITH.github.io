# 个人主页 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 基于 typst 简历，为现有 Hugo + Hextra 站点新增个人主页：首页加入个人 Hero 与卡片入口，并新建一个独立的精选「关于」页。

**Architecture:** 纯内容层改动，仅使用 Hextra v0.11.1 原生 shortcode，不引入额外依赖。首页 `content/_index.md` 改用 `hextra-home` 布局；新建 `content/about/index.md` 承载精选简历；头像压缩后放在 `static/images/avatar.jpg`，供两页共用；`hugo.yaml` 增加「关于」导航入口。验证方式为 `hugo` 构建无报错 + grep 生成的 HTML。

**Tech Stack:** Hugo v0.163（extended）、Hextra 主题 v0.11.1、ImageMagick（`magick`）。

---

## File Structure

| 文件 | 责任 |
|---|---|
| `static/images/avatar.jpg` | 压缩后的个人头像，URL `/images/avatar.jpg`，首页与关于页共用 |
| `content/_index.md` | 站点首页（着陆页）：Hero + feature 卡片 |
| `content/about/index.md` | 关于页：精选简历正文 |
| `content/about.md` | **删除**（旧空占位页，与 `about/index.md` 路由冲突） |
| `hugo.yaml` | 导航栏 `menu.main` 增加「关于」入口 |

说明：头像放 `static/images/`（而非 spec 初稿的 `content/about/` 页面包），因为首页与关于页分属不同页面，全局 `static` 路径可被两页统一引用 `/images/avatar.jpg`，避免跨页面包资源引用问题。

---

### Task 1: 压缩并放置头像

**Files:**
- Create: `static/images/avatar.jpg`（由 `/home/nros/_XY/大学相关/简历/typst/photo.png` 压缩而来）

- [ ] **Step 1: 建立目录并压缩图片**

源图为 2890×3877 PNG（约 4MB）。缩放到宽 500px、quality 85、去除元数据，输出 JPEG。

Run:
```bash
cd /home/nros/Documents/MirTITH.github.io
mkdir -p static/images
magick "/home/nros/_XY/大学相关/简历/typst/photo.png" -resize 500x -strip -quality 85 static/images/avatar.jpg
```

- [ ] **Step 2: 验证产物尺寸与体积**

Run:
```bash
identify static/images/avatar.jpg && du -h static/images/avatar.jpg
```
Expected: 输出宽度为 500（高度按比例约 670），文件体积 < 150KB（典型 ~40–70KB）。若体积 ≥ 150KB，将 quality 降到 80 重试 Step 1。

- [ ] **Step 3: Commit**

```bash
git add static/images/avatar.jpg
git commit -m "添加个人主页头像（压缩自简历照片）"
```

---

### Task 2: 改造首页 `content/_index.md`

**Files:**
- Modify: `content/_index.md`（整体重写）

- [ ] **Step 1: 重写 `content/_index.md`**

完整写入以下内容（替换原有全部内容）：

```markdown
---
title: 🐑
layout: hextra-home
---

<div class="hx-mt-6 hx-mb-6" style="text-align: center;">
  <img src="/images/avatar.jpg" alt="谢阳" style="width: 160px; height: 160px; border-radius: 9999px; object-fit: cover; display: inline-block;" />
</div>

<div class="hx-mt-6 hx-mb-6">
{{< hextra/hero-headline >}}
  谢阳 / Yang Xie
{{< /hextra/hero-headline >}}
</div>

<div class="hx-mb-12">
{{< hextra/hero-subtitle >}}
  机器人与具身智能方向硕士在读 · 哈工大（深圳）
{{< /hextra/hero-subtitle >}}
</div>

<div class="hx-mb-6">
{{< hextra/hero-button text="了解更多 →" link="about" >}}
{{< hextra/hero-button text="GitHub ↗" link="https://github.com/MirTITH" >}}
</div>

{{< hextra/feature-grid >}}
  {{< hextra/feature-card
    title="关于我"
    subtitle="教育、实习、科研项目与技能"
    link="about"
  >}}
  {{< hextra/feature-card
    title="博客"
    subtitle="技术笔记与随笔"
    link="blog"
  >}}
  {{< hextra/feature-card
    title="知识库"
    subtitle="开发、Linux、网络等文档沉淀"
    link="docs"
  >}}
{{< /hextra/feature-grid >}}
```

- [ ] **Step 2: 构建站点**

Run:
```bash
cd /home/nros/Documents/MirTITH.github.io
hugo --cleanDestinationDir
```
Expected: 构建成功，无 ERROR；输出统计行（Pages 等）。首次运行可能下载 Hextra 模块。

- [ ] **Step 3: 验证首页渲染**

Run:
```bash
grep -c "谢阳" public/index.html
grep -o "/images/avatar.jpg" public/index.html | head -1
grep -c "hero-button\|hextra-hero" public/index.html
grep -c "了解更多\|关于我\|知识库" public/index.html
```
Expected: 第一行 ≥ 1（姓名出现）；第二行输出 `/images/avatar.jpg`（头像被引用）；第三、四行 ≥ 1（hero 与卡片渲染）。

- [ ] **Step 4: Commit**

```bash
git add content/_index.md
git commit -m "首页改用 hextra-home 布局，加入个人 Hero 与卡片入口"
```

---

### Task 3: 新建关于页 `content/about/index.md`

**Files:**
- Create: `content/about/index.md`
- Delete: `content/about.md`

- [ ] **Step 1: 删除旧的空占位页**

`content/about.md` 与新建的 `content/about/index.md` 会产生 `/about/` 路由冲突，先删除旧文件。

Run:
```bash
cd /home/nros/Documents/MirTITH.github.io
git rm content/about.md
```

- [ ] **Step 2: 创建 `content/about/index.md`**

完整写入以下内容：

```markdown
---
title: 关于
toc: false
---

## 个人简介

我是谢阳，哈尔滨工业大学（深圳）控制科学与工程硕士在读，隶属[网络机器人与系统实验室（NRS）](https://www.nrs-lab.com)。研究方向为机器人与具身智能，聚焦双臂灵巧操作、VLA 模型与模仿学习，关注从硬件控制到模型算法的完整系统链路。

## 教育经历

- **哈尔滨工业大学（深圳）** · 控制科学与工程 硕士（2024 – 至今）
  网络机器人与系统实验室（NRS）；学业奖学金特等奖。
- **哈尔滨工业大学（深圳）** · 自动化 本科（2020 – 2024）
  综合排名 24/237；大学英语六级 537 分。

## 精选经历

### 实习

- **RoboSense 速腾聚创** · 多模态大模型开发工程师（2025.03 – 2025.06）
  - 面向双臂灵巧作业场景，搭建从硬件控制到模型算法的 VLA 系统链路。
  - 重构机械臂驱动，将控制延迟从 150ms 降至 35ms；开发基于 ROS 2 与 MoveIt Servo 的双臂遥操作系统。
  - 完成 π₀ 等 VLA 模型的数据采集、训练、推理与部署。
- **华为技术有限公司** · 2012 实验室（2024.07 – 2025.01）
  - 基于 UMI 搭建手持夹爪数据采集系统，优化 ORB-SLAM3 工程实现。
  - 复现并优化 Diffusion Policy 模仿学习算法，完成机器人抓取任务验证。

### 科研与项目

- **具身智能双臂移动机器人**（2024.07 – 至今）
  搭建导师组具身智能科研平台，负责机械臂 / 灵巧手 ROS 2 驱动、运动控制与自主移动抓取算法。
- **复杂环境下机械臂自主避障与自主抓取**（本科毕业设计）
  独立完成驱动适配、手眼标定、运动学解算、避障规划与抓取位姿生成，实机平均抓取成功率超过 80%。

### 竞赛

- **全国大学生智能车竞赛** · 全国总决赛一等奖、RT-Thread 创新专项奖（2021）

## 技能

- **编程语言**：C / C++、Python
- **机器人开发**：机器人学、MPC、柔顺控制、运动规划、ROS / ROS 2、MoveIt、手眼标定
- **模型与算法**：π₀、π₀.₅、Diffusion Policy、ACT 等模仿学习与 VLA 模型的遥操作数据采集、训练与部署
- **工程工具**：Linux、Git、CMake、Docker、PyTorch、OpenCV、Pinocchio、SolidWorks

## 联系方式

- GitHub：<https://github.com/MirTITH>
- 邮箱：<1023515576@qq.com>
- 实验室主页：<https://www.nrs-lab.com>
```

- [ ] **Step 3: 构建站点**

Run:
```bash
cd /home/nros/Documents/MirTITH.github.io
hugo --cleanDestinationDir
```
Expected: 构建成功，无 ERROR。

- [ ] **Step 4: 验证关于页渲染且不含手机号**

Run:
```bash
test -f public/about/index.html && echo "about page built"
grep -c "个人简介\|精选经历\|联系方式" public/about/index.html
grep -c "RoboSense\|Diffusion Policy\|智能车" public/about/index.html
grep -c "151-1233-6950\|15112336950" public/about/index.html
```
Expected: 第一行打印 `about page built`；第二、三行 ≥ 1（分节与精选内容存在）；**第四行必须为 0**（不含手机号）。

- [ ] **Step 5: Commit**

```bash
git add content/about/index.md content/about.md
git commit -m "新建精选关于页，移除旧占位页"
```

---

### Task 4: 导航栏增加「关于」入口

**Files:**
- Modify: `hugo.yaml`（`menu.main` 区块）

- [ ] **Step 1: 在 `hugo.yaml` 的「知识库」菜单项后插入「关于」**

找到：
```yaml
    - name: 知识库
      pageRef: /docs
      weight: 2
```
在其后、`Search` 项之前插入：
```yaml
    - name: 关于
      pageRef: /about
      weight: 3
```
（现有 `Search` weight 4、`GitHub` weight 5 保持不变，顺序正确。）

- [ ] **Step 2: 构建站点**

Run:
```bash
cd /home/nros/Documents/MirTITH.github.io
hugo --cleanDestinationDir
```
Expected: 构建成功，无 ERROR。

- [ ] **Step 3: 验证导航栏出现「关于」并指向 /about**

Run:
```bash
grep -o 'href="[^"]*about[^"]*"[^>]*>关于' public/index.html | head -1
```
Expected: 输出一条包含 `关于` 且链接含 `about` 的导航项（确认菜单已渲染）。

- [ ] **Step 4: Commit**

```bash
git add hugo.yaml
git commit -m "导航栏增加「关于」入口"
```

---

### Task 5: 整体验收

**Files:** 无（仅验证）

- [ ] **Step 1: 全量构建并确认无警告/报错**

Run:
```bash
cd /home/nros/Documents/MirTITH.github.io
hugo --cleanDestinationDir --printPathWarnings 2>&1 | tail -20
```
Expected: 无 `ERROR`/`WARN` 关于重复路由；首页、`/about/`、`/blog/`、`/docs/` 均在输出中正常生成。

- [ ] **Step 2: 启动开发服务器做冒烟检查**

Run:
```bash
cd /home/nros/Documents/MirTITH.github.io
timeout 15 hugo server --disableFastRender >/tmp/hugo-server.log 2>&1 &
sleep 8
curl -s localhost:1313/ | grep -c "谢阳"
curl -s localhost:1313/about/ | grep -c "个人简介"
```
Expected: 两个 `curl` 各输出 ≥ 1（首页与关于页可访问且含预期内容）。检查完成后服务器随 `timeout` 自动退出。

- [ ] **Step 3: 确认无遗留未提交改动**

Run:
```bash
cd /home/nros/Documents/MirTITH.github.io
git status --short
```
Expected: 工作区干净（`public/` 在 `.gitignore` 中，不应出现；若出现则忽略，不提交构建产物）。

---

## Self-Review

**1. Spec coverage:**
- 首页 Hero + 卡片 → Task 2 ✓
- 独立精选关于页 → Task 3 ✓
- 联系方式仅 GitHub/邮箱/实验室主页、无手机号 → Task 3 内容 + Step 4 显式校验 ✓
- 使用照片（压缩） → Task 1 ✓
- 导航入口 → Task 4 ✓
- 删除旧 about.md → Task 3 Step 1 ✓
- 仅用 Hextra 原生 shortcode → 全程 ✓
- 验收标准（构建无错、页面可达、无手机号、头像 <150KB） → Task 1 Step 2 + Task 5 ✓

**2. Placeholder scan:** 无 TBD/TODO；每个代码步骤均给出完整内容与命令。

**3. Type/路径一致性:** 头像路径全程统一为 `static/images/avatar.jpg` → 引用 `/images/avatar.jpg`；关于页路由统一为 `/about/`（来自 `content/about/index.md`）；菜单 `pageRef: /about` 与之一致。

偏离 spec 说明：头像位置由 spec 初稿的 `content/about/avatar.jpg` 调整为 `static/images/avatar.jpg`，以支持首页与关于页共用，spec 中「实现阶段确认引用路径」已为此预留。
