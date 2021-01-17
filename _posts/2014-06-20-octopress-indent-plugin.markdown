---
layout: article
title: "octopress的缩进插件"
date: 2014-06-20 20:45
comments: true
categories: "web相关"
---



  我们写中文的时候通常有首行缩进的需求，markdown默认是不支持的，octopress和wordpress也没有缩进的css。这里我们通过加个插件的方式完成。

  首先，处理markdown的渲染。我们建立如下插件:

	  	module Jekyll
	    module IndentFilter
	        def indent(content)
	            content.gsub(/<p>\s\s/, '<p class="indent">')
	        end
	    end
	end

	Liquid::Template.register_filter(Jekyll::IndentFilter)
  
  这个就是做了个替换。会把行首的两个字符替换成一个css标签。然后加个css在系统css里面就行了：

	.indent{text-indent:2em;}
  
<!--more-->

  需要注意的是，整个文章的缩进层次可以这样使用：

	# first
	## second
	## third
	** bold **
	no indent
	* item
	  indent
	  > * indent item

  效果如下所示：

# first
## second
## third

** bold **

no indent

* item

  indent

> * indent item

