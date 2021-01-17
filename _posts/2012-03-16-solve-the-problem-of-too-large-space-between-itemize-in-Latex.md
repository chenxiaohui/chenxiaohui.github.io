---
title: 解决Latex中Itemize距离过大的问题
author: Harry Chen
key: solve-the-problem-of-too-large-space-between-itemize-in-Latex
layout: article

dsq_thread_id:
  - 1255023816
categories:
  - Latex
tags:
  - Itemize
  - Latex
  - paralist
  - 行距
---

  默认的itemize存在行距过大的问题，大概是如下的样子：

![image][1]

  用paralist包可以减少行距，代码如下

> \usepackage{paralist}
\let\itemize

   [1]: http://www.roybit.com/wp-content/uploads/2012/03/image_thumb2.png (image)
