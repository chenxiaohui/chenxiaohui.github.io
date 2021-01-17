---
title: 'C#配置文件读写的两种思路'
author: Harry Chen
key: two-methods-to-deal-with-config-file-using-csharp
layout: article

categories:
  - .Net
tags:
  - INI
  - XML
  - 序列化
  - 配置文件
---

  配置文件是增加软件扩展性不可获取的一部分。本文提供两种C#配置文件读写的方式。

  第一种是使用Windows自身的INI文件读写API，在.NET下调用的时候需要对其进行声明，这也是最传统的一类，问题在于INI文件表达能力有限，每次都要费心地去给每个不同的配置项设置不同的KEY，不适合LIST型的配置项的书写。

  另一种是使用XML序列化与反序列化。这里只是用XML作为一个例子，其实.NET下的几种序列化方式[1]都可以用来作为配置文件读写的一种方式。XML的表达能力强于INI文件，同时序列化方式也大大简化了配置文件读写的过程，确是一种方便的工具。

  详见[代码][1]。

参考文献：

 [1]C#序列化技术详解（转），

