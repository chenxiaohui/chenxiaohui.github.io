---
layout: post
title: "vim配置符号和跳转"
date: 2015-03-28 12:05
comments: true
published: true
categories: "vim"
---
  
    对于一个简单的开发环境，能实现tags的定位跳转，以及查询就够用了。这种情况下，vim + 一些插件完全能够满足要求，尤其对于python这样的脚本语言开发，vim比IDE更简洁。这里我们尝试把vim配置成一个精简的IDE。

  首先升级你的ctags，换成exuberantCtags，后者功能更强大，且对c++等语言的支持更好。

    ubuntu下可以直接：
    	apt-get install exuberant-ctags 
    centos下：
    	yum install ctags
    mac下：
    	brew install ctags-exuberant
    windows下：
    	什么是windows?

  cscope如果系统没有默认安装的话也装一下。

  之后安装tags插件，相对[taglist.vim][2]其实我们更推荐[tagbar.vim][1]，因其对面向对象特性支持的更好。

<!--more-->

  然后配置tagbar，第一部分只是配置了下system标记，效果如图所示:

	" system mark
	if(has("win32") || has("win95") || has("win64") || has("win16"))
	    let g:system='win'
	else
	    if has("unix")
	        let s:uname = system("uname")
	        if s:uname == "Darwin\n"
	            let g:system='mac'
	        else
	            let g:system='unix'
	        endif
	    endif
	endif

  	"{{{ tagbar - taglist replacement
		nmap <silent><S-f8> :TagbarToggle<CR>
		if g:system=='win'
		    let g:tagbar_ctags_bin = 'ctags.exe'
		else
		    let g:tagbar_ctags_bin = 'ctags'
		endif
		let g:tagbar_autoclose = 1
		let g:tagbar_width = 30
		let g:tagbar_autofocus = 1
		let g:tagbar_sort = 0
		let g:tagbar_compact = 1
		let g:tagbar_autofocus = 1
	"}}}

  {% img img-polaroid center /images/2015/tagbar.vim "tagbar界面" "tagbar界面" %}

  现在有了tag显示，我们希望能够自动加载tags，这样打开一个文件的时候就可以直接操作这个文件所在项目的tags了，针对这种情况，需要先定义一个项目的根目录，这就需要用到base_dir_mark（只是一个变量..名字你随便），我们对一个项目生成且只生成一次tags(和cscope.out)，放在这个目录下。我（改进）的插件cscope_maps.vim包含了对base_dir_mark的查找和定义：

	if !exists('g:base_dir_mark')
	    "set base_dir_mark to indicate where to generate tags
	    let g:base_dir_mark = 'tags'
	endif

	function! GetBaseDirectory()
	    let max = 5
	    let dir = getcwd()
	    let i = 0
	    while isdirectory(dir) && i < max
	        if filereadable(dir .'/'. g:base_dir_mark)
	            return dir.'/'
	        endif
	        let idx = strridx(dir, '/')
	        let dir = dir[:idx-1]
	        let i = i + 1
	    endwhile
	    return ''
	endf

	function! AutoLoadCTagsAndCScope()
	    silent! execute 'cs kill -1'

	    let base_dir=GetBaseDirectory()
	    if !empty(base_dir)
	        silent! execute 'cs add ' .base_dir . 'cscope.out'
	    endif

	    let ctags_dir=base_dir
	    if !empty(ctags_dir)
	        silent! execute 'set tags =' . ctags_dir . 'tags,'.$VIMFILES.'/tags/'.&ft.'/tags'
	    else
	        silent! execute 'set tags ='.$VIMFILES.'/tags/'.&ft.'/tags'
	    endif
	endf

  之后就可以配置让每次打开一个文件的时候都自动去项目根目录下找tags(和cscope.out)，把这个目录作为项目根目录了。

  	" {{{ plugin -ctags 对tag的操作
	set tags=tags
	augroup TagGroup
	    autocmd!
	    "autocmd BufEnter *.* :exec 'set tags=tags,'.$VIMFILES.'/tags/'.&ft.'/tags'
	    autocmd BufEnter * :call AutoLoadCTagsAndCScope()
	    "autocmd BufWritePost *.cpp,*.c,*.h :silent! execute "!ctags -R  -c++-kinds=+p --fields=+iaS --extra=+q ."
	augroup END
	"}}}

  注释掉的一行，我们放到shell中实现

  	alias cr='find `pwd` -name "*.[ch]" -o -name "*.cpp" > cscope.files && ctags -R `pwd` --languages=c++ --c++-kinds=+px --fields=+iaKSz --extra=+q && cscope -Rb && rm -f cscope.files'

  这样在项目根目录执行一下cr来生成tags和cscope.out，这个操作同时确定了项目的根目录是哪里。至于自动更新tags，意义不是很大，而且开销有点高。

  最后是cscope的插件绑定，插件详见这个[github repo][3]。配置如下：

	"{{{ plugin - cscopemaps.vim里面定义了键盘映射
	let g:base_dir_mark = 'tags'
	map <silent><F7> :call AutoLoadCTagsAndCScope()<CR>
	map <silent><C-F7> :call Do_CsTag()<CR>
	"map <F3> <C-]>
	map <F3> :execute(":tj ".expand("<cword>"))<cr>
	map <m-left> <C-o>
	map <m-right> <c-i>

	"map <silent><S-F4><Esc>:!ctags -R *<CR>
	"map <silent><C-F4><Esc>:silent! execute "!ctags -R -c++-kinds=+p --fields=+iaS --extra=+q ."<CR>
	"查找调用这个定义
	"nmap <C-\>g :cs find g <C-R>=expand("<cword>")<CR><CR>
	"查找调用这个c符号的地方
	nmap <leader>cf :cs find c <C-R>=expand("<cword>")<CR><CR>
	nmap <leader>ck :cs find s <C-R>=expand("<cword>")<CR><CR>
	nmap <leader>cg :cs find g <C-R>=expand("<cword>")<CR><CR>
	nmap <leader>ct :cs find t <C-R>=expand("<cword>")<CR><CR>

	"查找调用这个函数的地方
	"nmap <C-\>c :cs find c <C-R>=expand("<cword>")<CR><CR>
	"}}}
  
  这样就实现了在tag的跳转和查找。 Do_CsTag函数实现的功能跟shell alias基本一样。没有安装neocomplcache的可以map <m-left> <C-t>。效果如下所示：

  {% img img-polaroid center /images/2015/tags.png "自动load tags" "自动load tags" %}	
  {% img img-polaroid center /images/2015/cscope.png "cscope find reference结果" "cscope find reference结果" %}

  	


[1]: http://www.vim.org/scripts/script.php?script_id=3465   "Tagbar : Display tags of the current file ordered by scope"
[2]: http://www.vim.org/scripts/script.php?script_id=273 "taglist.vim : Source code browser (supports C/C++, java, perl, python, tcl, sql, php, etc) "
[3]: https://github.com/chenxiaohui/vim_cscope "vim_cscope - a vim plugin to configure vim_cscope"

###Bibliography:

>\[1] Tagbar : Display tags of the current file ordered by scope, <http://www.vim.org/scripts/script.php?script_id=3465>

>\[2] taglist.vim : Source code browser (supports C/C++, java, perl, python, tcl, sql, php, etc) , <http://www.vim.org/scripts/script.php?script_id=273>

>\[3] vim_cscope - a vim plugin to configure vim_cscope, <https://github.com/chenxiaohui/vim_cscope>