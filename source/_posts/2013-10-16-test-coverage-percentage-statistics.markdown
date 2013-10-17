---
layout: post
title: "测试覆盖率统计"
date: 2013-10-16 10:15
comments: true
categories: oceanbase
---

**什么是代码覆盖率(code coverage)

代码覆盖（Code coverage）是软件测试中的一种度量，描述程式中源代码被测试的比例和程度，所得比例称为代码覆盖率。

代码覆盖主要包括如下四个方面：

1. 语句覆盖(StatementCoverage)
2. 判定覆盖(DecisionCoverage)
3. 条件覆盖(ConditionCoverage)
4. 路径覆盖(PathCoverage) 或者叫条件/判断覆盖率

具体的参见参考文献[1] [2].

**怎么得到覆盖率数据

这里我们主要说测试工具的使用的问题。c++的项目测试里面我们用gcc产生测试数据，用gcov和lcov生成测试结果的报表。

<!-- more -->

gcc这里需要做的工作是编译的时候打开coverage选项，主要是如下几步。

1. 编译的时候，增加 -fprofile-arcs -ftest-coverage 或者 –coverage；
2. 链接的时候，增加 -fprofile-arcs 或者 –lgcov；
3. 打开–g3 选项，去掉-O2以上级别的代码优化选项；否则编译器会对代码做一些优化，例如行合并，从而影响行覆盖率结果；

为了方便的在Makefile里面控制是否生成测试覆盖率数据，我们在Makefile里面加入如下开关

	ifeq ($(coverage), yes)
		CXXFLAGS       +=  -fprofile-arcs -ftest-coverage
		LINKERCXX      +=  -fprofile-arcs -ftest-coverage
		OPT_FLAGS     =  -g3
	endif

这样就可以通过make coverage=yes生成。

同理如果用automake工具的话，Makefile.am里面需要加入如下语句：

	if COVERAGE
		CXXFLAGS+=-fprofile-arcs -ftest-coverage
		AM_LDFLAGS+=-lgcov
		OPT_FLAGS =  -g3
	endif

configure.ac/configure.in脚本里面需要加入

    AC_ARG_WITH([coverage],
           AS_HELP_STRING([--with-coverage],
		          [with coverage (default is NO)]),
	   		  [
			    if test "$withval" = "yes"; then
			    	coverage=yes
			    fi
			  ],
			  [coverage=no]
	   )
	AM_CONDITIONAL([COVERAGE], test x$coverage = xyes )

就可以通过

	./configure --with-coverage来生成Makefile了

之后我们可以通过gcov/lcov工具来显示覆盖率的结果，使用帮助参见参考文献[3] [4]。至于如何在去开发机拉取结果/一些小技巧和容易出现的问题，请看[下一篇博客](http://cxh.me/2013/10/16/user-script-to-get-coverage/ "通过脚本统计代码覆盖率")。

[1] http://www.cnblogs.com/coderzh/archive/2009/03/29/1424344.html "代码覆盖率浅谈"
[2] http://zh.wikipedia.org/wiki/%E4%BB%A3%E7%A2%BC%E8%A6%86%E8%93%8B%E7%8E%87 "代码覆盖率"
[3] http://sdet.org/?p=212 "Linux下c/c++项目代码覆盖率的产生方法"
[4] http://www.cnblogs.com/turtle-fly/archive/2013/01/09/2851474.html "[整理] gcov lcov 覆盖c/c++项目入门" 

###参考文献

>[1] 代码覆盖率浅谈，<http://www.cnblogs.com/coderzh/archive/2009/03/29/1424344.html>

>[2] 代码覆盖率，<http://zh.wikipedia.org/wiki/%E4%BB%A3%E7%A2%BC%E8%A6%86%E8%93%8B%E7%8E%87>

>[3] Linux下c/c++项目代码覆盖率的产生方法，<http://sdet.org/?p=212>

>[4] [整理] gcov lcov 覆盖c/c++项目入门, <http://www.cnblogs.com/turtle-fly/archive/2013/01/09/2851474.html>
