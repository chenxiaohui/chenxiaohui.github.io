#!/usr/bin/env ruby

require "date"
require "jekyll"
require "pathname"
require "rexml/document"
require "uri"
require "yaml"

REQUIRED = %w[index.html tech/index.html life/index.html archive/index.html about/index.html feed.xml feed-tech.xml feed-life.xml sitemap.xml robots.txt].freeze
ALLOWED_CHANNELS = %w[tech life].freeze
ALLOWED_TOPICS = {
  "tech" => ["AI", "系统", "推荐", "工具"],
  "life" => ["湾区", "生活", "阅读", "钱和保险"]
}.freeze
FIXED_DESCRIPTIONS = {
  "index.html" => "工程师，记录 AI、系统与湾区生活",
  "about/index.html" => "工程师，记录 AI、系统与湾区生活",
  "tech/index.html" => "AI、系统、推荐与工具的公开技术笔记",
  "life/index.html" => "湾区日常、阅读、钱和保险",
  "archive/index.html" => "Harry Chen 的文章归档"
}.freeze

def front_matter(path)
  bytes = File.binread(path, 65_537)
  raise "front matter exceeds 64 KiB: #{path}" if bytes.bytesize > 65_536

  lines = bytes.force_encoding("UTF-8").lines
  raise "missing front matter: #{path}" unless lines.first&.strip == "---"

  closing = lines.drop(1).index { |line| line.strip.match?(/\A-{3,}\z/) }
  raise "unterminated front matter: #{path}" unless closing

  raw = lines[1, closing].join
  data = YAML.safe_load(raw, permitted_classes: [Date, Time], aliases: true) || {}
  [data, raw]
end

def html_description(html)
  html[/<meta name="description" content="([^"]*)">/, 1]
end

def output_path(build_dir, url)
  relative = url.delete_prefix("/")
  relative = File.join(relative, "index.html") if url.end_with?("/")
  build_dir.join(relative)
end

build_dir = Pathname(ARGV.fetch(0) { abort "usage: #{$PROGRAM_NAME} BUILD_DIR" }).expand_path
errors = []

REQUIRED.each do |relative|
  errors << "missing required output: #{relative}" unless build_dir.join(relative).file?
end

required_html = REQUIRED.grep(/\.html\z/)
required_html.each do |relative|
  next unless build_dir.join(relative).file?

  html = build_dir.join(relative).read
  errors << "#{relative} missing lang=zh-CN" unless html.match?(/<html[^>]+lang="zh-CN"/)
  errors << "#{relative} missing HTTPS canonical" unless html.match?(/<link rel="canonical" href="https:\/\/chenxiaohui\.me\//)
end

%w[feed.xml feed-tech.xml feed-life.xml sitemap.xml robots.txt].each do |relative|
  next unless build_dir.join(relative).file?

  content = build_dir.join(relative).read
  errors << "#{relative} contains legacy HTTP origin" if content.include?("http://chenxiaohui.me")
end

%w[feed.xml feed-tech.xml feed-life.xml sitemap.xml].each do |relative|
  next unless build_dir.join(relative).file?

  begin
    REXML::Document.new(build_dir.join(relative).read)
  rescue REXML::ParseException
    errors << "#{relative} is not valid XML"
  end
end

FIXED_DESCRIPTIONS.each do |relative, expected|
  next unless build_dir.join(relative).file?

  actual = html_description(build_dir.join(relative).read)
  errors << "#{relative} has unexpected description" unless actual == expected
end

config = YAML.safe_load_file("_config.yml", permitted_classes: [Date, Time], aliases: true)
legacy_identity_values = [config.dig("author", "email")].compact.reject(&:empty?)
FIXED_DESCRIPTIONS.each_key do |relative|
  next unless build_dir.join(relative).file?

  html = build_dir.join(relative).read
  errors << "#{relative} exposes a legacy identity field" if legacy_identity_values.any? { |value| html.include?(value) }
end

channels = YAML.safe_load_file("_data/channels.yml", permitted_classes: [Date, Time], aliases: true)
allowlist = YAML.safe_load_file("_data/legacy_channel_allowlist.yml", permitted_classes: [Date, Time], aliases: true)
profile = YAML.safe_load_file("_data/site_profile.yml", permitted_classes: [Date, Time], aliases: true)
reviewed_paths = allowlist.values.flatten
unless reviewed_paths.include?(profile.fetch("featured_post"))
  featured_data, = front_matter(profile.fetch("featured_post"))
  errors << "featured post has no reviewed channel" unless ALLOWED_CHANNELS.include?(featured_data["channel"])
end

explicit_posts = {}
Dir["_posts/*"].sort.each do |path|
  data, raw = front_matter(path)
  next unless data["channel"]

  explicit_posts[path] = data
  channel = data["channel"]
  errors << "#{path} has invalid channel" unless ALLOWED_CHANNELS.include?(channel)
  topics = Array(data["topics"])
  errors << "#{path} has invalid topics" unless ALLOWED_TOPICS.fetch(channel, []).then { |allowed| !topics.empty? && topics.all? { |topic| allowed.include?(topic) } }
  errors << "#{path} is missing description" if data["description"].to_s.strip.empty?

  cover = data["cover"].to_s
  errors << "#{path} must use a local cover" unless cover.start_with?("/") && File.file?(cover.delete_prefix("/"))
  errors << "#{path} is missing cover_alt" if data["cover_alt"].to_s.strip.empty?
  errors << "#{path} date must include a timezone" unless raw.match?(/^date:\s*.+(?:[+-]\d{4}|Z)\s*$/)

  if data["ai_assisted"] == true
    sources = Array(data["sources"])
    errors << "#{path} needs HTTPS sources" if sources.empty? || sources.any? { |url| URI.parse(url.to_s).scheme != "https" rescue true }
  end
end

site = Jekyll::Site.new(Jekyll.configuration(
  "source" => Dir.pwd,
  "destination" => build_dir.to_s,
  "quiet" => true
))
site.reset
site.read
posts_by_path = site.posts.docs.to_h { |post| [post.relative_path, post] }
post_urls = site.posts.docs.map(&:url)

ALLOWED_CHANNELS.each do |channel|
  relative = "#{channel}/index.html"
  next unless build_dir.join(relative).file?

  html = build_dir.join(relative).read
  visible_urls = post_urls.select { |url| html.include?("href=\"#{url}\"") }
  allowed_paths = Array(allowlist[channel]) + explicit_posts.select { |_path, data| data["channel"] == channel }.keys
  allowed_urls = allowed_paths.filter_map { |path| posts_by_path[path]&.url }
  (visible_urls - allowed_urls).each { |url| errors << "#{relative} exposes unreviewed post #{url}" }
  (allowed_urls - visible_urls).each { |url| errors << "#{relative} is missing reviewed post #{url}" }
end

explicit_posts.each_key do |path|
  post = posts_by_path[path]
  next unless post

  output = output_path(build_dir, post.url)
  unless output.file?
    errors << "missing generated post: #{post.url}"
    next
  end
  if explicit_posts[path]["ai_assisted"] == true && !output.read.include?("由 AI 协助整理，经 Harry Chen 审核")
    errors << "#{path} is missing AI disclosure"
  end
end

if build_dir.join("sitemap.xml").file?
  document = REXML::Document.new(build_dir.join("sitemap.xml").read)
  sitemap_paths = REXML::XPath.match(document, "//*[local-name()='loc']").filter_map do |node|
    URI(node.text).path
  rescue URI::InvalidURIError
    nil
  end.to_h { |path| [path, true] }
  File.readlines("test/fixtures/legacy_urls.txt", chomp: true).reject(&:empty?).each do |path|
    errors << "legacy URL missing from sitemap: #{path}" unless sitemap_paths[path]
  end
end

abort(errors.join("\n")) unless errors.empty?
puts "validated #{build_dir}"
