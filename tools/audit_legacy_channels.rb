require "date"
require "yaml"
require_relative "../lib/site_channels"

def front_matter(path)
  lines = File.foreach(path).lazy.take(500).to_a
  raise "missing front matter: #{path}" unless lines.first&.strip == "---"
  closing = lines.drop(1).index { |line| line.strip.match?(/\A-{3,}\z/) }
  raise "unterminated front matter: #{path}" unless closing
  YAML.safe_load(lines[1, closing].join, permitted_classes: [Date, Time], aliases: true) || {}
end

allowlist = YAML.safe_load_file("_data/legacy_channel_allowlist.yml", aliases: true)
reviewed = allowlist.values.flatten.to_h { |path| [path, true] }

Dir["_posts/*"].sort.each do |path|
  next if reviewed[path]
  data = front_matter(path)
  next if data["channel"]
  channel = SiteChannels.candidate(data)
  puts [channel, path, data["title"]].join("\t") if channel
end
