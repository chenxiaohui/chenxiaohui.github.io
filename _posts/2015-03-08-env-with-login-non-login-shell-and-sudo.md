---
layout: article
title: "登录非登录shell和sudo的环境变量"
key: env-with-login-non-login-shell-and-sudo
date: 2015-03-08 21:21
comments: true
published: true
categories: "Linux"
---
  关于登陆/非登录/交互/非交互shell的问题见[参考文献1][1]。今天遇到的问题是su/sudo的时候环境变量到底是怎么样的，执行了什么rc文件。

  1. sudo命令是以root的身份执行command命令，但是环境变量还是当前用户的，执行目录也仍然是当前目录
  即环境变量和执行目录都不会切换到root
  2. su - 命令是切换到另一个用户，环境变量会切换到username，执行目录会切换到目标用户username的家目录
  3. su 命令仅切换用户身份，例如从A切换到B，执行whoami命令，显示的是用户B，但当前目录不会切换，
  环境变量也仍未切换，仍为A用户的环境变量
  4. sudo su 只是用sudo的权限来执行su命令，跟su本身一样。
  5. visudo可以配置sudo的继承环境变量

  	Defaults    env_keep =  "COLORS DISPLAY HOSTNAME HISTSIZE INPUTRC KDEDIR LS_COLORS JAVA_HOME PATH"

[1]: http://blog.csdn.net/trochiluses/article/details/13767669   " bash 深入理解：交互式shell和非交互式shell、登录shell和非登录shell的区别"
#### Bibliography:

  \[1]  bash 深入理解：交互式shell和非交互式shell、登录shell和非登录shell的区别, <http://blog.csdn.net/trochiluses/article/details/13767669>
