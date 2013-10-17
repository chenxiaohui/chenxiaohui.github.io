---
layout: post
title: "记几个诡异的bug"
date: 2013-10-12 15:57
comments: true
categories: oceanbase
---

### ERROR: mutli target patterns

<s>这个莫名其妙啊，不知道在Makefile.am里改了什么，然后就这样，网上的解释大部分是说target里面有多余的冒号，但是我发现问题啊。最后该来该去bug没了，但是也复现不出来，只是在这里记一下，如果有复现的时候再说。</s>

后来 [聿明](http://weibo.com/leslieyuchen "阿里聿明") 解决了这个问题，原来是编译的线程开太多了，而开发机性能又不好，争用然后冲突。
	
	alias make='make -s -j 4' #这里开到4-5就不要更多了

<!-- more -->

### ob集群无法启动

怀疑是机器的问题，但是如果大部分机器我都无法启动这算怎么一回事，

rs的日志如下：

	[2013-10-12 14:41:56.484203] WARN  create_first_table (ob_root_bootstrap.cpp:164) [140296887187200] fail to create e
	mpty tablet. table_id=111 err=-54
	[2013-10-12 14:41:56.484272] WARN  bootstrap_first_table (ob_root_bootstrap.cpp:130) [140296887187200] fail to creat
	e first_tablet_entry's tablet. err=-54
	[2013-10-12 14:41:56.484289] ERROR do_bootstrap (ob_root_server2.cpp:582) [140296887187200] bootstrap first root table error, err=-54
	[2013-10-12 14:41:56.484302] ERROR boot_strap (ob_root_server2.cpp:565) [140296887187200] bootstrap failed! ret: [-54]
	[2013-10-12 14:41:56.484314] INFO  ob_root_server2.cpp:570 [140296887187200] ObRootServer2::bootstrap() end:ret[-54]
	[2013-10-12 14:41:56.484325] INFO  ob_root_worker.cpp:3129 [140296887187200] admin cmd=16, err=-54
	[2013-10-12 14:41:56.484339] WARN  do_admin_without_return (ob_root_worker.cpp:3252) [140296887187200] not supported admin cmd:cmd[16]

cs的日志如下：

	ERROR do_request (ob_chunk_service.cpp:451) [139992810493696] service not started, only accept start schema message or heatbeat from rootserver.
	[2013-10-12 14:41:56.480804] INFO  ob_tablet_image.cpp:3133 [139993389482080] begin scan report_tablet_list size:0
	[2013-10-12 14:41:56.481673] INFO  ob_general_rpc_stub.cpp:259 [139993389482080] report tablets over, send OB_WAITING_JOB_DONE message.
	[2013-10-12 14:41:56.482303] INFO  ob_tablet_manager.cpp:987 [139993389482080] tablet report. typeset=51
	[2013-10-12 14:41:56.482321] INFO  ob_tablet_image.cpp:3133 [139993389482080] begin scan report_tablet_list size:0
	[2013-10-12 14:41:56.483331] INFO  ob_general_rpc_stub.cpp:259 [139993389482080] report tablets over, send OB_WAITING_JOB_DONE message.
	[2013-10-12 14:41:56.483670] ERROR do_request (ob_chunk_service.cpp:470) [139992810493696] call func error packet_code is 219 return code is -1026

ms的日志如下：

	[2013-10-12 14:41:56.510527] WARN  create (../../src/common/hash/ob_hashtable.h:302) [139726122704928] create buckets fail
	[2013-10-12 14:41:56.527871] WARN  init (../../src/common/ob_kv_storecache.h:1755) [139726122704928] create map fail
	 ret=-1 num=5543383
	[2013-10-12 14:41:56.527890] ERROR init (ob_sql_query_cache.cpp:217) [139726122704928] KeyValueCache init error, ret: 1
	[2013-10-12 14:41:56.527897] ERROR initialize (ob_mysql_server.cpp:151) [139726122704928] ObSQLQueryCache init error, ret: 1
	[2013-10-12 14:41:56.527906] WARN  start (ob_mysql_server.cpp:508) [139726122704928] initialize failed ret is 1
	[2013-10-12 14:41:56.527913] ERROR do_work (ob_merge_server_main.cpp:172) [139726122704928] obmysql server start failed,ret=1
	[2013-10-12 14:41:56.527982] INFO  ob_mysql_server.cpp:611 [139726122704928] server stoped.

<s>create_bucket失败，这个也不能总是说内存的问题吧...莫非是大部分开发机都资源不足？我靠谁干的....</s>

确认了 ms 起不来是因为内存分配失败的问题 感谢 [瑶瓔](http://www.weibo.com/u/1912538231 "瑶瓔") 的辛苦debug

###关于border_flag

border_flag这事情是很早遗留的问题了，[@日照师兄](http://weibo.com/chuanhui85 "阿里日照") 说过，大概是border_flag和min/max对象两套东西一起在用，目前看直接不要用border_flag的MIN/MAX位就好了，比对的时候会直接跟min/max对象比对的，而忽略了border_flag。但是毕竟有些地方没改过来，比如：

	int ObRootTabletInfo::split_tablet(const ObReplica & replica)
	{
	  int ret = OB_ERROR;
	  if (replica.meta_.range_.start_key_ == meta_info_.range_.start_key_)
	  {
	    if (replica.meta_.range_.end_key_ < meta_info_.range_.end_key_)
	    {
	      meta_info_.range_.border_flag_.unset_min_value(); #这里需要设置
	      meta_info_.range_.start_key_ = replica.meta_.range_.end_key_;
	      ret = OB_SUCCESS;
	    }
	  }
	  if (OB_SUCCESS != ret)
	  {
	    TBSYS_LOG(WARN, "split tablet error:tablet[%s], replica[%s]", to_cstring(meta_info_.range_),
	        to_cstring(replica.meta_.range_));
	  }
	  return ret;
	}
	
如果split的时候一个tablet已经置位MIN/MAX了，现在分裂的时候后一部分（原tablet split之后的那部分）已经不是MIN-MAX，但是置位还在，就悲催了。

钦此。