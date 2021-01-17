---
layout: article
title: "gtest在mac上链接的问题"
key: gtest-bug-on-mac
date: 2015-02-06 20:39
comments: true
published: true
categories: "mac"
---

  gtest鉴于google自己的风格，不提供make install，直接make完之后配置路径链接就行，在linux上这样是ok的：

  	g++  -I$GTEST_DIR/include -I$GTEST_DIR -c $GTEST_DIR/src/gtest-all.cc
	g++ -I$GTEST_DIR/include -I$GTEST_DIR -c $GTEST_DIR/src/gtest_main.cc

	ar -rv libgtest.a gtest-all.o
	ar -rv libgtest_main.a gtest_main.o

	c++ -g -Wall -Wextra -pthread  -isystem $GTEST_DIR/include  -c -o RemoveElement.o RemoveElement.cpp
	c++ -g -Wall -Wextra -pthread  -isystem -isystem $GTEST_DIR/include/include -c -o SameTree.o SameTree.cpp

  在mac下这里会报错：architecture x86_64。关键我一直理解gest_main是包含main函数的gtest，gtest-all是不包含的，知道发现官方的makefile执行的时候是这样的 

  	ar rv gtest_main.a gtest-all.o gtest_main.o   

  用这里的gtest_main.a做libgtest_main.a就行了。不理解为什么在mac上单独打包一个gtest_main.o为什么不行。论坛貌似有人贴了一个patch，不看了，回家，碎觉。
