# 首页居中布局美化 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将首页 `content/_index.md` 的 Hero 区改为居中、卡片改为一行三列，修复左对齐失衡与"2+1"卡片留白。

**Architecture:** 纯内容层改动，仅改 `content/_index.md` 一个文件。用 `width:100% + text-align:center` 容器包裹头像/姓名/副标题以抵消 Hextra home 布局的 `items-start` 左对齐；姓名/副标题用居中 `<h1>`/`<p>` 替代无居中参数的 `hero-headline`/`hero-subtitle` shortcode；`feature-grid` 加 `cols="3"`。结构检查由实现方完成，最终视觉由用户在浏览器确认。

**Tech Stack:** Hugo v0.163（extended）、Hextra 主题 v0.11.1。

---

## File Structure

| 文件 | 责任 |
|---|---|
| `content/_index.md` | 首页：Hero 区居中 + 卡片 `cols="3"` |

---

### Task 1: 重写首页 _index.md 为居中布局

**Files:**
- Modify: `content/_index.md`（整体重写）

- [ ] **Step 1: 整体重写 `content/_index.md`**

完整写入以下内容（替换原有全部内容）：

```markdown
---
title: 🐑
layout: hextra-home
---

<div style="width: 100%; text-align: center;" class="hx-mt-6">
  <img src="/images/avatar.jpg" alt="谢阳"
       style="width: 160px; height: 160px; border-radius: 9999px; object-fit: cover; display: inline-block;" />
  <h1 style="margin-top: 1rem; font-size: 2.5rem; font-weight: 800; line-height: 1.2;">谢阳 / Yang Xie</h1>
  <p style="margin-top: 0.5rem; font-size: 1.125rem; color: #6b7280;">机器人与具身智能方向硕士在读 · 哈工大（深圳）</p>
</div>

{{< hextra/feature-grid cols="3" >}}
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
hugo --cleanDestinationDir 2>&1 | grep -i error || echo "BUILD CLEAN"
```
Expected: `BUILD CLEAN`（仅可能出现既有的 Hextra deprecation WARN，无 ERROR）。

- [ ] **Step 3: 结构检查 —— 居中容器、三列、无按钮残留**

Run:
```bash
cd /home/nros/Documents/MirTITH.github.io
echo "=== 姓名/副标题在居中容器内（text-align:center 与姓名同段出现）==="
python3 - <<'PY'
html = open('public/index.html', encoding='utf-8').read()
i = html.find('谢阳', html.find('</head>'))
seg = html[i-300:i+260]
print("center container:", 'text-align: center' in seg)
print("h1 present:", '<h1' in seg)
print("subtitle present:", '机器人与具身智能' in html)
print("avatar referenced:", '/images/avatar.jpg' in html)
PY
echo "=== 三列：feature-grid 列变量/类 ==="
grep -oE 'hextra-feature-grid-cols:\s*3|--hextra-feature-grid-cols:3|grid-cols-3' public/index.html | head -1
grep -oE 'class="hextra-feature-grid[^"]*"' public/index.html
echo "=== 无按钮残留（应为 0）==="
grep -c "hero-button\|了解更多" public/index.html
```
Expected:
- `center container: True`、`h1 present: True`、`subtitle present: True`、`avatar referenced: True`。
- 第二组：输出含 `3` 的列变量或 `grid-cols-3`（确认 `cols="3"` 生效）；并打印 feature-grid 的 class 串。
- `无按钮残留` 计数为 `0`。

注：若 `cols="3"` 通过 inline `style="--hextra-feature-grid-cols:3"` 而非 class 体现，上面第一条 grep 会命中该变量；两条 grep 任一命中即视为通过。

- [ ] **Step 4: Commit**

```bash
cd /home/nros/Documents/MirTITH.github.io
git add content/_index.md
git commit -m "首页改为居中布局，卡片一行三列"
```

---

### Task 2: 本地预览供用户确认视觉

**Files:** 无（仅启动预览 + 用户确认）

- [ ] **Step 1: 启动 dev server 并冒烟检查可访问**

Run:
```bash
cd /home/nros/Documents/MirTITH.github.io
timeout 12 hugo server --disableFastRender >/tmp/hugo-home.log 2>&1 &
sleep 7
curl -s -o /dev/null -w "home %{http_code}\n" localhost:1313/
curl -s localhost:1313/ | grep -c "谢阳 / Yang Xie"
wait 2>/dev/null
```
Expected: `home 200`；姓名计数 ≥ 1。

- [ ] **Step 2: 请用户在浏览器确认视觉**

提示用户打开 `http://localhost:1313`（或其常驻的 hugo server）查看：
- 头像、姓名、副标题是否水平居中。
- 三张卡片是否在宽屏一行排开、对称；窄屏是否自动折叠不溢出。

若用户反馈需要微调（字号、间距、灰度等），回到 Task 1 Step 1 调整对应内联样式后重建。仅当用户确认满意，本任务才算完成。

---

## Self-Review

**1. Spec coverage:**
- Hero 区整体居中 → Task 1 Step 1（居中容器 + 居中 h1/p 替代 hero shortcode）✓
- 不加按钮 → Task 1 Step 1（无按钮）+ Step 3（按钮残留计数=0）✓
- 卡片一行三列 → Task 1 Step 1（`cols="3"`）+ Step 3（列变量/类校验）✓
- 头像保持现状 → Task 1 Step 1（样式与原 _index.md 完全一致）✓
- 仅改 _index.md，不碰主题/CSS/其他页面 → File Structure 限定单文件 ✓
- 结构检查（构建无错、居中容器、三列、头像引用、无按钮） → Task 1 Step 2-3 ✓
- 视觉由用户在浏览器确认 → Task 2 ✓

**2. Placeholder scan:** 无 TBD/TODO；所有代码步骤给出完整文件内容与命令；校验命令含明确预期。

**3. 一致性:** 头像路径 `/images/avatar.jpg`、front matter（`title: 🐑`、`layout: hextra-home`）、卡片 `title`/`subtitle`/`link` 参数与现有内容/spec 一致；`cols="3"` 校验同时覆盖 class 与 inline 变量两种渲染形态。
