---
layout: post
title: "用来把一个线程的日志输出到单独文件的脚本"
date: 2014-02-14 21:32
comments: true
categories: "Oceanbase"
---

  很多开源项目的日志都是把多个线程的日志打印到一个文件的，有时候我们需要查看一个线程号下的所有日志，vim选中高亮线程号固然是一种方法，但是看起来不直观，以下脚本完成输出一个线程所有日志到一个文件的功能。

	"{{{ plugin-写一个线程的log到单独文件
	function! ThreadLog()
	    let file = readfile(expand("%:p"))
	    let pattern = expand('<cword>')
	    let matches = []
	    for line in file
	        let match = matchstr(line, pattern)
	        if(!empty(match))
	           call add(matches, line)
	        endif
	    endfor
	    let s:filename= pattern . '.log'
	    call writefile(matches, s:filename )
	endf
	nmap <leader>th :call ThreadLog()<cr>
	"}}}

  使用的时候把光标移动到线程号下面，然后,th就行了。实际上完成的是把所有包含当前单词的行都输出到一个文件的功能。文件名是当前单词。目测够用了。

  好久没写博客了，甚觉我已经离文人很远了。在这个欢乐祥和的日子里，实在是觉得生活充满了顾虑。人生就是这么多矛盾啊，不确定是种状态，确定也是种状态，想想之所以依然这么漂泊着，也就是应了一句话：青春逝去，认输之前。当然了，我觉得我还挺青春的。青春这东西，最重要的不是外表，阳光，积极向上什么的。这都是表面。青春是变革，至少是变革的勇气。