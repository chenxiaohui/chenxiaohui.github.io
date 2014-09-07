---
layout: post
title: "用google来验证一下Maclaurin展开式"
date: 2014-09-07 15:35
comments: true
categories: "基础理论"
---
  偶然发现google可以直接画出函数图像来，精准度极高，于是想起来用这个功能来看一下Maclaurin展开是如何随精度增加而逼近展开式的。从某种角度上讲，这是一个极好的拟合过程，相对于梯度下降的逐步拟合来讲，泰勒公式或者麦克劳林展开直接推导出了每一个拟合因子。
  
  泰勒级数的定义如下：

  {% img center /images/2014/taylor.png "Taylor公式" "Taylor公式" %}

  不过这是带拉格朗日余项的形式。让基准值=0可以得到 Maclaurin 展开式，当然这也就意味着Maclaurin展开式在0附近的拟合是最精确的。定义如下：

  {% img center /images/2014/Maclaurin.png "Maclaurin展开式" "Maclaurin展开式" %}

<!--more-->

  几个重要的Maclaurin展开如下：

  {% img center /images/2014/sinx.png %}
  {% img center /images/2014/cosx.png "几个重要的Maclaurin展开" "几个重要的Maclaurin展开" %}

  这里我们验证一下sinx的逼近随着级数的增加而增加的情况。这也对应于拟合过程拟合维度的增加，相对于一元的拟合，二元或者多元就是会精确一些，但是会带来过拟合的风险。

  首先是sinx的图像

  {% img center /images/2014/sin_x.png %}

  一元函数拟合的时候，y=x

  {% img center /images/2014/x_1.png %}

  二元拟合的时候，y=x-x^3/3!

  {% img center /images/2014/x_2.png %}

  三元拟合的时候，y=x-x^3/3!+x^5/5!

  {% img center /images/2014/x_3.png %}

  
  四元拟合的时候，y=x-x^3/3!+x^5/5!-x^7/7!

  {% img center /images/2014/x_4.png %}
  
  合并起来的图像大致如此：

  {% img center /images/2014/combine.png %}

  再高阶的图像就不画了，上面基本保证了坐标系缩放比例是一致的(sinx的图像由于y轴比例没有跟其他的x轴保持一样的缩放比例），可以看到随着拟合维度的升高，拟合曲线越来越逼近sinx，这也直观体现了Maclaurin展开式的意义。
