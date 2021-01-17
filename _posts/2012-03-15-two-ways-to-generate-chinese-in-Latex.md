---
title: 两种可行的Latex中文生成方式(GBK/UTF8)
author: Harry Chen
layout: article

dsq_thread_id:
  - 1342087725
categories:
  - Latex
tags:
  - beamer
  - ctex
  - gbk
  - Latex
  - utf8
  - 中文
---
# 

  本来想总结一下Latex里各种中文排版支持，但是发现太乱了，CCT，CJK，CTEX神马的，还有GBK和UTF8下的不同编码方式，再加上XeLatex这样来搅局的……所以最后决定只给出一种可行的排版方式，测试环境是Windows CTex2.8。

  ps:每天忍辱负重的在Windows下用Vim和Latex……

  第一种是gbk编码下的编译方式

    REM taskkill /im AcroRd32.exe
    pdflatex %1
    bibtex %1
    pdflatex %1
    gbk2uni %1.out
    pdflatex %1
    start %1.pdf

  其中第一句的目的是结束掉当前的PDF文档，但是它会随机选择一个Acrobat Reader进程结束，所以给注掉了。从代码里可以看出，需要执行多遍pdflatex，同时穿插bibtex生成参考文件，gbk2uni的作用是将gbk转成unicode，这个命令是cct里的，请确保你的环境变量中有cct的bin目录。

  测试article代码如下：

    \documentclass{article}
    \usepackage{CJK}
    \usepackage{cite}
    ewcommand{\upcite}[1]{ extsuperscript{ extsuperscript{
