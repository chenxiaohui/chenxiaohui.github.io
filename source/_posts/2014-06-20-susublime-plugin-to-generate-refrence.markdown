---
layout: post
title: "sublime根据markdown引用生成参考文献的插件"
date: 2014-06-20 21:21
comments: true
categories: "web相关"
---

  写这个的目的主要是每次写博客需要生成以下版权声明，免得引用了别人的文章被人说盗版。markdown里面支持通过列表组织引用的url，如下所示：

	  [1]: http://www.baidu.com   "百度"
	  [2]: http:://www.google.com "谷歌"
	  [3]: http://www.facebook.com "404 Not Found"

  我们可以通过这个形式来生成如下的代码


  效果如下：

<!--more-->

  代码如下:

	#!/usr/bin/python
	#coding=utf-8
	#Filename:generate_ref.py

	import sublime, sublime_plugin

	class GeneraterefCommand(sublime_plugin.TextCommand):
	    def run(self, edit):
	        sels = self.view.sel()
	        lines=[]
	        for sel in sels:
	            lines += (self.view.substr(sel)).strip("\n").split("\n")
	        outlines=[]
	        for line in lines:
	            idx1 = line.find(":")
	            index = line[:idx1]
	            idx2 = line.find('"', idx1)
	            url = line[idx1+1:idx2].strip(' ')
	            title = line[idx2:].strip('"')
	            outlines.append('\n>\%s %s, <%s>'%(index,title,url))
	        self.view.insert(edit, sel.end(),"\n###参考文献:\n".decode("utf-8") + "\n".join(outlines))

###参考文献:

  \[1] 百度, <http://www.baidu.com>

  \[2] 谷歌, <http:://www.google.com>

  \[3] 404 Not Found, <http://www.facebook.com>

