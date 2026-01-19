---
layout: article
title: "maven download dependency挂住的问题"
key: maven-download-stuck
date: 2015-04-19 22:08
comments: true
published: true
categories: "Java"
---
  
  今天迁移工程到mac上，准备以后用mac作为主开发工具。迁移maven的时候发现，maven download会停在那里，如下：

![](https://harrychen.oss-cn-beijing.aliyuncs.com/blog-images/2015/maven_error.jpg)

   解决如下：

1. 怀疑http_proxy问题，去掉系统环境变量。无效
2. 怀疑shadowsocks问题，关掉，无效。
3. maven配置问题，对比了默认配置，没什么错误的地方。
4. 怀疑服务器问题，换成开源中国的maven源，ok，就是慢点。
5. 继续等待，几分钟后报错： java.net.SocketException: Malformed reply from SOCKS server，似乎还是代理的问题。
6. 查阅发现java还有自己的代理配置，见[参考文献][1]，去掉代理。貌似还是无效。
7. 索性重启，搞定。

[1]: https://www.java.com/en/download/help/proxy_setup.xml   "How do I configure proxy settings for Java?"