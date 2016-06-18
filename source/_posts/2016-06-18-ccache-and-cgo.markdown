---
layout: post
title: "ccache和cgo并存的问题"
date: 2016-06-18 20:15
comments: true
published: true
categories: "C++"
---

   ccache是加快编译的神器，有了ccache，忘了distcc。但是发现go和c混编的项目里面如果用了cgo的话，go编译的时候ccache会报错。主要是传给ccache的某些参数ccache不认识。错误如下：

   	/usr/bin/ccache: invalid option -- 'd'
	Usage:
	    ccache [options]
	    ccache compiler [compiler options]
	    compiler [compiler options] (via symbolic link)

	Options:
	    -c, --cleanup delete old files and recalculate size counters
	                          (normally not needed as this is done automatically)
	    -C, --clear clear the cache completely
	    -F, --max-files=N set maximum number of files in cache to N (use 0 for
	                          no limit)
	    -M, --max-size=SIZE set maximum size of cache to SIZE (use 0 for no
	                          limit; available suffixes: G, M and K; default
	                          suffix: G)
	    -s, --show-stats show statistics summary
	    -z, --zero-stats zero statistics counters

	    -h, --help print this help text
	    -V, --version print version and copyright information

	See also <http://ccache.samba.org>.
	dpkg-architecture: warning: Couldn't determine gcc system type, falling back to default (native compilation)

  之前都是关了ccache，后来想新的版本能不能搞定呢？有人提了Issue但是没看到release上有啥新的fix。直接升了一下版本：


  	wget https://www.samba.org/ftp/ccache/ccache-3.2.5.tar.bz2
  	bunzip2 ccache-3.2.5.tar.bz2
  	tar xvf ccache-3.2.5.tar
  	cd ccache
  	./autogen.sh
  	./configure
  	make -j 8
  	yum install asciidoc
  	make install

   发现还是一样。后来想可以用shell包一层啊，看[网上][1]有相应的方案：

   	 #!/bin/bash
  	 ccache gcc "$@"

   貌似这样ccache不认识的参数就不传递了？反正是ok了，改天研究下。
   


[1]: https://bbs.archlinux.org/viewtopic.php?id=204639 "ccache does not work with nvcc (CUDA)"