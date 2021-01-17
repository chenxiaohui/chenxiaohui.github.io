---
layout: article
title: "vim7.4 && vimgdb编译"
date: 2014-06-09 10:52
comments: true
categories: "vim"
---
  首先，你下载的vim7.4代码的一般结构跟常见的工程是不一样的，主要体现在configure不会生成Makefile，make的时候是通过Makefile的配置生成config.h的，也就是说你想的好好的希望如下操作：

	 ./configure --prefix=$HOME --with-features=huge --enable-multibyte --enable-pythoninterp --enable-cscope --enable-fontset --enable-gdb --enable-largefile \
	 --enable-gui=gnome2 \
	 --enable-luainterp \
	 --enable-tclinterp \
	 --with-python-config-dir=/usr/lib/python2.7/config-x86_64-linux-gnu  #编译配置
	 --with-lua-prefix=/usr/local/bin/lua

	    make && make install

  来编译的话，那么实际配置跟上面configure里面是没有关系的。

  以你需要做的是修改Makefile，打开必要的开关，比如安装目录，lua支持什么的

	# Uncomment the next line to install Vim in your home directory.
	prefix = $(HOME)
	# LUA
	# Uncomment one of these when you want to include the Lua interface.
	# First one is for static linking, second one for dynamic loading.
	# Use --with-luajit if you want to use LuaJIT instead of Lua.
	# Set PATH environment variable to find lua or luajit executable.
	CONF_OPT_LUA = --enable-luainterp
	#CONF_OPT_LUA = --enable-luainterp=dynamic
	#CONF_OPT_LUA = --enable-luainterp --with-luajit
	#CONF_OPT_LUA = --enable-luainterp=dynamic --with-luajit


  其他的操作按如下步骤就行，摘自[larrupingpig/vimgdb-for-vim7.4](https://github.com/larrupingpig/vimgdb-for-vim7.4 "vimgdb")：

### vimgdb install

  You need:

  vim-7.4.tar.bz2 <http://www.vim.org/sources.php>

  vimgdb-for-vim7.4 (this patch) <https://github.com/larrupingpig/vimgdb-for-vim7.4>

  Untar all files, apply the patch and make Vim:

	tar xjvf vim-7.4.tar.bz2 -C /tmp

	tar xzvf vimgdb-for-vim7.4.tar.gz -C /tmp

	cd /tmp

	patch -p0 < vimgdb-for-vim7.4/vim74.patch

	cd vim74/src

	make

	sudo make install

### Install vimGdb runtime:

  Copy the file vimgdb_runtime found in the vimgdb tarball, to your runtime path. To find your runtime path location execute the vim command (this is usually $HOME/.vim): :set runtimepath?

	cp -rf /tmp/vimgdb-for-vim7.4/vimgdb_runtime/* ~/.vim

  Change to the doc directory, start Vim and run the ":helptags ." command to process the taglist help file. Without this step, you cannot jump to the taglist help topics. You can now use the ":help vimgdb" command to get the vimGdb documentation.
