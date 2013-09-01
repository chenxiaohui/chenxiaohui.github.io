---
title: 关于Flex和.NET自定义事件的比较
author: Harry Chen
layout: post
permalink: /difference-between-Flex-and-dotNet-event/
categories:
  - .Net
tags:
  - .NET
  - 'C#'
  - Flex
  - 消息
  - 自定义
---
# 

实际上大多数语言，或者说大多数框架的消息机制是类似的。Flex和.NET(c#为例)的消息机制可以做为一个例子说明。如下我们给出一个简单的Flex自定义消息和.NET自定义消息的例子，不同的是，.NET下消息是通过代理(delegate)给出的，而Flex这个超像java的东东还是一如既往的用观察模式去AddEventListener，不过这种差别应该都是语言层的差别，就实现机制应该没什么不一样的，毕竟消息这种东西嘛，到头来都是观察模式，授人以柄，供其调用。

两者的不同点其实也挺值得玩味的，Flex是弱类型语言，类型弱得连函数都若有如无，所以不需要定义事件处理句柄的类型（我的理解），而C#各个event自己管理，所以也不需要用一个类似于Flex消息类型的东西去界定这是哪个消息。

世界如此有爱。

Flex自定义消息例子


    EventType.as：定义了消息类型，类似于一个枚举
    package event
    {
    	public final class EventType
    	{
    		public static const TableClickEvent:String="TableClick";
    	}
    }
    TableEvent.as：定义了消息本身，继承自Event,自定义了一个参数传递一个value
    package event
    {
    	import flash.events.Event;

    	public class TableEvent extends Event
    	{
    		public var value:int=0;
    		public function TableEvent(type:String, value:int,bubbles:Boolean=false, cancelable:Boolean=false)
    		{
    			super(type, bubbles, cancelable);
    			this.value=value;
    		}

    	}
    }
    Table.as：分发消息的类，也就是消息源
    package msg
    {
    	import event.*;

    	import flash.events.EventDispatcher;
    	public class Table extends EventDispatcher
    	{
    		public function Table()
    		{
    		}
    		public function TableClick():void
    		{
    			dispatchEvent(new TableEvent(EventType.TableClickEvent,1));
    		}
    	}
    }
    监听消息的代码：
    public var table:Table;
    table=new Table();
    table.addEventListener(EventType.TableClickEvent,TableClick);
    table.TableClick();

应该比较通俗易懂，不做解释

下面给出.NET下自定义消息的一个例子：


    MyEvent.cs自定义消息分发类，自定义了一个delegate指定消息句柄类型:
    using System;
    using System.Collections.Generic;
    using System.Text;

    namespace testMessage
    {
        class MyEvent
        {
            public delegate void MyEventHandler(MyEventArgs e);
            public event MyEventHandler handler;
            public void Click()
            {
                if (handler != null)
                    handler(new MyEventArgs("helloworld"));
            }
          }
    }
    MyEventArgs.cs消息类型定义
    using System;
    using System.Collections.Generic;
    using System.Text;

    namespace testMessage
    {
        class MyEventArgs:EventArgs
        {
            public String strMessage;
            public MyEventArgs(string message)
            {
                strMessage = message;
            }
        }
    }
    消息监听类：
    using System;
    using System.Collections.Generic;
    using System.Text;

    namespace testMessage
    {
        class Program
        {
            static void Main(string[] args)
            {
                MyEvent eve = new MyEvent();
                eve.handler =new MyEvent.MyEventHandler(eve_handler);
                eve.Click();
            }

            static void eve_handler(MyEventArgs e)
            {
                Console.WriteLine(e.strMessage);
            }
        }
    }