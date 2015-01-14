---
layout: post
title: "Django自定义Filter"
date: 2015-01-14 13:29
comments: true
published: true
categories: "Python"
---

  遇到这样一个问题：Django中有字段是根据位来存储信息的，并且不是对应Model数据库中的字段，BitField使用起来比较不太适合。这样就得在模板中根据位来显示不同的内容。查Django并试验，好像位操作不能直接写在if操作符中，同时django也不支持在模板直接调用函数。一个合理的选择是建立自定义的Filter。详见[参考文献][1]。基本代码如下：

  	配置：
  	mSohuConf={
    	"A_mask" : 0x04,
    	"B_mask" : 0x02,
    	"C_mask" : 0x01,
	}

  	Filter代码：
	from django import template
	from django.utils.safestring import mark_safe
	from .. import config
	register = template.Library()
	mask_html = (
	    (config.mSohuConf['A_mask'], '<span class="label label-danger">A</span>'),
	    (config.mSohuConf['B_mask'], '<span class="label label-warning">B</span>'),
	    (config.mSohuConf['C_mask'], '<span class="label label-info">C</span>'),
	)
	default_html = '<span class="label label-default">D</span>'
	@register.filter()
	def news_tag(value):
	    output = default_html
	    for mask, html in mask_html:
	        if value & mask:
	            output += html +'\n'
	    return mark_safe(output)

	模板：
	{% load news_tag %}
	<td>{{item.status|news_tag}}</td>

<!--more-->

  需要注意的有：

  1. mark_safe是必须的，否则会被自动escape。
  2. 使用的时候需要load。写的时候需要register声明或者手动声明。
  3. 文档说必须重启才能使用新的标签。目测不用。

  多参数的列子如下：

	@register.filter()
	def news_op(status, id):
	    if status & config.mSohuConf['A_mask']:
	        output = '<a href="/xxx/%d/%d/" title="xxx">xxx</a>'%(news_id, status)
	    else:
	        output = '<a href="/xxx/%d/%d/" title="xxx">xxx</a>'%(news_id, status)
	    return mark_safe(output)
	    
	模板：
	{{item.status|news_op:item.id}}

   毕竟还是不太方便。

[1]: https://docs.djangoproject.com/en/1.7/howto/custom-template-tags/   "Custom template tags and filters"