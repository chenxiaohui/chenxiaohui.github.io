---
layout: article
title: "关于ob代码规范里面的行末空格"
date: 2013-11-20 10:50
comments: true
categories: "Oceanbase"
---

  行尾的空格在post-review的时候会被标识成红色，其实可以通过如下vim配置直接显示出来并全部去掉：


	" 删除所有行未尾空格
	nnoremap <C-f12> :%s/[ \t\r]\+$//g<cr>''
	"显示空格
	highlight ExtraWhitespace ctermbg=red guibg=red
	match ExtraWhitespace /\s\+$/
	augroup ExtraWhitespaceGroup
	    autocmd!
	    autocmd BufWinEnter * match ExtraWhitespace /\s\+$/
	    autocmd InsertEnter * match ExtraWhitespace /\s\+\%#\@<!$/
	    autocmd InsertLeave * match ExtraWhitespace /\s\+$/
	    autocmd BufWinLeave * call clearmatches()
	augroup END

  这样打开所有文件（其实可以只处理cpp)的时候行尾空格都会变成红色，<Ctrl-F12>可以统一去掉所有的空格。这么做唯一不爽的是如果有未遵从代码规范的文件那么就满篇的红色。比如多隆大神早期的代码....