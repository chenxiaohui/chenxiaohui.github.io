---
layout: post
title: "gitbook使用指导"
date: 2015-08-23 16:23
comments: true
published: true
categories: "Latex"
---
  
  gitbook是nodejs实现的用来帮助书写电子书的，很多开源的书籍项目是基于gitbook的。gitbook的编写语言是markdown，书籍遵循一定的格式完成之后可以通过gitbook发布为各种版本，比如pdf，mobi等电子书格式，或者发布为静态的website，挂到github pages上，对于一些开源项目来说，这是很方便的书写帮助文档的方式。gitbook同样有一个[paas的平台][1]，可以允许多人协作在线完成一部电子书

  首先安装gitbook

  	npm -g install gitbook
  	npm -g install gitbook-cli
  	npm -g install ebook-convert

  第三个是安装生成电子书的插件，但是这里并不会安装bin文件，需要手动安装[Calibre][2]。Mac下可以安装Calibre的app然后链接一下bin：

  	ln -s /Applications/calibre.app/Contents/MacOS/ebook-convert /usr/local/bin

  这样就可以生成pdf/mobi等格式的电子书了。

  使用方式可以通过gitbook help来查看。主要是如下几个：

  	gitbook build [book] [output] 	生成电子书，通过--format指定输出格式，默认输出为website
  	gitbook pdf [book] [output]     生成pdf电子书
	gitbook epub [book] [output]    生成epub电子书
  	gitbook mobi [book] [output]    生成mobi电子书
  	serve [book] 	 				生成并开启http server预览
  	init [directory]				根据summary建立基本目录结构
  	install [book]					安装依赖和插件

  Summary的基本样子见这里：

  	# Summary
	* [Introduction](README.md)
	* [入门](getting_started/README.md)
	   * [初识](getting_started/what_is_it.md)
	   * [安装](getting_started/installing_es.md)
	   * [API](getting_started/api.md)
	   * [文档](getting_started/document.md)
	   * [索引](getting_started/tutorial_indexing.md)
	   * [搜索](getting_started/tutorial_search.md)
	   * [汇总](getting_started/tutorial_aggregations.md)
	   * [小结](getting_started/tutorial_conclusion.md)
	   * [分布式](getting_started/distributed.md)
	   * [本章总结](getting_started/conclusion.md)
	* [分布式集群](distributed_cluster/README.md)




[1]: https://www.gitbook.com/ "A modern publishing toolchain. Simply taking you from ideas to finished, polished books."
[2]: http://calibre-ebook.com/ "calibre: The one stop solution for all your e-book needs. Comprehensive e-book software."