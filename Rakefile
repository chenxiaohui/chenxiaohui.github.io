require 'date'

desc "Create a new blog post"
task :post do
  title = ENV['title'] || ENV['TITLE']

  if title.nil? || title.empty?
    puts "Usage: rake post title=\"Your Post Title\""
    puts "Example: rake post title=\"My New Blog Post\""
    exit 1
  end

  # Generate slug from title
  slug = title.downcase.strip.gsub(/\s+/, '-').gsub(/[^\w\-]/, '')

  # Get current date and time
  date = Date.today.strftime('%Y-%m-%d')
  datetime = Time.now.strftime('%Y-%m-%d %H:%M')

  # Generate filename
  filename = File.join('_posts', "#{date}-#{slug}.md")

  # Check if file already exists
  if File.exist?(filename)
    puts "Error: File already exists: #{filename}"
    exit 1
  end

  # Generate frontmatter
  content = <<~HEREDOC
    ---
    layout: article
    title: "#{title}"
    key: #{slug}
    date: #{datetime}
    published: true
    categories: "技术"
    comments: true
    ---

    这里写文章摘要...

    <!--more-->

    ## 正文标题

    这里是文章正文内容...

  HEREDOC

  # Create the file
  File.write(filename, content)

  puts "✓ Created new post: #{filename}"
  puts "✓ Title: #{title}"
  puts "✓ Date: #{datetime}"
  puts ""
  puts "Next steps:"
  puts "  1. Edit the post: #{filename}"
  puts "  2. Preview: bundle exec jekyll serve"
  puts "  3. Commit: git add #{filename} && git commit -m 'modify #{date.gsub('-', '')}'"
end

desc "Create a new draft post"
task :draft do
  title = ENV['title'] || ENV['TITLE']

  if title.nil? || title.empty?
    puts "Usage: rake draft title=\"Your Draft Title\""
    exit 1
  end

  slug = title.downcase.strip.gsub(/\s+/, '-').gsub(/[^\w\-]/, '')
  date = Date.today.strftime('%Y-%m-%d')
  datetime = Time.now.strftime('%Y-%m-%d %H:%M')
  filename = File.join('_posts', "#{date}-#{slug}.md")

  if File.exist?(filename)
    puts "Error: File already exists: #{filename}"
    exit 1
  end

  content = <<~HEREDOC
    ---
    layout: article
    title: "#{title}"
    key: #{slug}
    date: #{datetime}
    published: false
    categories: "草稿"
    comments: true
    ---

    草稿内容...

  HEREDOC

  File.write(filename, content)
  puts "✓ Created draft: #{filename}"
end

desc "List recent posts"
task :list do
  posts = Dir.glob('_posts/*.md').sort.reverse.take(10)

  puts "\nRecent posts:"
  puts "=" * 60

  posts.each do |post|
    basename = File.basename(post)
    # Extract title from frontmatter
    content = File.read(post)
    if content =~ /^title:\s*["']?(.+?)["']?$/
      title = $1
      puts "#{basename.ljust(45)} | #{title}"
    else
      puts basename
    end
  end

  puts "=" * 60
  puts "\nTotal posts: #{Dir.glob('_posts/*.md').count}"
end
