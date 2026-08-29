require "nokogiri"
require "pathname"
require "uri"

module LegacyContentSanitizer
  UNAVAILABLE_HOSTS = %w[
    csrd.aliapp.com
    fmn.xnimg.cn
    image.beekka.com
    static.data.taobaocdn.com
    www.ccvita.com
    www.roybit.com
  ].freeze

  module_function

  def unavailable?(value)
    host = value.to_s[%r{\Ahttps?://([^/:?#]+)}, 1]
    UNAVAILABLE_HOSTS.include?(host&.downcase)
  end

  def sanitize(html)
    document = Nokogiri::HTML(html)
    document.css("[href], [src]").each do |node|
      attribute = node["href"] ? "href" : "src"
      next unless unavailable?(node[attribute])

      if node.name == "a"
        node.remove_attribute("href")
        node["class"] = [node["class"], "legacy-link-unavailable"].compact.join(" ")
        node["title"] = "历史链接已失效"
      else
        placeholder = Nokogiri::XML::Node.new("span", document)
        placeholder["class"] = "legacy-media-unavailable"
        placeholder["role"] = "img"
        placeholder["aria-label"] = node["alt"].to_s unless node["alt"].to_s.empty?
        placeholder.content = "历史图片暂不可用"
        node.replace(placeholder)
      end
    end
    document.to_html
  end

  def sanitize_missing_local_targets(html, source:, destination:)
    document = Nokogiri::HTML(html)
    document.css("[href], [src]").each do |node|
      attribute = node["href"] ? "href" : "src"
      next unless missing_local_target?(node[attribute], source: source, destination: destination)

      if node.name == "a"
        node.remove_attribute("href")
        node["class"] = [node["class"], "legacy-link-unavailable"].compact.join(" ")
        node["title"] = "历史链接已失效"
      else
        placeholder = Nokogiri::XML::Node.new("span", document)
        placeholder["class"] = "legacy-media-unavailable"
        placeholder["role"] = "img"
        placeholder["aria-label"] = node["alt"].to_s unless node["alt"].to_s.empty?
        placeholder.content = "历史图片暂不可用"
        node.replace(placeholder)
      end
    end
    document.to_html
  end

  def missing_local_target?(value, source:, destination:)
    return false if value.nil? || value.empty? || value.start_with?("#", "mailto:", "tel:", "javascript:", "data:")

    uri = URI.parse(value)
    return false if uri.host || uri.path.nil? || uri.path.empty?

    decoded = URI::DEFAULT_PARSER.unescape(uri.path)
    relative = if decoded.start_with?("/")
      decoded.delete_prefix("/")
    else
      source.dirname.relative_path_from(destination).join(decoded).cleanpath.to_s
    end
    return true if relative == ".." || relative.start_with?("../")

    candidates = if decoded.end_with?("/")
      [destination.join(relative, "index.html")]
    else
      [destination.join(relative), destination.join(relative, "index.html")]
    end
    candidates.none?(&:exist?)
  rescue URI::InvalidURIError
    true
  end
end

Jekyll::Hooks.register :posts, :post_render do |post|
  post.output = LegacyContentSanitizer.sanitize(post.output)
end

Jekyll::Hooks.register :site, :post_write do |site|
  destination = Pathname(site.dest)
  site.posts.docs.each do |post|
    output = Pathname(post.destination(site.dest))
    next unless output.file?

    html = output.read
    sanitized = LegacyContentSanitizer.sanitize_missing_local_targets(
      html,
      source: output,
      destination: destination
    )
    output.write(sanitized) unless sanitized == html
  end
end
