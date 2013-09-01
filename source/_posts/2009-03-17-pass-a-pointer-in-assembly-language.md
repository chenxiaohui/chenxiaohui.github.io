---
title: 汇编传指针
author: Harry Chen
layout: post
permalink: /pass-a-pointer-in-assembly-language/
categories:
  - 随笔
---
# 

#####

写接口实验程序，想写个函数，函数里读入一个数字，存到内存一个变量里，传了变量的偏移值进去，函数里怎么也写不进内存，调了很长时间后才发现mov [bp 4]，ax是不对的，[bp 4]只取出了地址，想在写进去还要再寻一次值，我觉得一般的办法就是寄存器间接寻址了，加一条：

MOV SI,[BP 4]

MOV [SI],AX

这里寄存器只能用BX,BP,SI,DI,对32位汇编可以使用EAX,EBX,ECX,EDX,ESI,EDI,EBP,ESP

当然如果用invoke指令应该会简单很多…..

C语言还是最伟大的语言啊，简化多少操作…..