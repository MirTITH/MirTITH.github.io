# 首页居中布局美化设计文档

**日期**：2026-06-18
**目标**：将个人主页首页（`content/_index.md`）改为居中布局，卡片改为一行三列，修复当前左对齐失衡、"2+1"卡片留白等不美观问题。

## 背景

- 站点 Hugo + Hextra（v0.11.1），首页 [content/_index.md](../../../content/_index.md) 使用 `layout: hextra-home`。
- 现状（据截图与构建产物）：
  - 头像、姓名、副标题**左对齐**且重心偏左上。
  - 用户已手动删除原有的两个 `hero-button`，顶部无按钮。
  - 三张 feature-card 呈"2+1"换行，右下大片留白。
- **根因（已实测）**：Hextra home 布局外层容器为 `hx:flex hx:flex-col hx:items-start`，`items-start` 使所有子元素靠左；`hero-headline`/`hero-subtitle` 亦默认左对齐且无居中参数。
- **feature-grid 默认 grid 类**：`hx:sm:max-lg:grid-cols-2 hx:max-sm:grid-cols-1`，无 3 列规则，故第 3 张卡片换行。

## 已确认的设计决策

| 维度 | 决策 |
|---|---|
| 整体对齐 | Hero 区（头像+姓名+副标题）整体**居中** |
| 按钮 | **不加按钮**（保持用户已删除的状态） |
| 卡片排列 | **一行三列**（`feature-grid` 加 `cols="3"`），小屏自动折叠 |
| 头像 | **保持现状**（160px 圆形、黑底，不处理图片） |
| 实现范围 | 仅改 `content/_index.md`，不碰主题、不加 CSS 文件、不改其他页面 |

## 详细设计

### 1. Hero 区居中

用一个 `width: 100%; text-align: center;` 的容器包裹头像、姓名、副标题，以抵消外层 `items-start` 的左对齐。姓名/副标题用普通居中标签替代 `hero-headline`/`hero-subtitle` shortcode（后者无居中参数，且在 flex 容器内强制左对齐）：

```html
<div style="width: 100%; text-align: center;" class="hx-mt-6">
  <img src="/images/avatar.jpg" alt="谢阳"
       style="width: 160px; height: 160px; border-radius: 9999px; object-fit: cover; display: inline-block;" />
  <h1 style="margin-top: 1rem; font-size: 2.5rem; font-weight: 800; line-height: 1.2;">谢阳 / Yang Xie</h1>
  <p style="margin-top: 0.5rem; font-size: 1.125rem; color: #6b7280;">机器人与具身智能方向硕士在读 · 哈工大（深圳）</p>
</div>
```

- 头像样式与现状完全一致（不改图片、不改尺寸、不动黑底）。
- 姓名 `<h1>`：约 2.5rem、加粗。
- 副标题 `<p>`：约 1.125rem、灰色（`#6b7280`，深浅适中，明暗主题下均可读）。
- 不含任何按钮。

### 2. 卡片一行三列

```
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

- `cols="3"` 设置 `--hextra-feature-grid-cols: 3`，桌面一行三列；Hextra 内置响应式在小屏折叠为单列/两列。
- 三张卡片内容不变。

### 3. front matter

保持 `title: 🐑`、`layout: hextra-home` 不变。

## 文件改动总览

| 文件 | 改动 |
|---|---|
| `content/_index.md` | Hero 区改居中（替换两个 hero shortcode 为居中 `<h1>`/`<p>`）；`feature-grid` 加 `cols="3"` |

## 验收标准

**结构检查（由实现方完成）：**
- `hugo` 构建无 error。
- 构建产物 `public/index.html` 中：`--hextra-feature-grid-cols` 或 `cols=3` 对应的 3 列样式生效；姓名「谢阳 / Yang Xie」与副标题出现在 `text-align: center` 容器内；头像 `/images/avatar.jpg` 仍被引用；无 `hextra/hero-button` 残留、无按钮文案。

**视觉确认（由用户在浏览器完成）：**
- 头像、姓名、副标题在页面水平居中。
- 三张卡片在宽屏一行排开、对称；窄屏自动折叠不溢出。
- 整体观感平衡，无明显左偏或大片留白。

## 不做的事（YAGNI）

- 不加任何按钮。
- 不处理头像图片（黑底保持）。
- 不新增自定义 layout 或全局 CSS 文件。
- 不改动导航、关于页或其他内容。
- 不引入社交图标、动效等额外元素（如需可后续单独立项）。
