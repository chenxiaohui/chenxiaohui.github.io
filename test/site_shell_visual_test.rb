require "minitest/autorun"
require "nokogiri"
require "pathname"

class SiteShellVisualTest < Minitest::Test
  BUILD_DIR = Pathname("_site")
  PAGES = {
    "tech/index.html" => "/tech/",
    "life/index.html" => "/life/",
    "about/index.html" => "/about/"
  }.freeze

  def setup
    skip "run a production Jekyll build before this test" unless BUILD_DIR.join("index.html").file?
  end

  def test_primary_pages_share_the_personal_brand_shell
    PAGES.each do |relative, active_href|
      document = read_page(relative)
      shell = document.at_css(".personal-brand-page")

      refute_nil shell, "missing personal shell on #{relative}"
      refute_nil shell.at_css(".personal-brand-nav")
      refute_nil shell.at_css(%(.personal-brand-nav a.is-active[href="#{active_href}"]))
      refute_nil shell.at_css(".personal-brand-footer")
      visible_headings = document.xpath('//h1[not(ancestor::header[contains(@style, "display:none")])]')
      assert_equal 1, visible_headings.length, "duplicate page title on #{relative}"
      assert_empty document.css(".page__header")
      assert_empty document.css(".page__footer")
    end
  end

  def test_404_uses_the_same_shell
    document = read_page("404/index.html")

    refute_nil document.at_css(".personal-brand-page .layout--404")
    refute_nil document.at_css(".personal-brand-nav")
    refute_nil document.at_css(".personal-brand-footer")
    assert_empty document.css(".page__header")
    assert_empty document.css(".page__footer")
  end

  def test_article_keeps_its_content_inside_the_same_shell
    document = read_page("2016/05/26/union-struct-initialize/index.html")

    refute_nil document.at_css(".personal-brand-page .layout--article")
    refute_nil document.at_css(".personal-brand-nav")
    refute_nil document.at_css(".personal-brand-footer")
    assert_includes document.text, "S3Atomic atomic = {{.pid = 2, .atomic32 = 1}};"
    assert_empty document.css(".page__header")
    assert_empty document.css(".page__footer")
  end

  private

  def read_page(relative)
    Nokogiri::HTML(BUILD_DIR.join(relative).read)
  end
end
