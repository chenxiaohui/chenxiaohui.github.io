---
layout: article
title: "node_zk_browser安装时的一个问题"
key: error-with-node-zk-browser
date: 2014-11-19 18:56
comments: true
categories: "分布式系统"
---

  zookeeper基本是基于API和console进行znode的操作，并没有一个比较方便的操作界面，taobao 伯岩大神写过一个工具node_zk_browser，可以比较方便的查询zookeeper信息。地址在

	https://github.com/killme2008/node-zk-browser

  界面如下所示：

  ![](/assets/images/2014/zk_browser.png "zk_browser" "zk_browser")

  安装的时候遇到一个问题

	Downloading zookeeper-3.4.3 from http://apache.mirrors.tds.net/zookeeper/zookeeper-3.4.3/zookeeper-3.4.3.tar.gz

  这个地址是找不到的。apache的这个mirror上只有3.4.6的包了。改package.json也没用。表示不懂node.js，不知道npm去哪里找的url。

  但是我们可以这样绕过去。先到其他的路径下：

  	npm install zookeeper

  这会安装最新的node-zookeeper，安装完毕之后生成一个node_modules目录，下面有一个zookeeper目录，直接复制这个目录到node-zk-browser下面的node_modules目录里。

  搞定。

  

[1]: http://www.blogjava.net/killme2008/archive/2011/06/06/351793.html   "Zookeeper的web管理应用"
[2]: http://blog.izturn.mobi/post/15025383777/node-zookeeper-install-note "node-zookeeper安装小记"

#### 参考文献:

  \[1] Zookeeper的web管理应用, <http://www.blogjava.net/killme2008/archive/2011/06/06/351793.html>
  
  \[2] node-zookeeper安装小记, <http://blog.izturn.mobi/post/15025383777/node-zookeeper-install-note>
