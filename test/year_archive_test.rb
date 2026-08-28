require "minitest/autorun"
require "date"
require_relative "../lib/year_archive"

Post = Struct.new(:date)

class YearArchiveTest < Minitest::Test
  def test_groups_descending_years
    groups = YearArchive.groups([Post.new(Date.new(2025, 1, 1)), Post.new(Date.new(2026, 1, 1))])
    assert_equal [2026, 2025], groups.keys
  end

  def test_path
    assert_equal "/archive/2026/", YearArchive.path(2026)
  end
end
