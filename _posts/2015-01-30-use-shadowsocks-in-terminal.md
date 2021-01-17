---
layout: article
title: "在命令行使用Shadowsocks翻墙"
key: use-shadowsocks-in-terminal
date: 2015-01-30 18:13
comments: true
published: true
categories: "其他"
---
  拜GFW所赐，连tm boot2docker都连接不上了。好在有shadowsocks的服务，可以转成http proxy给命令行使用。

  首先安装[privoxy][1]。Linux下直接`apt-get install privoxy`，然后编辑配置文件（etc/privoxy/config)：

    forward-socks5   /               127.0.0.1:1080 .
	listen-address  localhost:8118
	#local network do not use proxy
	forward         192.168.*.*/     .
    forward            10.*.*.*/     .
    forward           127.*.*.*/     .


  基本上上这两项就可以了。之后在shell配置下代理，详见[参考文献2][2]：

  	export http_proxy='http://127.0.0.1:8118'
	export https_proxy='http://127.0.0.1:8118'


  最后chkconfig设置下开机启动。Mac下略微麻烦一些。主要是配置开机启动。详见[参考文献3][3]。至于Mac下的Shadowsocks，还是ShadowsocksX比较方便，跟Linux下一样，都是会在1080启动监听。

[1]: http://www.privoxy.org/   "Privoxy"
[2]: http://cxh.me/2015/01/11/linux-proxy-setup/ "通过搭建代理来共享网络"
[3]: http://blog.devtang.com/blog/2012/12/08/use-privoxy/ "使用Privoxy做智能代理切换"

###Bibliography:

  \[1] Privoxy, <http://www.privoxy.org/>

  \[2] 通过搭建代理来共享网络, <http://cxh.me/2015/01/11/linux-proxy-setup/>

  \[3] 使用Privoxy做智能代理切换, <http://blog.devtang.com/blog/2012/12/08/use-privoxy/>
