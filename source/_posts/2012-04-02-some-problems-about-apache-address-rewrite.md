---
title: Apache地址重写的几个问题
author: Harry Chen
layout: post

categories:
  - PHP
tags:
  - .htaccess
  - httpd.conf
  - rewrite
  - 地址重写
---
# 

Apache地址重写的配置分为两种方式即通过httpd.conf配置和.htaccess文件。

首先要打开rewrite模块windows下的配置是

> LoadModule rewrite_module modules/mod_rewrite.so

httpd.conf的配置可以全局生效也可以只配置一个目录需要做的事情是在相应目录的Directory标签下配置Rewrite规则。

.htaccess的则放到相应目录下或者根目录即可这是VPS里常用的一种方式毕竟作为一个VPS购买者不可能要求提供商去更改全局配置文件。这种方式需要注意的有如下两点

首先.htaccess要想起作用必须要在httpd.conf中相应的Directory标签下配置AllowOverride All默认是None其次是windows下这种无文件名仅有扩展名的文件是无法直接生成的可以在cmd窗口下使用copy con命令来生成这命令也有年头了我小学的时候还学过光阴荏苒啊扯远了…Ctrl Z保存。

![image][1]

然后我们说一下几个概念。

首先是RewriteEngine这是地址重写的引擎可以方便的设置为On或者Off来启用和关闭引擎。

其次是RewriteCond地址重写的条件符合这个条件的才进行表达式判断和重写这样能有效减少匹配的条数提高重写效率。

最后是RewriteBase和RewriteRuleRewriteBase指明重定向地址的基础即RewriteRule后一部分重定向地址会拼合上RewriteBase合成一个完整的重定向地址。这在一个web容器下有多个网站的时候比较有用。

RewriteRule才是我们讨论的主要话题。RewriteRule实现把符合表达式的地址重定向到另一个地址的功能RewriteRule的语法类似于下面

> RewriteRule ^forum-([0-9] )-([0-9] )\\.html$ forumdisplay.php?fid=$1&page=$2

RewriteRule紧跟着判断表达式之后是需要重定向的位置正则表达式()会捕获一个分组然后通过$n引用这个分组从而实现地址重写。RewriteRule匹配的开始位置是整个URL去掉当前目录后剩下的部分比如我在/discuz配置上面所示的RewriteRule然后输入一个URL-http://localhost/discuz/forum-1-1.html被用来匹配的输入会是forum-1-1.html也就是前面的/discuz/被吃掉了。对于整个问题我们可以用如下的语句验证。

> RewriteRule ^(.*)/forum-([0-9] )-([0-9] )\\.html$ rewrite.php?param=$1
>
> 注在rewrite.php里打印一下GET['param’]参数

另外这里需要说明的是如果我定义了

> RewriteBase /discuz

那么前面的^forum-([0-9] )-([0-9] )\\.html$不受影响但是后面会变成/discuz/forumdisplay.php?fid=$1&page=$2。不过RewriteBase并不是必须的若有指定RewriteBase结果为RewriteBase 重定向地址否则为当前目录 重定向地址。这里当前目录指的是.htaccess所在目录使用.htaccess的时候或者Directory标签指定的目录使用httpd.conf的时候。

以上操作在windows下测试通过。

参考文献

[1]Apache中RewriteCond规则参数介绍

[http://hi.baidu.com/һ/blog/item/ace7f14e19851cc4d0c86af2.html][2]

[2]RewriteRule-htaccess详细语法使用教程

[http://www.3code.cn/rewriterule-htaccess详细语法使用教程/][3]

   [1]: http://www.roybit.com/wp-content/uploads/2012/04/image_thumb.png (image)
   [2]: http://hi.baidu.com/%D2%BB/blog/item/ace7f14e19851cc4d0c86af2.html
   [3]: http://www.3code.cn/rewriterule-htaccess%E8%AF%A6%E7%BB%86%E8%AF%AD%E6%B3%95%E4%BD%BF%E7%94%A8%E6%95%99%E7%A8%8B/
