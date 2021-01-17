---
title: 正则表达式匹配器的实现
author: Harry Chen
key: implement-of-regular-expression-matcher
layout: article

dsq_thread_id:
  - 1273908025
categories:
  - 软件发布
tags:
  - 匹配器
  - 正则表达式
---

  这里实现了一个正则文法匹配器。其中正则文法是使用正则表达式实现的。正则表达式是我们平时经常使用的一种文法工具，各种编程工具里都有正则表达式的匹配器。Linux下的Grep工具也是一种正则文法的匹配器实现。

  我们这里给出正则文法的形式定义

![wenfa][1] 这个定义是有二义的，消除二义之后的定义形式如下所示：

![wefa1][2] 算法的基本思路如下所示：

![suanfa][3] 类图如下所示：

![sdf][4] 另，为了效果能更友好，使用了Latex的几个宏包，无法打包进代码里，所以想要运行请安装CTex套装，代码在CTex2.5以上版本运行通过。

  文档和可执行文件[这里][5]下载，代码[这里][6]下载。

 参考文献:

  \[1]: John E. Hopcroft, Rajeev Motwani, Jeffrey D. Ullman，Introduction to Automata Theory, Languages, and Computation[M]，2nd Edition. Addison Wesley Press, November 24, 2000.

  \[2]: 罗贵明，自动机与形式逻辑课件[EB/OL]，清华大学软件学院，2010。

  \[3]: 高仲仪，金茂忠，编译原理及编译程序构造[M]，北京航空航天大学出版社，1990-12。

  \[4]: Alfred V.Aho, Monica S.Lam, Ravi Sethi, Jeffrey D.Ullman, Compilers: Principles, Techniques, and Tools (2nd Edition)[M]，Addison Wesley Press,2009-1.

  \[5]: The TikZ and PGF manual, Example: State machine[EB/OL],  ,2006-11-08

  \[6]: 如何将正则表达式转化为自动机[EB/OL]，.


[1]: John E. Hopcroft, Rajeev Motwani, Jeffrey D. Ullman，Introduction to Automata Theory, Languages, and Computation[M]，2nd Edition. Addison Wesley Press, November 24, 2000.
[2]: 罗贵明，自动机与形式逻辑课件[EB/OL]，清华大学软件学院，2010。
[3]: 高仲仪，金茂忠，编译原理及编译程序构造[M]，北京航空航天大学出版社，1990-12。
[4]: Alfred V.Aho, Monica S.Lam, Ravi Sethi, Jeffrey D.Ullman, Compilers: Principles, Techniques, and Tools (2nd Edition)[M]，Addison Wesley Press,2009-1.
[5]: The TikZ and PGF manual, Example: State machine[EB/OL],  ,2006-11-08
[6]: 如何将正则表达式转化为自动机[EB/OL]，.

