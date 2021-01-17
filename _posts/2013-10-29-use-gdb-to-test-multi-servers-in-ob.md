---
layout: article
title: "分布式调试之用gdb调试分布式系统"
key: use-gdb-to-test-multi-servers-in-ob
date: 2013-10-29 13:40
comments: true
categories: "Oceanbase"
---

  分布式系统开发的时候我们最经常遇到的问题就是，从一个server发送了一条报文之后怎么在另一个server查看这条报文的处理逻辑是否正确，单机的debug都不是问题，但是多机debug怎么做呢？

  在ob团队里面，正常情况下我们有如下三种方式处理这些问题：

  1. 做mock，写单测，隔离开集群环境
  2. 加调试日志，部署集群环境，看日志。
  3. 非daemon模式下通过gdb调试。

  这里我们详细说一下第三种。这也是最有效果的一种。

<!-- more -->

  需要强调的是，正常情况下ob启动之后各个server会以守护进程方式运行，这时候如果用gdb启动server的话，gdb不知道在fork之后跟哪个进程，而在我测试下，[set follow-fork-mode][1]貌似也没成功过。

  所以最好的方法是直接不要通过守护进程启动，我们在部署ob到home目录下，集群名用ob1，.gdbinit里面写入：

	cd ~/ob1
	file bin/rootserver
	set args -r 10.235.162.8:3500 -R 10.235.162.8:3500 -i eth0 -C 1 -N
	break "/home/xiaohui.cpc/roottable_dev/src/rootserver/ob_root_worker.cpp:2053"
	break "/home/xiaohui.cpc/roottable_dev/src/rootserver/ob_root_worker.cpp:941"

  参数里面加-N表示不以daemon方式启动。

  这样通过gdb可以启动rootserver，然后同样启动其他需要的server，就可以调试在gdb里面看到程序执行后停在断点的位置。启动脚本如下，这里我们只启动了chunkserver。

  	#!/bin/bash
	rs_ip=10.235.162.8
	rs_port=3500
	cs_port=3501
	ups_port=3502
	ms_port=3503
	freeze_port=3504
	mysql_port=3505
	net=bond0
	appname=ob1.xiaohui.cpc
	no_daemon=-N

	#bin/rootserver -r $rs_ip:$rs_port -R $rs_ip:$rs_port -i $net -C 1 $no_daemon
	bin/chunkserver -r $rs_ip:$rs_port -p $cs_port -n $appname -i $net $no_daemon

	#bin/updateserver -r $rs_ip:$rs_port -p $ups_port -m $freeze_port -i $net $no_daemon
	#bin/mergeserver -r $rs_ip:$rs_port -p $ms_port -z $mysql_port -i $net $no_daemon

	#bin/rs_admin -r $rs_ip -p $rs_port set_obi_role -o OBI_MASTER
	#bin/rs_admin -r $rs_ip -p $rs_port -t 60000000 boot_strap $no

  断点命中的情况如图1所示：
  
  ![](/assets/images/2013/gdb_multi_server.png "图1：断点命中的情况" "图1：断点命中的情况")
  
  唯一的问题是gdb有时候会退出，如图2。感觉上是rpc超时了？

  ![](/assets/images/2013/gdb_quit.png "图2：gdb退出" "图2：gdb退出")

  感谢玩大数据的[颜然师兄][2]提供非daemon方式启动的方法。


[1]: http://www.ibm.com/developerworks/cn/linux/l-cn-gdbmp/ "使用 GDB 调试多进程程序"
[2]: http://weibo.com/hanfooo "韩富晟 支付宝颜然，玩大数据的，OceanBase工程师"

#### 参考文献:

  \[1] 使用 GDB 调试多进程程序, <http://www.ibm.com/developerworks/cn/linux/l-cn-gdbmp/>

  \[2] 韩富晟 支付宝颜然，玩大数据的，OceanBase工程师, <http://weibo.com/hanfooo>
