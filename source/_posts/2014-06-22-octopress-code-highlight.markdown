---
layout: post
title: "octopress代码着色"
date: 2014-06-22 11:15
comments: true
categories: "web相关"
---


  markdown有自己支持的代码模块，但是想支持着色，就需要单独对代码进行parse和加上css。octopress支持自己的代码语法，但是比较麻烦，并且是本地渲染，对不同语言需要指定。

  所以还是js渲染比较方便一点，我们可以用[google code prettify][1]进行着色，在markdown里面只要对代码加入缩进（tab或者四个空格）。服务端引入如下js:
	
	<link href="{{ root_url }}/javascripts/google-code-prettify/prettify.css" media="screen, projection" rel="stylesheet" type="text/css">
	<script type="text/javascript" src="{{ root_url }}/javascripts/google-code-prettify/prettify.js"></script>
	
	<script type="text/javascript" >
	<!--
	    $(function() {
	      $('pre').addClass('prettyprint').attr('style', 'overflow:auto');
	      window.prettyPrint && prettyPrint();
	      $('table').addClass('table')
	});
	-->
	</script>

  google code prettify的样式可以[这里][2]选择，关于行号的一些问题参见[这里][3]。

[1]:https://code.google.com/p/google-code-prettify/ "google code prettify"
[2]:http://jmblog.github.io/color-themes-for-google-code-prettify/ "google code prettify theme"
[3]:http://blog.evercoding.net/2013/02/27/highlight-code-with-google-code-prettify/ "Jekyll中使用google-code-prettify高亮代码"

###参考文献:

  \[1] google code prettify, <https://code.google.com/p/google-code-prettify/>
 
  \[2] google code prettify theme, <http://jmblog.github.io/color-themes-for-google-code-prettify/>
 
  \[3] Jekyll中使用google-code-prettify高亮代码, <http://blog.evercoding.net/2013/02/27/highlight-code-with-google-code-prettify/>
