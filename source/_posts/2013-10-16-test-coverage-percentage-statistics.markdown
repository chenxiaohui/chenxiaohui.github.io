---
layout: post
title: "测试覆盖率统计"
date: 2013-10-16 10:15
comments: true
categories: oceanbase
---

代码覆盖率(code coverage)的评价准则

函数覆盖率（Function coverage）：程序中的每个函数或者子函数都被调用过吗？
指令/语句覆盖率（Statement coverage）：程序中的每个节点node或者每个语句都被执行过吗？
判断/分支覆盖率（Decision coverage or branch coverage）：若用控制流图表示程序，有执行到控制流图中的每一个边吗？例如控制结构中所有IF或者switch case指令都有执行到逻辑运算式成立及不成立的情形吗？
条件覆盖率（Condition coverage）：也称为断定覆盖（predicate coverage），每一个逻辑运算式中的每一个条件（无法再分解的逻辑运算式）是否都有执行到成立及不成立的情形吗？条件覆盖率成立不表示判断覆盖率一定成立。
条件/判断覆盖率（Condition/decision coverage）：需同时满足判断覆盖率和条件覆盖率。
考虑以下的C/C++函数：

int foo (int x, int y)

{

int z = 0;

if ((x>0) && (y>0)) {

z = x;
lsv
}

return z;

}

假设此函数是一个大型程序的一部份，且某测试用例执行到此函数：

函数覆盖率：只要函数foo有执行过一次，即满足函数覆盖率100%的条件。
指令覆盖率：若有调用过foo(1,1)，函数中每一行（包括z = x;）都执行一次，满足指令覆盖率100%的条件。
判断覆盖率：若有调用过foo(1,1)及foo(0,1)，前者会使if的条件成立，因此z = x;会执行，后者会使if的逻辑运算式（(x>0) && (y>0);）不成立，因此满足判断覆盖率100%的条件。
条件覆盖率：若有调用过foo(1,1)、foo(1,0)及foo(0,0)，前二个会使(x>0)的条件成立，而第三个会使该条件不成立，而第一个会使(y>0)的条件成立，而后面二个会使该条件不成立，所有条件都有出现成立及不成立的情形，因此满足条件覆盖率100%的条件。
考虑以下的程序：

if a and b then

以下二个测试可以得到100%的条件覆盖率：

a=true, b=false
a=false, b=true
但上述的测试条件都不会使if的逻辑运算式成立，因此不符合判断覆盖的条件。至少还需要添加如下的测试条件，才能保证if的判断条件都满足了。

a=true, b=true
 

 http://www.cnblogs.com/turtle-fly/archive/2013/01/09/2851474.html

 http://sdet.org/?p=212

 http://www.cnblogs.com/turtle-fly/archive/2013/01/09/2851474.html

 http://magustest.com/blog/whiteboxtesting/using-gcov-lcov/