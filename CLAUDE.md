# Jekyll + GitHub Pages 部署指南

## 自动检查清单

当用户报告"没有生效"或样式/功能未部署时，按以下步骤排查：

### 1. 检查 GitHub Actions 状态

```bash
# 查看最近的 Actions 运行状态
gh api repos/chenxiaohui/chenxiaohui.github.io/actions/runs --jq '.workflow_runs[0:3] | .[] | "\(.created_at) - \(.conclusion) - \(.head_commit.message)"'
```

### 2. 检查 GitHub Pages 配置

```bash
# 查看 Pages 配置
gh api repos/chenxiaohui/chenxiaohui.github.io/pages

# 确认以下关键点：
# - "source.branch" 应该是 "gh-pages" (如果使用 GitHub Actions 部署)
# - 或者是 "master" (如果使用 Jekyll 内置部署)
# - "status" 应该是 "built"
```

**常见问题**：如果使用 GitHub Actions 部署到 `gh-pages` 分支，但 Pages 配置指向 `master` 分支，会导致部署的代码不生效。

**解决方法**：
```bash
# 更新 Pages 配置为使用 gh-pages 分支
gh api --method PUT repos/chenxiaohui/chenxiaohui.github.io/pages --input - <<'EOF'
{
  "source": {
    "branch": "gh-pages",
    "path": "/"
  }
}
EOF
```

### 3. 验证部署内容

```bash
# 获取 gh-pages 分支
git fetch origin gh-pages:gh-pages

# 检查关键文件是否包含预期的更改（以 CSS 为例）
git show gh-pages:assets/css/main.css | grep "你要查找的样式"

# 对比本地构建和线上部署
grep "你要查找的样式" _site/assets/css/main.css
```

### 4. 处理缓存问题

如果代码已正确部署但未生效，可能是缓存问题：

```bash
# 方法1: 触发 Pages 重新构建
gh api --method POST repos/chenxiaohui/chenxiaohui.github.io/pages/builds

# 方法2: 创建空提交触发 GitHub Actions
git commit --allow-empty -m "触发重新部署以清除缓存"
git push origin master
```

用户需要等待 1-3 分钟后**强制刷新浏览器**（Ctrl+Shift+R 或 Cmd+Shift+R）。

### 5. 检查 CDN 缓存

```bash
# 查看文件的缓存头
curl -I https://chenxiaohui.me/assets/css/main.css | grep -i "cache\|etag"

# 注意：
# - cache-control: max-age=14400 表示 4 小时缓存
# - cf-cache-status: HIT 表示 Cloudflare 缓存命中
```

## Jekyll 本地开发

### 启动本地服务器

```bash
# 使用 bun (优先)
bun run serve

# 或使用 bundle
bundle exec jekyll serve -H 0.0.0.0
```

### 生产环境构建

```bash
bun run build
# 或
JEKYLL_ENV=production bundle exec jekyll build
```

### 常见文件路径

- **主题皮肤配置**: `_config.yml` → `text_skin: dark`
- **自定义样式**: `_sass/custom.scss` (会被自动引入到 `assets/css/main.scss`)
- **首页配置**: `_layouts/home.html`
- **文章模板**: `_posts/YYYY-MM-DD-title.md`

## 部署工作流

此项目使用 **GitHub Actions** 自动部署：

1. 推送到 `master` 分支触发 `.github/workflows/deploy.yml`
2. Actions 运行 `JEKYLL_ENV=production bundle exec jekyll build`
3. 构建结果推送到 `gh-pages` 分支
4. GitHub Pages 从 `gh-pages` 分支部署

## 注意事项

- Jekyll 的 SCSS 编译可能会优化掉某些 CSS 属性，使用 `@include` mixins 可以更好地控制输出
- 修改 `_config.yml` 后需要重启 Jekyll 服务器
- 本地构建和生产环境构建可能有差异（检查 `JEKYLL_ENV` 环境变量）
