module SiteChannels
  CHANNELS = %w[tech life].freeze
  TOPICS = {
    "tech" => ["AI", "系统", "推荐", "工具"],
    "life" => ["湾区", "生活", "阅读", "钱和保险"]
  }.freeze
  CANDIDATE_CATEGORIES = {
    "tech" => ["技术", "Linux", "C++", "Python", "Java", "web相关", "分布式系统", "效率工具", "工具"],
    "life" => ["生活", "生活记录", "湾区", "阅读", "摄影", "随笔", "钱和保险"]
  }.freeze

  module_function

  def resolve(data:, relative_path:, allowlist:)
    explicit = data["channel"]
    if explicit
      raise ArgumentError, "invalid channel: #{explicit}" unless CHANNELS.include?(explicit)
      return explicit
    end

    CHANNELS.find { |channel| Array(allowlist[channel]).include?(relative_path) }
  end

  def valid_topics?(channel:, topics:)
    values = Array(topics)
    CHANNELS.include?(channel) && !values.empty? && values.all? { |topic| TOPICS.fetch(channel).include?(topic) }
  end

  def candidate(data)
    categories = Array(data["categories"]).map(&:to_s)
    CHANNELS.find { |channel| (categories & CANDIDATE_CATEGORIES.fetch(channel)).any? }
  end
end
