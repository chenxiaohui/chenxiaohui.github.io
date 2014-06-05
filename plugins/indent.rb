module Jekyll
    module IndentFilter
        def indent(content)
            content.gsub(/<p>\s\s/, '<p class="indent">')
            #content.gsub(/<p>\s\s/, '<p class="indent">').gsub(/((<ul>|<ol>)\n<li>\s[\s\S]*?(<\/ul>|<\/ol>))/, '<blockquote>\1</blockquote>')
        end
    end
end

Liquid::Template.register_filter(Jekyll::IndentFilter)
