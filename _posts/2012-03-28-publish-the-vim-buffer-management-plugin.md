---
title: 发布VIM缓冲区切换插件buf_it升级版
author: Harry Chen
layout: article

dsq_thread_id:
  - 1262682716
categories:
  - vim
tags:
  - buf_it
  - gvim
  - Windows
  - 优化
  - 缓冲区
---
# 

  VIM默认使用的过程中有一个重要的问题，就是打开多个文件的时候无法可视化看到打开的文件，并在这些文件中切换。MiniBufExplorer是一个常用的buffer切换插件，但是这个插件在Windows下使用的时候有许多问题，同时也太繁琐。buf_it[1]则实现了轻量的buffer管理，但是buf_it同样在windows下有许多问题，而buf_it的退出机制也会出现只想关闭一个文件确关闭了整个vim的情况。

  基于这两个问题，我修改了buf_it插件，这里共享出来，欢迎大家提意见。先给张图

![image][1]

  修改：

> 1 windows下使用GVIM优化，方式多开一个空白缓冲区，windows下gvim右键配置见参考文献2
>
> 2 增加自定义退出方式
>
> 3 修改了部分快捷键，只是个人习惯，可无视之

  安装：

> 直接扔到plugin目录就行，原作者没写doc，那我也不写啦。

  配置：

    nnoremap wq :w:call BufClose()
    nnoremap q :call BufClose()
    nnoremap w :w
    nnoremap x :bd!:call BufClose()

  使用：

> shift h,l ：左右切换tab
>
> be ：BufEcho 显示当前缓冲区名字
>
> bo ：只保留当前缓冲区，其他的都关掉
>
> alt i : 切换到序号为i的缓冲区
>
> wq: 保存关闭当前缓冲区并退出
>
> q: 关闭当前缓冲区并退出
>
> w: 保存当前缓冲区
>
> x: 不保存关闭当前缓冲区

  下载:[buf_it][2]

参考文献：

[1] buf_it : Buffer list in statusline,

[2] 在windows下给你的右键菜单添加"edit with vim"的方法,

