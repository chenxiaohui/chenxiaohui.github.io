require "minitest/autorun"
require_relative "../lib/site_channels"

class SiteChannelsTest < Minitest::Test
  ALLOWLIST = {
    "tech" => ["_posts/2025-12-28-ai.md"],
    "life" => ["_posts/2026-02-01-alviso-king-tide-and-cat.md"]
  }.freeze

  def test_explicit_channel_wins
    assert_equal "tech", SiteChannels.resolve(
      data: { "channel" => "tech" }, relative_path: "_posts/new.md", allowlist: ALLOWLIST
    )
  end

  def test_reviewed_legacy_path_is_visible
    assert_equal "life", SiteChannels.resolve(
      data: { "categories" => ["生活"] },
      relative_path: "_posts/2026-02-01-alviso-king-tide-and-cat.md",
      allowlist: ALLOWLIST
    )
  end

  def test_category_alone_does_not_publish_legacy_post
    assert_nil SiteChannels.resolve(
      data: { "categories" => ["技术"] }, relative_path: "_posts/unreviewed.md", allowlist: ALLOWLIST
    )
  end

  def test_category_produces_a_review_candidate_only
    assert_equal "tech", SiteChannels.candidate("categories" => ["技术"])
    assert_equal "life", SiteChannels.candidate("categories" => ["生活记录", "湾区"])
    assert_nil SiteChannels.candidate("categories" => ["未审核分类"])
  end

  def test_rejects_unknown_channel
    assert_raises(ArgumentError) do
      SiteChannels.resolve(data: { "channel" => "news" }, relative_path: "_posts/new.md", allowlist: ALLOWLIST)
    end
  end

  def test_topics_belong_to_channel
    assert SiteChannels.valid_topics?(channel: "tech", topics: ["AI", "工具"])
    refute SiteChannels.valid_topics?(channel: "tech", topics: [])
    refute SiteChannels.valid_topics?(channel: "tech", topics: ["湾区"])
  end
end
