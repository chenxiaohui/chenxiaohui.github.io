---
layout: post
title: "oceanbase源码分析-RootServer主要框架"
date: 2013-09-02 12:55
comments: true
categories: oceanbase源码分析
---

##BaseMain

BaseMain的逻辑从start开始,首先定义了日志格式(ob_easy_log_format),具体定义在ob_easy_log.cpp中
日志格式如何使用需要跟到Libeasy里去看了.

之后parse_cmd_line解析命令行参数.既然继承自同一个基类,那么这几个server的启动函数就非常相似

之后是一些启动琐事,建立pid文件,建立log文件,设置log级别等.有些地方引用到了TBsys和libeasy,如果需要了解的话可以跟进去看看.

start的最后注册了signal ,并调用do_work开始逻辑.do_work需要子类重载实现.
restart处理了重启的问题. 

##ObServerConfig
	主要是读取系统配置,包含一个oibsystemconfig的指针

##ObSystemConfig
	系统配置,键值对和resultset形式


##ObRootMain
继承自common下的BaseMain,定义了RootServer的启动流程

ObRootMain的几个主要成员:
#RootServerConfig 
	定义了rootserver的配置
		继承自obServerConfig

ReloadConfig 
	
ConfigManager
	
ObRootWorker
	很大的一个类,包含了rootserver的几乎所有逻辑,ObRootMain设置一些配置项之后调用ObRootWorker的start



	还有一部分代码格式错乱的 clustermanager/ocm_admin.cpp中



#ObRootReloadConfig




