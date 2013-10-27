# Title: Include Pandoc Tag for Jekyll
# Description: Import markdown files and use pandoc to render it.
# Configuration: You can set default import path in _config.yml (defaults to pandoc_dir: pandoc)
#
# Syntax {% pandoc path/to/file %}
#
# Example:
# {% pandoc table.md %}
#
# This will import test.js from source/pandoc/table.md
# and output the contents rendered with pandoc
#

require 'pathname'

module Jekyll
  class PandocTag < Liquid::Tag
    def initialize(tag_name, markup, tokens)
      @file = nil
      if markup.strip =~ /(\S+)/i
        @file = $1
      end
      super
    end

    def render(context)
      code_dir = (context.registers[:site].config['pandoc_dir'].sub(/^\//,'') || 'pandoc')
      code_path = (Pathname.new(context.registers[:site].source) + code_dir).expand_path
      file = code_path + @file
      outfile = code_path + "output.html"
      if File.symlink?(code_path)
        return "Code directory '#{code_path}' cannot be a symlink"
      end

      unless file.file?
        return "File #{file} could not be found"
      end
      
      Dir.chdir(code_path) do
        system "pandoc -o output.html -f markdown -t html #{file}"
        outfile.read
      end
    end
  end

end

Liquid::Template.register_tag('pandoc', Jekyll::PandocTag)
