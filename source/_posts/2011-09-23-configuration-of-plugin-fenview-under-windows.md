---
title: FencView插件在windows下的配置
author: Harry Chen
layout: post
permalink: /configuration-of-plugin-fenview-under-windows/
dsq_thread_id:
  - 1257610554
categories:
  - vim
tags:
  - fencview
  - iconv
  - libiconv
  - vim
  - Windows
  - 编码
---
# 

坦白的讲，我没觉得这插件有什么用……

FencView的作用是Auto detect the file encoding. 自动探测编码，防止乱码的插件。但是_vimrc设置了内部编码之后，至少在Windows下我没遇到什么明显的乱码……


    set encoding=utf-8
    set fileencodings=utf-8,gb2312,gb18030,gbk,ucs-bom,cp936,latin1 " 如果你要打开的文件编码不在此列，那就添加进去
    set termencoding=utf-8

Windows下这插件主要的问题是找不到iconv，也正常，这么华丽丽的编码转换工具必然是linux下的，不过我们可以下载Libiconv for Windows，这样就可以在win下使用iconv了，下载地址如下：

然后记得配置一下环境变量

![image][1]

当然你可能遇到找不到库的问题……去刚才的页面下载Dependencies吧

   [1]: http://www.roybit.com/wp-content/uploads/2011/09/image_thumb2.png (image)
