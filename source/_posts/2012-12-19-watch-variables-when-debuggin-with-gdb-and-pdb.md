---
title: GDB/PDB调试时变量的监视
layout: post
dsq_thread_id:
  - 1264071274
categories:
  - Python
tags:
  - pdb
  - 监视
  - 调试
format: standard
---

  gdb下有几个监视变量的命令，比如watch可以监视一个变量是否更改，rwatch监视读，awatch监视写等等。这里说的主要是另一个命令，display。

  display命令做的事情是指定一个变量，然后在每次调试停住的时候显示这个变量的值。这个是很有用的操作，等于在命令行调试的时候提供了类似于IDE里监视变量（Add to Watch）的功能。但是一直没有发现python的调试工具pdb里有类似的功能。后来在Python官方文档里看到一个命令:commands，提供了类似的功能。

  commands命令的使用是 commands [bpnumber] 。bpnumber指定了断点的id（集），省略的话表示上一个断点（集）。之后可以输入需要做的事情，然后以end结尾，一个简单的例子如下：


    (Pdb) commands 1
    (com) print some_variable
    (com) end
    (Pdb)


  commands有一个明显的问题，就是如果停在其他断点的地方，就会终止这个commands，以后即使执行到了这个断点，也不会再执行该commands，官方的解释是：

> Specifying any command resuming execution (currently continue, step, next, return, jump, quit and their abbreviations) terminates the command list (as if that command was immediately followed by end). This is because any time you resume execution (even with a simple next or step), you may encounter another breakpoint–which could have its own command list, leading to ambiguities about which list to execute.

  但是这个明明是说只要恢复执行，commands就失效啊…但是实际上比如你只打了一个断点，然后在这个断点定义了commands，之后每次都是用continue，这是不会导致该断点失效的，毕竟没有encounter another breakpoint–which could have its own command list嘛。
