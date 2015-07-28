---
title: 关于.Net下DataGridView绑定自定义数据结构的问题
author: Harry Chen
layout: post

dsq_thread_id:
  - 1257608527
categories:
  - .Net
tags:
  - AutoGenerateColumns
  - Controller
  - DataGridView
  - List
  - model
  - MVC
  - View
  - 绑定
---

  数据绑定是个非常有用的东东，经常在C 下写MVC结构程序的童鞋可能都苦于界面（View）和数据（Model）之间的一致，如果View单一而且需要做的一致性工作不多的话，我们经常会直接在Controller里写更新操作（如图1所示），而如果有多个View，数据同步复杂的话，经常需要手动实现一个观察者模式，每个对数据（Model）的原子操作都需要同时对View进行更新（如图2所示）。

![临时1][1]![临时3][2]

图1 图2

  总的来说.Net平台设计还是非常优秀而人性化的，比如说数据绑定。数据绑定相当于自动实现了从Model到View的数据更新（如图3所示），而免去了自己管理数据一致和自己实现观察者模式的麻烦。同时，DataGridView控件的引入极大的方便了表格形式数据的显示和操作，这个比C 里德ListCtrl使用起来要方便很多。

![临时2][3]

图3

  扯了好多无关的东东，该进入正题了。我们要探讨的是DataGridView控件绑定自定义数据结构的问题。我们要实现的目的是绑定到一个List的结构里，而T可以自己定义。具体的代码不贴了，参考文献1里有一个比较简明的例子。一个比较突出的问题是List没有实现ISort接口，所以绑定后无法自动排序，参考文献2里有相应的解决方法，其中封装的BindingCollection泛型类可以直接作为List泛型的替代品来使用。

  本文主要探讨的问题是其中一个更小的问题。就是使用了BindingCollection之后绑定数据前后数据列会发生变化，如下所示：

  ![test][4] 可见顺序发生了变化，这里没有项的增加，但是如果有没加入的列，DataGridView会自动添加一个列，这个问题很讨厌啊。试了好久之后，从MSDN里查到一个属性AutoGenerateColumns，这个属性在属性编辑器里没有可视化的编辑项，但是可以通过代码设置，所以只需要设置

    dataGridClient.AutoGenerateColumns = false;

  即可避免此问题。
