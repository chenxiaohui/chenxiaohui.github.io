---
layout: post
title: "通过脚本统计代码覆盖率"
date: 2013-10-16 20:56
comments: true
categories: oceanbase
---

  只是记录一下工作里面的一些trick。我发现我对这些trick的兴趣无比的高。

  我们有时候需要在开发机上统计代码覆盖率，这可能是做测试的同学经常的工作，做开发的同学也难免会遇到。对于某些分支复杂的逻辑，代码覆盖工具是极大的助力。
	
  关于gcc coverage选项和gcov/lcov工具的使用已经在 [上篇文章](http://cxh.me/2013/10/16/test-coverage-percentage-statistics/ "测试覆盖率统计")里面说过了，我们这里说的是如何实现方便的统计和拉取数据并显示。

<!-- more -->

  首先，测试目录和代码目录是分开的，我们在测试目录运行的时候会生成测试文件的代码覆盖率统计，但是实际上被测试的文件的代码覆盖率是在源码目录生成的。这是需要注意的一点，之前我考虑过合并两处的代码覆盖率统计文件，后来发现没有必要，毕竟你关注的是源码目录的统计文件。这样我们通过如下脚本实现代码覆盖率的生成和拉取。

	#!/bin/bash
	if [ $# = 1 ] ;then
	    lcov --capture --directory . --output-file $1.info --test-name $1
	    lcov --remove $1.info "/usr*" -o $1.info # remove output for external libraries
	    genhtml $1.info --output-directory ~/$1_output --title "$1" --show-details --legend
	    rm $1.info
	    tar czvf ~/$1.tar.gz ~/$1_output
	    rm -rf ~/$1_output
	else
	    echo 'cover.sh <testname>'
	fi

  解释几点：

  1. 第四行目的是去掉usr相关的统计，毕竟跟我们没关系。生成的代码打包到HOME目录下。

  2. 可能会报.gcda文件目录出错，找不到要创建的目录的错误，这种主要用于跨平台情况。
这个是由于.gcda文件的生成默认保存到.o所在的目录，但是如果.o所在目录不存在，就会出现错误。
设置环境变量可以解决这个问题。设置GCOV_PREFIX=/target/run' 同 GCOV_PREFIX_STRIP=1
则生成的.gcda文件 将会保存到 /target/run/build/foo.gcda。

  3. 有时候会遇到"Merge mismatch for summaries" 的错误，可以将.gcda全部删除或者对整个文件全部编译，而不是单个改变的文件，这个是由于gcda与gcno不相配导致的，因为两者之间都有个时间戳用来记录是不是相同的。

  然后是关于拉取到本地的问题，直接在bashrc里面配置如下别名好了：

	alias getcov="from 你的测试用例.tar.gz && tar zxvf xxx.tar.gz && cd xxx"

	function from() {m
	 scp -r 你的用户名@$你的开发机:$@ .
	}
	alias html='google-chrome http://localhost:8000; python -m SimpleHTTPServer'

  这样getcov拉取覆盖率文件，html命令建立webserver并打开浏览器，小trick，用起来舒服而已。

----------------------

  擦，我不得我提醒各位，有时候发现修改了case之后覆盖率并没有提升，这一定不是你的问题，不一定是coverage数据没有更新的问题，不一定是数据没有拉取成功的问题，极有可能是浏览器缓存了数据的问题。

  针对这种问题，我们的解决方法就是：

  **作死地按f5**