module Jekyll
    module IndentFilter
        def indent(content)
            output = []
            content.each_line do |line|
                output << line.gsub(/<p>\s\s/, '<p class="indent">')
            end
            output.join('')
        end
    end
end

Liquid::Template.register_filter(Jekyll::IndentFilter)
