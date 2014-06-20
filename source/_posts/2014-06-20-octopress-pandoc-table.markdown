---
layout: post
title: "octopress支持markdown表格"
date: 2014-06-20 20:57
comments: true
categories: "web相关"
---



   pandoc支持扩展的markdown，也就是支持类似于如下的表格：

	-----------------------------------------------------------------------------------------------------------------
	测量指标                    低程度中心性             低亲近中心性                      低居间中心性
	--------------------   -------------------   -----------------------------  -------------------------------------
	高程度中心性                                        “自我”所嵌入的聚类                “自我”的联系人是冗余的，
	                                                   远离网络中其他节点                整个世界绕他而行


	高亲近中心性               是联系重要他人或                                       在事件中，自我位于一个相互
	                         活跃人物的关键人物                                     联系密切、活跃的聚类中，与
	                                                                             很多节点都很接近；其他节点也是如此
	------------------------------------------------------------------------------------------------------------------
	: 表3-1 不同中心性测量指标之间的关系[^16]
  
  效果可以渲染成这样：

{% pandoc test.md %}

<!--more-->

  插件如下。

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

  使用的时候先生成一个md文件，放在source/pandoc（随便设定）目录下。插件只是生成了html文件然后read进来了而已，所以有点傻，比如下面我的代码放到缩进里面还是被执行了。

  最后用如下语法载入（去掉空格）：

  	{ % pandoc test.md % }