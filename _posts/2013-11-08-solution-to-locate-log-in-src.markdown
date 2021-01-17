---
layout: article
title: "分布式调试之vim日志定位解决方案"
date: 2013-11-08 21:31
comments: true
categories: "Oceanbase"
---

  做分布式系统看日志解决问题是基本功了，毕竟多个server跑在不同的机器上，即使用gdb能attach到某个进程上，或者[用非daemon模式启动并调试][1]但是case往往很复杂，难以用测试环境完全模拟case，所以大部分情况下还是需要看日志解决问题的。

  不过日志多了之后往往容易跟丢，在浩如烟海的日志里面定位到发生错误的地方也不是见容易的事情。这周大部分时间就费在这上面了（不过还是不熟）。期间写了一个简单的vim插件实现日志的定位。想法如下：

<!-- more -->

  偶然发现通过deploy.py ob1.rs0.less打开less窗口之后按v键可以转到vim窗口，这就解决很多问题了，毕竟我可不想在less下实现什么功能。vim script就熟悉多了。

  ob的log格式是这样的

  	[2013-11-08 20:02:23.698586] WARN  get_schema (ob_root_schema_service.cpp:296) [139800896067328] local schema not inited 

  可以看出关键的地方是打印日志的文件和行数，所以我们用正则\w+.c(pp)*:\d+（vim里需要转义）来匹配日志行，得到所在文件和行数之后用执行ssh命令去开发机的项目下find对应的文件，把找到的结果写入某个特定文件（~/.session)里面，之后写一个插件根据文件中的记录打开对应的文件并标红对应的行即可。

  定位log的vim脚本实现如下：

	if !exists('g:project_base_dir')
	    let g:project_base_dir = '$HOME/dev $HOME/src'
	endif

	if !exists('g:user_name')
	    let g:user_name = 'xxxx'
	endif

	if !exists('g:server_ip')
	    let g:server_ip = 'xx.xx.xx.xx'
	endif

	function! LogSession() range
	    let filearr = []
	    for linenum in range(a:firstline, a:lastline)
	        let curr_line = getline(linenum)
	        let pos_str = matchstr(curr_line,'\(\w\+\)\.c\(pp\)*:\(\d\+\)')
	        let pos_arr = split(pos_str, ":")
	        if !empty(pos_arr)
	            let filename = pos_arr[0]
	            let linenum = pos_arr[1]
	            if index(filearr, filename) == -1
	                "generate file list
	                let session_cmd = "find ". g:project_base_dir ." -name ". filename .' -exec echo "{}"":'.linenum.'" >>~/.session \;'
	                let ssh_cmd = "!ssh ".g:user_name.'@'.g:server_ip." \'".session_cmd."\'"
	                echo ssh_cmd
	                execute ssh_cmd
	                execute ':call Vm_toggle_sign()'
	                call add(filearr, filename)
	            endif
	        endif
	    endfor
	endfunction
  
  解释几点

  * g:project_base_dir定义源码所在目录，如果源码引用了其他的库，最好把其他库的源码目录一并指定。
  * g:user_name 开发机用户名，这是你源码所在机器的用户名
  * g:server_ip 开发机IP，这是你的源码所在机器的IP，保证能够无密码登录。

  这样在测试机看log的less窗口里面按v进入vim（vim脚本需要部署到开发机和测试机各一份），然后在对应的行（或者多行）执行LogSession，对应的文件位置信息就被写入开发机的~/.session文件里面（这个应该可以配置，忘了做了）。

  另开一个窗口ssh到开发及，打开.session，应该类似于如下：

  	/home/xxx.xx/dev/src/rootserver/ob_root_server.cpp:584
	/home/xxx.xx/dev/src/rootserver/ob_root_server.cpp:2183
	/home/xxx.xx/dev/src/rootserver/ob_root_inner_table_task.cpp:175
  
  定位到某一行调用插件打开代码就行，这就涉及到[前文所说的插件了][2]。按照快捷键打开对应的行就行。

  之后在vimrc里面映射键就行了

  	map <leader>ss :call LogSession()<cr>
  	nnoremap <leader>co :call OpenFileWithDefApp()<cr>
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
  
  截图如下：

  ![](/images/2013/three-log.png "log文件" "log文件")

  ![](/images/2013/one-line.png "定位到对应的源码行c" "定位到对应的源码行")

  ![](/images/2013/two-line.png "定位到对应的源码行cpp" "定位到对应的源码行")

[1]: http://cxh.me/2013/10/29/use-gdb-to-test-multi-servers-in-ob/ "用gdb调试分布式系统（OB中的应用）"
[2]: http://cxh.me/2013/11/08/a-vim-plugin-to-deal-with-file-list/ "自己写的一个根据路径打开文件的插件"