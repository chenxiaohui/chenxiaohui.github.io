---
title: 支持上传文件的xhEditor for Typecho EX插件
author: Harry Chen
layout: post

dsq_thread_id:
  - 1258318670
categories:
  - 软件发布
tags:
  - Typecho
  - xhEditor
  - 文件上传
---
# 

  Typecho是一套超轻量的开源博客，界面简洁，功能紧凑，但是Typecho的文本编辑器实在是不好，需要自己写html代码，插图也不方便。试用了几个插件，发现TinyMCE回车总有问题，每次保存就多几个空行，其他几个插件也有类似问题。于是就想能不能把xhEditor这个强大的可视化HTML编辑器移植过去，后来找到一个xhEditor for Typecho插件，下载地址在[这里][1]，作者主页。这个插件不支持上传图片，而插件使用之后系统本身的插图功能就不能用了，所以导致图片只能贴网络图了。

  于是决定在这个插件基础上改进，主要是

> 增加了图片/多媒体文件上传功能
增加More标签直接插入功能
修改三种工具栏模式，保证每种模式都有查看源码、Preview和More标签按钮
更新xheditor到最新版1.1.13

  你可能需要在admin/css/typeecho.source.css里改一下body的一个默认颜色，否则导致上传图片的弹窗左边的字显示为白色而看不到。需要说明的是，这一版More标签没有直接的可视化效果，点了之后请到源码里查看，以后有时间再做效果。另外，没时间给More做个小图标了，直接用了显示源码的那个按钮的图标。

  有bug请留言。谢谢。下载地址:[XhEditor for Typecho EX][2]

   [1]: http://115.com/file/atedbyls
   [2]: http://www.roybit.com/wp-content/uploads/2012/03/XhEditor-for-Typecho.rar (XhEditor for Typecho)
