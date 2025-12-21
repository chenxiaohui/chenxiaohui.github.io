# Claude 使用说明

本文件包含使用 Claude 管理此博客的重要说明和注意事项。

## 发布新文章的完整流程

### 1. 创建新文章

使用 Rakefile 提供的任务创建新文章：

```bash
bundle exec rake post title="你的文章标题"
```

或者手动创建文件到 `_posts` 目录，文件名格式：`YYYY-MM-DD-slug.md`

### 2. 必需的 Front Matter 字段

每篇文章的 front matter **必须**包含以下字段：

```yaml
---
layout: article
title: "文章标题"
key: unique_article_key
date: YYYY-MM-DD HH:MM
published: true           # ⚠️ 重要：必须设置为 true
categories: "技术"
comments: true
---
```

### 3. 写作风格要求 ⚠️

**重要**：文章必须像真人写的，不要有 AI 腔调。

#### 写作原则

- **用口语化表达**：用"挺"、"还行"、"估计"、"大概"等日常用语，别太书面
- **避免过度修饰**：不要用"莫过于"、"悄然而至"、"终究"这类文绉绉的词
- **表达要真实**：可以说"说实话"、"挺突然的"、"有点懵"，别装得太明白
- **承认不确定性**：可以说"走一步看一步"、"估计够呛"，不要什么都很确定
- **用短句**：长句拆成短句，读起来轻松
- **允许不完美**：可以有语气词、口语、甚至不那么完整的句子

#### 要避免的 AI 写作特征

❌ 过度使用排比和对仗（"既...又..."、"不仅...也..."）
❌ 文学化的过渡词（"然而"、"诚然"、"固然"）
❌ 总结性太强的结尾（"无论如何，都要..."）
❌ 过于完整的逻辑结构（每段都有总分总）
❌ 华丽的形容词堆砌

✅ 更自然的表达：
- "说起来也挺神奇的" 而不是 "回顾往昔，颇为感慨"
- "估计够呛" 而不是 "这将是一个巨大的挑战"
- "不过也就这样了，走一步看一步吧" 而不是 "但我相信通过不断努力..."

### 4. ⚠️ 技术注意事项

#### 时间设置问题（关键！）

- **问题**：Jekyll 默认不会发布"未来"的文章（future posts）
- **原因**：GitHub Pages 使用 UTC 时间构建，而 `_config.yml` 中 `timezone` 未设置
- **解决方案**：
  - 文章的 `date` 字段使用**早上的时间**（如 06:00 - 08:00）
  - 避免使用 10:00 之后的时间，因为可能被 UTC 时间判断为未来时间
  - 推荐格式：`date: YYYY-MM-DD 06:00`

#### 必需字段检查清单

- [ ] `published: true` - 没有此字段文章不会发布
- [ ] `layout: article` - 使用正确的布局
- [ ] `date` 使用早上时间（06:00-08:00）
- [ ] `key` 是唯一的标识符
- [ ] `categories` 和 `comments` 已设置

### 5. 部署流程

#### 自动部署

1. 创建或修改文章后，提交到 master 分支：
   ```bash
   git add _posts/YYYY-MM-DD-your-post.md
   git commit -m "添加新文章：文章标题"
   git push
   ```

2. GitHub Actions 会自动触发构建（通常需要 1-2 分钟）

3. 等待 3-5 分钟后访问网站验证：
   - 首页：https://chenxiaohui.me/
   - 文章页面：https://chenxiaohui.me/YYYY/MM/DD/article-slug/

#### 如果自动部署没有触发

有时 GitHub Actions 可能延迟，可以尝试：

1. 创建空提交强制触发：
   ```bash
   git commit --allow-empty -m "触发重新构建"
   git push
   ```

2. 或者访问 GitHub 网站手动检查：
   - Actions 页面：https://github.com/chenxiaohui/chenxiaohui.github.io/actions
   - Pages 设置：https://github.com/chenxiaohui/chenxiaohui.github.io/settings/pages

### 6. 分支说明

- **master 分支**：Jekyll 源代码 + 自动部署分支
  - 包含 `_posts/`, `_layouts/`, `_config.yml` 等
  - GitHub Pages 从此分支的根目录（`/`）构建网站
  - **所有文章修改都应该在这个分支上进行**

- **source 分支**：历史遗留分支
  - 2019年的旧配置
  - 目前不再使用
  - ⚠️ 不要在这个分支上添加文章

### 7. 常见问题排查

#### 文章没有显示在网站上

检查清单：
1. ✅ Front matter 中有 `published: true`
2. ✅ `date` 字段使用的是早上时间（06:00-08:00）
3. ✅ 文件已经 commit 并 push 到 master 分支
4. ✅ GitHub Actions 构建成功（查看 Actions 页面）
5. ✅ 等待 3-5 分钟让 CDN 缓存刷新

#### 构建成功但网站没更新

- 可能是 CDN 缓存问题，等待 5-15 分钟
- 尝试在 URL 后添加时间戳强制刷新：`https://chenxiaohui.me/?v=123456`

### 8. 本地预览

在推送到 GitHub 之前，可以本地预览：

```bash
# 启动本地 Jekyll 服务器
bun run serve
# 或
bundle exec jekyll serve

# 访问 http://localhost:4000
```

### 9. 快速参考

**创建新文章**：
```bash
bundle exec rake post title="文章标题"
```

**提交并发布**：
```bash
git add _posts/YYYY-MM-DD-*.md
git commit -m "添加新文章：标题"
git push
```

**检查部署状态**：
- Actions: https://github.com/chenxiaohui/chenxiaohui.github.io/actions
- 网站: https://chenxiaohui.me/

---

## 历史问题记录

### 2025-12-21：首次发布新文章遇到的问题

**问题**：文章添加后网站没有显示

**原因**：
1. Front matter 缺少 `published: true` 字段
2. `date` 字段设置为 `10:00`，被 Jekyll 判断为 future post

**解决方案**：
1. 添加 `published: true` 到 front matter
2. 将时间改为 `06:00`（早上时间）

**经验教训**：
- 始终使用 Rakefile 创建文章，它会自动添加所有必需字段
- 如果手动创建，务必检查所有必需字段
- 时间设置使用早上时间避免 UTC 时区问题
