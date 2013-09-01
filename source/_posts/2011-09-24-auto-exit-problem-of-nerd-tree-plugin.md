---
title: Nerd_Tree插件自动退出
author: Harry Chen
layout: post
permalink: /auto-exit-problem-of-nerd-tree-plugin/
dsq_thread_id:
  - 1259618836
categories:
  - vim
tags:
  - Nerd_tree
  - taglist
  - 自动退出
---
# 

我们知道（不知道也没事）Taglist插件有自动退出功能，即只剩下一个文件的时候，即使Taglist窗口开着，在主窗口用:q的时候会同时退出Taglist窗口，而Nerd_Tree默认并没有这个功能，我们可以仿照Taglist插件来给Nerd_Tree插件天上这个功能。

首先插入如下代码


    " Exit Vim itself if only the taglist window is present (optional)
    let s:NERDTreeBufName = 'NERD_tree_'
    	augroup Exit_onlywindow
    		"当进入Nerd_Tree的buffer时也检测是否需要退出
    		exec "autocmd BufEnter ". s:NERDTreeBufName .
    		\"* call :Tlist_Window_Exit_Only_Window()"
    		autocmd BufEnter __Tag_List__ nested
    		\ call s:Tlist_Window_Exit_Only_Window()
    	augroup end

然后把Tlist_Window_Exit_Only_Window的函数拷贝进去


    " Tlist_Window_Exit_Only_Window
    " If the 'Tlist_Exit_OnlyWindow' option is set, then exit Vim if only the
    " taglist window is present.
    function! s:Tlist_Window_Exit_Only_Window()
        " Before quitting Vim, delete the taglist buffer so that
        " the '0 mark is correctly set to the previous buffer.
        if v:version < 700
    	if winbufnr(2) == -1
    	    bdelete
    	    quit
    	endif
        else
    	if winbufnr(2) == -1
    	    if tabpagenr('$') == 1
    		" Only one tag page is present
    		bdelete
    		quit
    	    else
    		" More than one tab page is present. Close only the current
    		" tab page
    		close
    	    endif
    	endif
        endif
    endfunction

OK了，看看效果吧