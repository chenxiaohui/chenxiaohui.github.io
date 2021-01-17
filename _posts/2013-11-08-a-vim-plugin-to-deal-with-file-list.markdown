---
layout: article
title: "自己写的一个根据路径打开文件的插件"
date: 2013-11-08 21:26
comments: true
categories: "vim"
---

  这个其实修改了很多次，最初的目的是在linux下嘛，找电影不方便，只能用locate打印出一个电影列表来，但是每次复制路径到命令行多不方便啊，最好能在vim里面操作，于是想想干脆做成通用的好了，就有了这个filelist.vim

<!-- more -->

	"=============================================================================
	"     FileName: filelist.vim
	"         Desc:
	"       Author: ChenXiaohui
	"        Email: sdqxcxh@gmail.com
	"     HomePage: http://www.cxh.me
	"      Version: 0.0.1
	"   LastChange: 2013-11-06 20:31:23
	"      History:
	"=============================================================================
	function! GetCmd(type,line)
		let cmd=get(g:applist,a:type)
		if empty(cmd)
			let cmd=get(g:applist,'default')
		endif
		"no %
		if cmd[0] != '!' && cmd[0] != ':'
			let cmd='!nohup '.cmd.' '.Trans(a:line).' >/dev/null 2>&1 &'
	    else
			let cmd=substitute(cmd,'%',Trans(Trans(a:line)),'g')
		endif

		"let cmd=substitute(cmd,'%<',a:line,'g')
		return cmd
	endfunction

	function! OpenFileWithDefApp()
		let cmd=''
		let origin_line = Trim(Trim(getline("."),'\\'), ' ')

	    let idx = stridx(origin_line,':')
	    echo idx
	    if idx > -1
	        let line = strpart(origin_line, 0, idx)
	        let linenum = strpart(origin_line, idx)
	    else
	        let line = origin_line
	    endif

	    if !filereadable(line)
			"Directory
			let cmd=GetCmd('pwd',line)
		else
			let idx=strridx(line,".")
			"has no ext
			if idx==-1
				let cmd=GetCmd('default',line)
			else
	            let fileExt = tolower(matchstr(line,'\.\w\+'))
				let fileExt=tolower(strpart(fileExt,1))
				for [exts,app] in items(g:applist)
					let supportExt=split(exts,',')
					if index(supportExt,fileExt)>=0
						let cmd=GetCmd(exts,line)
					endif
				endfor
			endif
		endif

		if empty(cmd)
			let cmd=GetCmd('default',line)
		endif
	    execute cmd
	    if exists('linenum')
	        execute linenum
	        execute ':call Vm_toggle_sign()'
	        "execute ':set cursorline'
	        "normal V
	    endif
	endf

	function! DelFile ()
		let line=getline(".")
		if !filereadable(line)
			"echo "!rm -ri ".Trans(getline("."))
			:execute "!rm -ri ".Trans(getline("."))
		else
			"echo "!rm -i ".Trans(getline("."))
			:execute "!rm -i ".Trans(getline("."))
		endif
		:del
	endf

	function! CopyFile()
		let cmd=''
		let line=getline(".")

		if !filereadable(line)
			"Directory
			let cmd='!cp -a'.Trans(line).' '.Trans(g:dst_dir)
		else
			let cmd='!cp '.Trans(line).' '.Trans(g:dst_dir)
		endif
		:execute cmd
	endf

	function! ChDir()
		let cmd=''
		let line=getline(".")

		if !filereadable(line)
			"Directory
			let cmd=':cd '.Trans(line)
		else
			let cmd=':cd '.Trans(DirName(line))
		endif
		:execute cmd
		":echo cmd
		:sh
	endf

	function! DirName(line)
		let idx=strridx(a:line,'/')
		return strpart(a:line,0,idx)
	endf

	function! Trans(line)
	    let line=Trim(a:line, ' ')
		let line=substitute(line,"'","\\\\'","g")
		let line=substitute(line,' ','\\ ','g')
		let line=substitute(line,'!','\\!','g')
		let line=substitute(line,'#','\\#','g')
		let line=substitute(line,'&','\\&','g')
		let line=substitute(line,'(','\\(','g')
		let line=substitute(line,')','\\)','g')
		return line
		"return "'".line."'"
		"return "'".substitute(a:line,"'","'\\\\''","g")."'"
	endf
  
  原理还是很简单的，分析当前行，得到文件路径，根据类型找到关联命令，然后替换关联命令得到最后的shell命令并执行。就是一堆转义比较罗嗦，在vimrc里面定义关联程序信息：

	" plugin- deal with filelist
	nnoremap <leader>co :call OpenFileWithDefApp()<cr>
	nnoremap <leader>rm :call DelFile()<cr>
	nnoremap <leader>cd :call ChDir()<cr>
	nnoremap <leader>to :call CopyFile()<cr>
	let g:dst_dir="/media/cxh/MY MP3/"
	let g:applist={
	            \'pdf':'evince',
	            \'png,gif,jpg':'eog',
	            \'rmvb,mkv,flv,avi,mp4,m4v':'mplayer',
	            \'rar':'!unrar l %',
	            \'epub':'!calibre %',
	            \'zip':'!unzip -O CP936 -l %',
	            \'pwd':'nautilus',
	            \'docx,xlsx,pptx,ppt':'libreoffice',
	            \'default':':e %'
	            \}
	
  需要特别说明的是：

  1. 几个函数的作用分别是调用执行程序打开当前文件，删除，到当前文件所在路径下，和copy当前文件到制定的dst_dir（这个我主要用在替代windows下的发动到移动存储介质用了）
  2. applist是类型-程序关联数组，说明一下，%会被替换成当前行所指定的文件路径。如果applist里面的命令既不是!开头（shell执行）也不是:开头（vim内部命令），就会被转换成类似于：!nohup mplayer /media/xx.rmvb >/dev/null 2>&1 &的命令，相当于windows的调用默认程序打开。
  3. 支持这种形式的行号调用 xxx.cpp:123 默认用:e 打开之后会定位到对应行，然后标红，标红使用三种方式：**visualmark**, **cursorline**和**normal V**，第一种需要[安装插件][1]

  钦此。

[1]: http://www.vim.org/scripts/script.php?script_id=1026 "Visual Mark : Visual mark, similar to UltraEdit's bookmark"

#### 参考文献:

  \[1] Visual Mark : Visual mark, similar to UltraEdit's bookmark, <http://www.vim.org/scripts/script.php?script_id=1026>
