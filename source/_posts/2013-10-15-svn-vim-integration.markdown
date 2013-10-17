---
layout: post
title: "svn vim 整合方案"
date: 2013-10-15 11:53
comments: true
categories: oceanbase
---

这也是实际工作中遇到的问题，所以还是分类到了oceabase分类里面。

遇到的情况是这样的，有可能同时做多个任务的修改，或者说上一个任务的修改并未提交（尚未ship不能提交），但是下一个已经修改了，这样的话，post-review的时候是需要管理post列表的，而不能把所有的修改一起post。之前应该写过一篇文章说一个post-review插件的实现，但是实际上颇为不便，最好的办法是直接在vim里面操作一个修改列表。这里我们首先通过如下方式生成修改列表。
<!-- more -->

	alias sta='st|grep ^A '
	alias stm='st|grep ^M '
	alias std='st|grep ^D '
	alias po='echo "#!/bin/sh" >post-review.sh && echo "post-review \\" >>post-review.sh  && sta >> post-review.sh ; std >>post-review.sh; stm >> post-review.sh ; vi post-review.sh'

之后可以得到类似如下所示的post-review.sh，当然这个是不能直接运行的。

	#!/bin/sh
	post-review \
	M       tests/rootserver/root_table/iterator/test_ob_server_tablet_iter.cpp
	M       tests/rootserver/root_table/iterator/test_ob_root_replica_iter.cpp
	M       tests/rootserver/root_table/iterator/test_ob_server_replica_iter.cpp
	M       tests/rootserver/root_table/iterator/test_iterator_base.h
	M       tests/rootserver/root_table/iterator/Makefile.am
	M       tests/rootserver/root_table/iterator/test_ob_root_table_iter.cpp
	M       tests/rootserver/root_table/iterator/run.sh
	M       tests/rootserver/root_table/iterator/test_ob_alive_root_table_iter.cpp

我们面临两个问题：

1. 每行的格式都略有差别，比如前面有A/M/D标记，后面没有续行符号\，没有空格什么的。
2. 需要能够针对每一行或者多行进行svn操作（svn diff/revert 应该是最常见的操作）

这里我们通过vim脚本实现如下的功能：

svn.vim 实现如下

	function! StripSVN() range
	    "Step through each line in the range...
	    for linenum in range(a:firstline, a:lastline)
	        "Replace loose ampersands (as in DeAmperfy())...
	        let curr_line   = getline(linenum)
	        let replacement = substitute(curr_line,'^\(A\|M\|D\)','','g')
	        call setline(linenum, replacement." \\")
	    endfor
	    call cursor(linenum)
	    "Report what was done...
	    if a:lastline > a:firstline
	        echo "Strip Svn" (a:lastline - a:firstline + 1) "lines"
	    endif
	endfunction
	function! SVNCommand(cmd, prompt, combine) range
	    if a:prompt
	        let sure = input("Are you sure? (y/n) ")
	        if sure != 'y'
	            return
	        endif
	    endif
	    let cmd = '!svn '.a:cmd
	    for linenum in range(a:firstline, a:lastline)
	        "Replace loose ampersands (as in DeAmperfy())...
	        let curr_line   = getline(linenum)
	        let replacement = substitute(curr_line,'^\(A\|M\)','','g')
	        let replacement = Trim(Trim(replacement,'\\'),' ')
	        if a:combine
	           let cmd = cmd.' '.replacement.' '
	        else
	            let cmd = '!svn ' . a:cmd. ' ' . replacement
	            execute cmd
	            "echo cmd
	        endif
	    endfor
	    if a:combine
	        execute cmd
	        "echo cmd
	    endif
	endfunction

第一个函数处理每行的格式，第二个函数读取每行的内容，生成命令并执行，prompt=1 的时候会提示并让用户确认， combine=1 的时候所有行会拼成一条执行，否则每行执行一次。

然后在vimrc中添加：

	noremap <leader>sp :call StripSVN()<CR>
	noremap <leader>sf :call SVNCommand("diff", 0 ,1)<cr>
	noremap <leader>sr :call SVNCommand("revert", 1 ,0)<cr>dd
	noremap <leader>sl :call SVNCommand("log", 0 ,0)<cr>
	noremap <leader>sa :call SVNCommand("add", 0 ,1)<cr>
	noremap <leader>sb :call SVNCommand("blame", 0 ,1)<cr>
	noremap <leader>sd :call SVNCommand("delete", 1 ,0)<cr>dd

这样实现了两种操作，n状态下在当前行执行操作，v状态下在选中的所有行执行操作。
---------------------

其实偶然发现我好像没说怎么用，大致流程是这样的：

1. po(alias)，生成修改列表
2. 在每个行，或者选中多个行执行svn命令(<leader>sf,<leader>sr什么的)，查看diff啊，回滚啊，查看log啊，查看blame啊
3. 提交前选中所有行执行<leader>sp， 去掉行首的A/M/D标记，在行尾加续行符
4. 执行post-review.sh提交

------------------------------------------

参考文献：

> [1] SVN 命令参考（svn command reference）, <http://riaoo.com/subpages/svn_cmd_reference.html>

> [2] 使用脚本编写 Vim 编辑器, <http://www.ibm.com/developerworks/cn/linux/l-vim-script-2/>
