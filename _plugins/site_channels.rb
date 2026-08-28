require_relative "../lib/site_channels"

module SiteChannels
  class Generator < Jekyll::Generator
    priority :high

    def generate(site)
      allowlist = site.data.fetch("legacy_channel_allowlist")
      site.posts.docs.each do |post|
        channel = SiteChannels.resolve(
          data: post.data,
          relative_path: post.relative_path,
          allowlist: allowlist
        )
        post.data["resolved_channel"] = channel if channel
      end
    end
  end
end
