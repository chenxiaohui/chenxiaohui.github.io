require "minitest/autorun"
require "nokogiri"
require "pathname"

class ArchiveVisualTest < Minitest::Test
  BUILD_DIR = Pathname("_site")

  def setup
    skip "run a production Jekyll build before this test" unless BUILD_DIR.join("archive/index.html").file?
    @archive = Nokogiri::HTML(BUILD_DIR.join("archive/index.html").read)
    @year = Nokogiri::HTML(BUILD_DIR.join("archive/2011/index.html").read)
  end

  def test_archive_uses_the_personal_brand_shell
    shell = @archive.at_css(".personal-brand-page")

    refute_nil shell
    refute_nil shell.at_css(".personal-brand-nav")
    refute_nil shell.at_css('.personal-brand-nav a.is-active[href="/archive/"]')
    refute_nil shell.at_css(".personal-brand-footer")
    assert_empty @archive.css(".page__header")
    assert_empty @archive.css(".page__footer")
  end

  def test_archive_exposes_filterable_posts_and_load_more
    archive = @archive.at_css("[data-archive]")

    refute_nil archive
    assert_equal "20", archive["data-batch-size"]
    refute_nil archive.at_css("[data-archive-year]")
    refute_nil archive.at_css("[data-archive-channel]")
    assert_operator archive.css("[data-archive-item]").length, :>, 20
    refute_nil archive.at_css("[data-archive-load-more]")
    refute_nil @archive.at_css('script[src^="/assets/js/archive.js?v="]')
  end

  def test_year_archive_uses_the_same_progressive_list
    archive = @year.at_css('[data-archive][data-fixed-year="2011"]')

    refute_nil @year.at_css(".personal-brand-page")
    refute_nil archive
    assert_equal 115, archive.css("[data-archive-item]").length
    refute_nil archive.at_css("[data-archive-load-more]")
  end
end
