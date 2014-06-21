---
title: Latex中使用visio的矢量图(转载+修改）
author: Harry Chen
layout: post

dsq_thread_id:
  - 1264827018
categories:
  - Latex
  - 与技术相关
tags:
  - Latex
  - visio
  - 插图
---
# 

  我们知道，visio用来画流程图等专业图很方便，而Latex的专业排版效果是Word所不能比的，而Visio不支持导入eps和dvi格式的矢量图，而导出jpeg毕竟有质量损失，那么怎么才能在Latex中直接使用visio导出的矢量图呢？

1\. Visio可以保存为wmf，emf等矢量图形格式（word的默认插图格式），再转换为eps格式（可使用TpX，由本论坛得知早期版本貌似可直接保存eps）插入LaTeX。可转换后的eps图片格式不稳定，图形易错位；另外Visio使用Windows字体，转换后的eps图形只引用而不包含字体，插入LaTex后由于找不到对应字体，中文（或mathtype公式，特殊符号）会乱码。
2\. 用ps虚拟打印的方式虽然可以解决格式和乱码问题，但中文字符（或其他不支持的内容）会按位图处理，得不到完美的矢量图形。

  经过探索，将visio保存为pdf格式是最完美的解决方式，因为pdf文件保存了所有格式和字体信息。借助pdfcrop和ebb程序，调用graphicx宏包插入pdf格式图片，能够得到完美的visio矢量图形。

注：
1.导入的代码依然可以使用标准的fig标签，例如：
egin{figure}
