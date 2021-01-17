---
title: Vim 的MiniBufExplorer插件改进
author: Harry Chen
key: improvements-of-minibuf-explorer-plugin
layout: article

dsq_thread_id:
  - 1260004543
categories:
  - vim
  - 随笔
tags:
  - bufexplorer
  - Minibufexplorer
  - vim
  - 切换
  - 右键
---
# 

  首先，VI(M)是一种信仰。

  然后扯一下关于MiniBufExplorer插件，主要的作用是实现缓冲区之间的切换，比BufExplorer更加小巧，界面如图所示，下载链接在这里

  ![image][1]

  这个插件在windows下使用的问题主要是在切换的时候会切换到一个No Name的初始缓冲区，这样我本来打开了三个文件，却总在四个文件直接来回切换，同时默认的:bd删除缓冲区命令和:q关闭文件命令在windows下也存在一些问题，:bd不能关闭最后的窗口，:q又直接关闭几个缓冲区。

  针对如上问题，做以下的改进

  > 1 修改MiniBufExplorer插件的切换代码，切换时不停留在No Name缓冲区
  > 2 在_vimrc文件中重新绑定关闭快捷键的代码，加入窗口数的判断

  针对第一个问题，我们修改minibufexpl.vim里的如下代码


    " Skip any non-modifiable buffers, but don't cycle forever
    " This should stop us from stopping in any of the [Explorers]
    while (getbufvar(l:curBuf, '&modifiable') == 0 || bufname('%')=='') && l:origBuf != l:curBuf


  主要是bufname为空（初始缓冲区）的时候再跳转一次。

  针对第二个问题，我们在_vimrc文件中重定义绑定和退出函数


    " 如果只有一个窗口，那么直接退出
    function! CustomExit()
    	if (winbufnr(2) == -1)
    		q
    	else
    		bd
    	endif
    endfunction

    nmap wq :w:call CustomExit()
    nmap q :call CustomExit()
    nmap w :w
    nmap x :bd!:call CustomExit()


    nnoremap  :MBEbn
    nnoremap  :MBEbp


  最后，为了windows下使用方便，可以配置一下右键，请在regedit中添加如下项，然后默认值设置为"E:\Vim im73\gvim.exe" -p –remote-silent "%1"，gvim路径请自行修改

![image][2]

  这样就可以用右键菜单打开gvim，打开两个以上文件的时候，可以用shift l shift h切换左右菜单，q退出文件等等。

   [1]: http://www.roybit.com/wp-content/uploads/2011/09/image_thumb.png (image)
   [2]: http://www.roybit.com/wp-content/uploads/2011/09/image_thumb1.png (image)
