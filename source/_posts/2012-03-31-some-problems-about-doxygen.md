---
title: Doxygen几个小问题，mark一下
author: Harry Chen
layout: post
permalink: /some-problems-about-doxygen/
dsq_thread_id:
  - 1341183078
categories:
  - Others
tags:
  - doxygen
  - gbk
  - visual assist x
  - 乱码
---
# 

首先是在Visual Assist X中的配置，在Snippet Editor窗口修改一下file header的snippet和Refactor Document Method的snippet.

![image][1]

设置分别如下

file header

/**
* @file $FILE_BASE$.$FILE_EXT$
* @Synopsis $end$
* @author 你的名字,你的邮箱
* @version $version$
* @date $DAY$:$MONTH$:$YEAR$
*/

Refactor Document Method

/* —————————————————————————-*/
/**
* @Synopsis $SymbolName$
* $end$
* @Param $MethodArg$
*
* @Returns $SymbolType$
*/
/* —————————————————————————-*/
然后记得DoxygenWizard的这个工作目录是一定要点选的，这里有个触发，如果直接复制路径进去是无法run doxygen的。

![image][2]

最后是中文编码的问题，如果你的项目是GBK编码，那么要防止乱码必须要做的事情是设置工程为UTF-8编码，而设置输入为GBK。切记。

![image][3]

![image][4]

   [1]: http://www.roybit.com/wp-content/uploads/2012/03/image_thumb5.png (image)
   [2]: http://www.roybit.com/wp-content/uploads/2012/03/image_thumb6.png (image)
   [3]: http://www.roybit.com/wp-content/uploads/2012/03/image_thumb7.png (image)
   [4]: http://www.roybit.com/wp-content/uploads/2012/03/image_thumb8.png (image)
