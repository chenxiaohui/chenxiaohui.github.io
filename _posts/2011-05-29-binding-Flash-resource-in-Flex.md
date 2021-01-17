---
title: 关于Flex绑定Flash资源
author: Harry Chen
layout: article

categories:
  - Flex
  - 与技术相关
tags:
  - flash
  - Flex
  - 资源
---

  很多时候我们需要在Flex里使用Flash的资源，大家的习惯可能是用Flash的一个扩展导出一个原件为SWC，然后在Flex里引用，但是问题是一者SWC太多，二者Flash按钮不能导出（至少CS4还不行）。我们这里提供一种简单的基于绑定的导出方式。

  首先在Flash里选择为ActionScript导出（右键，属性里），然后编译SWF文件，之后我们直接用代码引用SWF文件里的原件，并引用为Image控件的source。代码如下


    package assets
    {
    	import mx.controls.Image;

    	public class DiceOne extends Image
    	{
    		[Embed(source="../res/dice.swf",symbol="DiceOne")]
    		[Bindable]
    		public var img:Class;

    		public function DiceOne()
    		{
    			super();
    			source=img;
    		}
    	}
    }

  这样就可以把这个原件像一个Sprite或者MovieClip一样引用了。
