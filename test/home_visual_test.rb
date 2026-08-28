require "minitest/autorun"
require "nokogiri"
require "pathname"

class HomeVisualTest < Minitest::Test
  BUILD_DIR = Pathname("_site")

  def setup
    skip "run a production Jekyll build before this test" unless BUILD_DIR.join("index.html").file?
    @document = Nokogiri::HTML(BUILD_DIR.join("index.html").read)
  end

  def test_home_uses_the_approved_personal_brand_shell
    shell = @document.at_css(".personal-brand-home")

    refute_nil shell
    refute_nil shell.at_css(".personal-brand-nav")
    refute_nil shell.at_css(".personal-brand-hero")
    assert_equal "HC", shell.at_css(".personal-brand-monogram")&.text&.strip
    refute_nil shell.at_css(".personal-brand-featured")
    assert_equal 2, shell.css(".personal-brand-channel").length
    refute_nil shell.at_css(".personal-brand-footer")
  end

  def test_home_replaces_the_generic_theme_chrome
    assert_empty @document.css(".page__header")
    assert_empty @document.css(".page__footer")
  end

  def test_home_keeps_real_navigation_and_channel_links
    hrefs = @document.css(".personal-brand-home a").map { |node| node["href"] }

    %w[/ /tech/ /life/ /archive/ /about/ /feed.xml].each do |href|
      assert_includes hrefs, href
    end
  end
end
