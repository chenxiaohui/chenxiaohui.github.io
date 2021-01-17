---
layout: article
title: "分布式调试之导入import文件"
key: vim-script-to-find-import-file
date: 2013-11-19 17:41
comments: true
categories: "Oceanbase"
---
  最近看元启师兄写了一个脚本更新所有重构之后的include引用，我暂时没有需要如此伤筋动骨的代码，所以暂时用不上。但是有时候引用一个类要去找所在的文件，而有时候经常会记错地方。写了一个简单的vim插件依赖ctags来找对象或函数所在的位置。代码如下：

<!-- more -->

	if !exists('g:base_dir_mark')
	    "set base_dir_mark to indicate where to generate post-review.sh
	    let g:base_dir_mark = 'tags'
	endif

	if !exists('g:strip_prefix_arr')
	    "set base_dir_mark to indicate where to generate post-review.sh
	    let g:strip_prefix_arr = ['rootserver', 'root_table']
	endif

	if !exists('g:import_token')
	    "set base_dir_mark to indicate where to generate post-review.sh
	    let g:import_token = 'import "%s"'
	endif

	function! GetImportFile()
	    let filepath = expand("%:p")
	    let base_dir = GetBaseDirectory() . 'src/'
	    let idx = stridx(filepath, base_dir)
	    if idx == 0
	        let import_file_name = strpart(filepath, len(base_dir))
	        let import_cmd = substitute(g:import_token, '%s', import_file_name, 'g')
	        for prefix in g:strip_prefix_arr
	            let import_cmd = substitute(import_cmd, prefix.'/', '', 'g')
	        endfor
	        let @" = import_cmd
	        echo import_cmd
	    endif
	endf

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


  前提是配置好你的ctags，然后在系统根目录下用

	ctags -R * //其他语言
	ctags -R  -c++-kinds=+p --fields=+iaS --extra=+q . //c++
 
  生成tags，插件会去去找tags文件，然后把找到的位置定义为项目目录，之后的引用路径会按照这路径来生成相对路径。strip_prefix_arr制定要去掉的前缀，比如我们的路径是/home/dev/src/rootserver/xxx.h，tags生成在dev下，按照base_dir_mark/src去掉项目路径得到 rootserver/xxx.h，根据strip_prefix_arr去掉rootserver，最后得到import "xxx.h"。