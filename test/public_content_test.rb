require "minitest/autorun"
require "nokogiri"
require "pathname"
require "uri"

class PublicContentTest < Minitest::Test
  BUILD_DIR = Pathname("_site")
  FORBIDDEN_PUBLIC_TEXT = [
    "支付宝北京",
    "支付宝Oceanbase组",
    "搜狐大数据中心",
    "美团云"
  ].freeze
  UNAVAILABLE_ASSET_HOSTS = %w[
    csrd.aliapp.com
    fmn.xnimg.cn
    image.beekka.com
    static.data.taobaocdn.com
    www.ccvita.com
    www.roybit.com
  ].freeze

  def setup
    skip "run a production Jekyll build before this test" unless BUILD_DIR.join("index.html").file?
  end

  def test_current_brand_pages_do_not_publish_confirmed_work_history
    brand_pages = %w[index.html about/index.html tech/index.html life/index.html archive/index.html]
    hits = brand_pages.each_with_object([]) do |relative, found|
      path = BUILD_DIR.join(relative)
      text = path.read
      matches = FORBIDDEN_PUBLIC_TEXT.select { |term| text.include?(term) }
      found << [relative, matches] unless matches.empty?
    end

    assert_empty hits
  end

  def test_generated_links_use_the_canonical_archive_path
    legacy_links = html_files.flat_map do |path|
      Nokogiri::HTML(path.read).css('a[href^="/archive.html"]').map do |link|
        [path.relative_path_from(BUILD_DIR).to_s, link["href"]]
      end
    end

    assert legacy_links.empty?, "legacy archive links remain: #{legacy_links.first(10).inspect}"
  end

  def test_liquid_like_cpp_initializers_render_verbatim
    union_page = Nokogiri::HTML(BUILD_DIR.join("2016/05/26/union-struct-initialize/index.html").read)
    spinlock_page = Nokogiri::HTML(BUILD_DIR.join("2016/06/13/safe-spin-lock/index.html").read)

    assert_includes union_page.text, "S3Atomic atomic = {{.pid = 2, .atomic32 = 1}};"
    assert_includes spinlock_page.text, "SpinLock lock_val = {{{.tid = (int32_t)_get_tid(), .atomic32 = 1}}};"
  end

  def test_generated_pages_do_not_reference_confirmed_unavailable_assets
    hits = html_files.flat_map do |path|
      Nokogiri::HTML(path.read).css("[href], [src]").each_with_object([]) do |node, found|
        url = node["href"] || node["src"]
        host = URI.parse(url).host rescue nil
        if UNAVAILABLE_ASSET_HOSTS.include?(host)
          found << [path.relative_path_from(BUILD_DIR).to_s, node.name, url]
        end
      end
    end

    assert_empty hits
    placeholder_count = html_files.sum do |path|
      Nokogiri::HTML(path.read).css(".legacy-media-unavailable").length
    end
    assert_operator placeholder_count, :>, 0
  end

  def test_generated_posts_do_not_reference_missing_local_targets
    hits = generated_post_files.flat_map do |path|
      Nokogiri::HTML(path.read).css("[href], [src]").filter_map do |node|
        value = node["href"] || node["src"]
        next if local_target_exists?(path, value)

        [path.relative_path_from(BUILD_DIR).to_s, node.name, value]
      end
    end

    assert hits.empty?, "missing local post targets remain: #{hits.first(10).inspect}"
  end

  private

  def html_files
    @html_files ||= BUILD_DIR.glob("**/*.html")
  end

  def generated_post_files
    @generated_post_files ||= BUILD_DIR.glob("20??/**/index.html")
  end

  def local_target_exists?(source, value)
    return true if value.nil? || value.empty? || value.start_with?("#", "mailto:", "tel:", "javascript:", "data:")

    uri = URI.parse(value)
    return true if uri.host || uri.path.nil? || uri.path.empty?

    decoded = URI::DEFAULT_PARSER.unescape(uri.path)
    relative = if decoded.start_with?("/")
      decoded.delete_prefix("/")
    else
      source.dirname.relative_path_from(BUILD_DIR).join(decoded).cleanpath.to_s
    end
    candidates = if decoded.end_with?("/")
      [BUILD_DIR.join(relative, "index.html")]
    else
      [BUILD_DIR.join(relative), BUILD_DIR.join(relative, "index.html")]
    end
    candidates.any?(&:exist?)
  rescue URI::InvalidURIError
    false
  end
end
