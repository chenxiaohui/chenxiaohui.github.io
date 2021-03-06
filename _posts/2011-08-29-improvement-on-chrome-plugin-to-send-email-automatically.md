---
title: 对Chrome自动发送邮件插件的改进
author: Harry Chen
key: improvement-on-chrome-plugin-to-send-email-automatically
layout: article

dsq_thread_id:
  - 1254528969
categories:
  - Web
  - 与技术相关
tags:
  - Chrome
  - 发送邮件
  - 插件
---
# 

  针对之前那个插件存在的一些问题，这两天又做了一点改进。主要的功能改进包括：

> 1 如果直接点击右键，那么获取当前网页的链接，然后跳转到一个服务器的页面，发送邮件完成之后自动关闭。
>
> 2 如果选择了文字再点击邮件，那么程序通过ajax将所选文字发送到一个服务，发送邮件完成之后弹出提示。

  过程中遇到过几个主要问题，这里与大家共勉一下：

> 1 有的虚拟主机的设置不允许Get参数里包含http://（不明所以，不知道怎么设置的），后来程序先把http替换成ptth，再替换回来，这样就绕过了这个问题。
>
> 2 ajax的错误提示可以通过responseText打印出来，这样方便很多调试，当然jquery就会方便很多。
>
> 3 js关闭窗口的代码window.close在不同浏览器里会有不同的问题[1]。
>
> 4 正常情况下ajax无法跨域访问，但是Chrome插件里Background.html里是可以跨域访问的。

  代码[这里][1]下载，不做过多解释了。哎，最近得好好折腾一下开题了。

参考文献：

[1] JavaScript无提示关闭窗口(兼容IE/Firefox/Chrome),

