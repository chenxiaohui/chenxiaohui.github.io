---
title: chrome自动发送邮件插件
author: Harry Chen
layout: post

dsq_thread_id:
  - 1258066965
categories:
  - PHP
  - Web
  - 与技术相关
tags:
  - Chrome
  - 发送邮件
  - 插件
---
# 

写这个插件的最初的原因是实验室的网络无法同步Chrome书签，同时有时候需要与宿舍的笔记本同步一些文本信息，所以琢磨自己写一个同步插件。

但是偌大一个教育网，竟然找不到一个可用的在线存储服务，金山快盘已经叫嚣要开放API很久了，但是就是没见到官方的API手册。最后想来想去，干脆用邮件算了，最终的 程序结构如下：

![程序结构][1]

Chrome插件的开发参考了ClickTrans[1]的开发，源码可以在[这里][2]下载，使用的时候在浏览器里右键，就会有Save选项，如果选择了文本，就把文本发送到邮件，否则发送当前链接地址。具体实现不解释，可以参考代码，简单说下Chrome插件的一些东东。

Chrome插件实际上是一组JS的脚本 配置文件，可能还有Html的页面，Chrome本身提供一些API接口，剩下的就通过JS来操作页面元素实现。Chrome插件里比较重要的两个东东，一个是页面，包括了BackGround页，Popup页（Popup页又分Page_Action和Browser_Action），另一个是向页面注入的JS脚本。因为插件自己的脚本并不能直接操作Web页，所以必须要向页面注入一个脚本才能进行页面操作。Chrome的API可以通过这里[2]查询，自己的脚本和注入脚本之间的通信参见ClickTrans[1]的文章。

最后不得不提的一个东西，JS本身是无法实现SMTP协议的，或者说没人做，需要发送邮件的时候必须借助其他Web语言，通过服务的形式调用，我是写了一个简单的PHP响应请求并发送邮件的程序，具体代码如下，重要的不是代码，而是PHP下mail的配置，详见配置win下的sendmail[3]


    

Chrome插件的代码里固定了一个邮件服务的地址，localhost/test/send.php，如果需要请自行更改然后打包，有空再做成可配置的，然后放到SinaAppEngine上，这样就方便访问了，否则总得本地起服务，太费劲了。

参考文献

[1] 从无到有制作Chrome扩展：ClickTrans，



[2] Chrome扩展API参考，

[3] php mail函数在win下的使用，以及配置win下的sendmail



   [1]: http://www.roybit.com/wp-content/uploads/2011/08/thumb.png (程序结构)
   [2]: http://www.roybit.com/wp-content/uploads/2011/08/chrome%E6%8F%92%E4%BB%B61.rar
   [3]: http://www.php.net/if
   [4]: http://www.php.net/mail
   [5]: http://www.php.net/echo
   [6]: http://www.php.net/else
