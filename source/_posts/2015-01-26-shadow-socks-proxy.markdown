---
layout: post
title: "使用shadow socks翻墙"
date: 2015-01-26 15:39
comments: true
published: true
categories: "其他"
---
  
   拜GFW所赐，连tm boot2docker都连接不上了。而且最近红杏抽风，遂决定买[shadowsocks][1]服务翻墙。服务直接在官网购买，90一年，比红杏略便宜一点，主要还是可控性比较大，因为是socks5的代理。

  [这里][1]购买服务，一年99，这个优惠码可以再打一点折`imouto985`。之后进入后台可以看到分配给自己的密码，服务器主要是日本，美国和新加坡的，实测貌似日本的响应更快一点。

  {% img img-polaroid center /images/2015/shadow_mac.png %}

  mac下下载了客户端直接打开配置好地址就能用，linux下需要自己配置代理。

  首先下载安装node.js

  	wget http://nodejs.org/dist/v0.10.35/node-v0.10.35.tar.gz
  	tar zxvf node-v0.10.35.tar.gz 
  	cd node-v0.10.35
  	./configure && make 
  	sudo make install

  然后安装npm和shadowsocks

  	sudo apt-get install npm
  	sudo apt-get install shadowsocks

  apt-get安装的nodejs好像有问题，所以用源码安装。编辑配置文件，默认是`/usr/local/lib/node_modules/shadowsocks/config.json`，启动之后就可以连上服务器了。

  之后需要配置proxy。以chrome为例，如果之前配置过goagent的话，基本配置一样。不过proxy switch sharp终于升级到了proxy switch omega了。需要注意的是shadowsocks是socks代理，选择的时候不要选择http。gfwlist 可用如下：

  	https://autoproxy-gfwlist.googlecode.com/svn/trunk/gfwlist.txt

  之后就可以翻墙了。最后说一句：**Fxxk GFW，祝病魔早日战胜方校长，所有参与GFW的人都将钉在历史的耻辱柱上**。


[1]: https://portal.shadowsocks.com/aff.php?aff=483   "shadow socks"
[2]: https://shadowsocks.com/   "Shadowsocks.com"