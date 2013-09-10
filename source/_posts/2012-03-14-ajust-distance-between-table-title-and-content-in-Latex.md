---
title: Latex里图片与表格标题与正文距离的调整
author: Harry Chen
layout: post

dsq_thread_id:
  - 1254290451
categories:
  - Latex
tags:
  - Latex
  - 图标
  - 标题
  - 距离
---
# 

首先，我们这里的图表用的分别是figure和table标签，宏包应该是graphicx和??，我们需要调整的距离是其标题(caption)的前后的空白，比如下面图中所示：

![image][1]

首先，我们可以通过如下代码设置这个距离，above设置标题上面的距离，below设置标题下面的距离。

> \setlength{bovecaptionskip}{10pt}
\setlength{elowcaptionskip}{-10pt}

需要特别说明的是一点，网上好像都没有人说这个事情。如果标题在图标的上面的话，这两个距离是反的，这点让人觉得很不适应。

![image][2]

参考文献：

   [1]: http://www.roybit.com/wp-content/uploads/2012/03/image_thumb.png (image)
   [2]: http://www.roybit.com/wp-content/uploads/2012/03/image_thumb1.png (image)
