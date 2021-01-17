---
title: Vim轻量级缓冲区管理插件Buf_it修订版Buf_itv2
author: Harry Chen
key: light-vim-buffer-management-plugin-bufit-v2
layout: article
dsq_thread_id:
  - 1257607419
categories:
  - vim
tags:
  - buf_it
  - vim
format: standard
---
# 

  之前发布了Vim的缓冲区管理插件Buf_it的一个修正版，但是后来发现在windows下命令行使用的时候有问题，同时与Nertree和Taglist等插件也有冲突。于是继续fix了几个bug，然后解决了这部分冲突，新的代码放在我的[github][1]上，或者也可以这里下载，有问题可以继续留言，谢谢。

  效果如下：

![效果图][2]

### 安装：

> 扔进plugin目录就行

### 配置


    nnoremap wq :w:call BufClose(0)
    nnoremap q :call BufClose(0)
    nnoremap w :w
    nnoremap x :call BufClose(1)


### 使用

> shift h,l ：左右切换tab
>
> \be ：BufEcho 显示当前缓冲区名字
>
> \bo ：只保留当前缓冲区，其他的都关掉
>
> alt i : 切换到序号为i的缓冲区
>
> \wq: 保存关闭当前缓冲区并退出
>
> \q: 关闭当前缓冲区并退出
>
> \w: 保存当前缓冲区
>
> \x: 不保存关闭当前缓冲区

### 参考文献：

[1] buf_it : Buffer list in statusline,


[2] 在windows下给你的右键菜单添加”edit with vim”的方法,


