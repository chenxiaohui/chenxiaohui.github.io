---
title: doxygen生成项目调用关系
layout: article
key: doxygen_call_graph
date: 2021-02-19 14:53
---


如果要看一个项目的调用关系，可以考虑一些IDE工具，比如正版source insight等，嗯，正版。

但是毕竟兼容性不好。可以考虑doxygen来生成一份，作为参考，主要还是靠看代码和调试。

首先 doxygen -g 生成配置。实测下面这些是需要补充在Doxyfile的


	HAVE_DOT               = YES
	EXTRACT_ALL            = YES
	EXTRACT_PRIVATE        = YES
	EXTRACT_STATIC         = YES
	CALL_GRAPH             = YES
	CALLER_GRAPH           = YES
	DISABLE_INDEX          = YES 
	GENERATE_TREEVIEW      = YES
	RECURSIVE              = YES


最后doxygen Doxyfile可以看最终效果。比如这个是rocksdb的一个简单调用关系图。
