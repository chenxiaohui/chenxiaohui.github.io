require_relative "../lib/year_archive"

module YearArchive
  class Page < Jekyll::PageWithoutAFile
    def initialize(site, year, posts)
      super(site, site.source, "archive/#{year}", "index.html")
      self.data = {
        "layout" => "archive-year",
        "title" => year.to_s,
        "description" => "Harry Chen 的 #{year} 年文章归档",
        "nav_key" => "archive",
        "archive_year" => year,
        "posts" => posts
      }
    end
  end

  class Generator < Jekyll::Generator
    safe true

    def generate(site)
      YearArchive.groups(site.posts.docs).each do |year, posts|
        site.pages << Page.new(site, year, posts)
      end
    end
  end
end
