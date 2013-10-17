---
title: '简短总结一下C#里跨线程更新UI'
author: Harry Chen
layout: post

mkd_text:
  - |
    跨线程更新UI是写多线程程序尤其是通信类的程序经常遇到的问题，这里面主要的问题是冲突，比如数据线程想要更新UI的时候，用户同时也在更新UI，就会出现争用。C#里可以用
    
    	:::c#
    	Control.CheckForIllegalCrossThreadCalls = false;
    
    <!--more-->
    
    来关闭跨线程检测。但是这样做有一定的风险，容易让程序崩溃。
    
    最好的办法是通过Invoke，这篇博客只是提供一个示例，至于那些线程同步、Invoke和BeginInvoke，Invoke底层实现神马的，有空再说吧。
    
    一个简单的例子如下：（注，Form1 加入了一个名为txt的TextBox）
    
    	:::c#
    	using System;
    	using System.Collections.Generic;
    	using System.ComponentModel;
    	using System.Data;
    	using System.Drawing;
    	using System.Linq;
    	using System.Text;
    	using System.Windows.Forms;
    	using System.Threading;
    
    	namespace testThread
    	{
    		public partial class Form1 : Form
    		{
    			private delegate void InvokeCallback(string msg); //定义回调函数（代理）格式
    			public Form1()
    			{
    				InitializeComponent();
    				Control.CheckForIllegalCrossThreadCalls = false;//关闭跨线程调用检测
    				MyMessage m = new MyMessage();//一个消息源
    				//启动一个线程，把界面对象传递过去
    				Thread t = new Thread(new ParameterizedThreadStart(m.Test));
    				t.Start((object)this);
    			}
    			//Invoke回调函数
    			public void UpdateText(string text)
    			{
    				if (txt.InvokeRequired)//当前线程不是创建线程
    					txt.Invoke(new InvokeCallback(UpdateText),new object[]{text});//回调
    				else//当前线程是创建线程（界面线程）
    					txt.Text = text;//直接更新
    			}
    		}
    		//消息源
    		class MyMessage
    		{
    			public void Test(object para)
    			{
    				Form1 form = (Form1)para;
    				form.UpdateText("测试");
    			}
    		}
    	}
    
    上面的例子很简单，主要是需要判断一下当前线程是不是控件的创建线程，如果是就直接更新，否则建立一个Invoke对象，设置好代理和参数，然后调用Invoke。需要注意的是建立线程的时候如果需要传参数，应该通过ParameterizedThreadStart建立并且以object格式传递参数。
dsq_thread_id:
  - 1258318261
categories:
  - .Net
tags:
  - CheckForIllegalCrossThreadCalls
  - Invoke
  - UI
  - 更新
  - 跨线程
format: standard
---
# 

跨线程更新UI是写多线程程序尤其是通信类的程序经常遇到的问题，这里面主要的问题是冲突，比如数据线程想要更新UI的时候，用户同时也在更新UI，就会出现争用。C#里可以用


    Control.CheckForIllegalCrossThreadCalls = false;


来关闭跨线程检测。但是这样做有一定的风险，容易让程序崩溃。

最好的办法是通过Invoke，这篇博客只是提供一个示例，至于那些线程同步、Invoke和BeginInvoke，Invoke底层实现神马的，有空再说吧。

一个简单的例子如下：（注，Form1 加入了一个名为txt的TextBox）


    using System;
    using System.Collections.Generic;
    using System.ComponentModel;
    using System.Data;
    using System.Drawing;
    using System.Linq;
    using System.Text;
    using System.Windows.Forms;
    using System.Threading;

    namespace testThread
    {
        public partial class Form1 : Form
        {
            private delegate void InvokeCallback(string msg); //定义回调函数（代理）格式
            public Form1()
            {
                InitializeComponent();
                Control.CheckForIllegalCrossThreadCalls = false;//关闭跨线程调用检测
                MyMessage m = new MyMessage();//一个消息源
                //启动一个线程，把界面对象传递过去
                Thread t = new Thread(new ParameterizedThreadStart(m.Test));
                t.Start((object)this);
            }
            //Invoke回调函数
            public void UpdateText(string text)
            {
                if (txt.InvokeRequired)//当前线程不是创建线程
                    txt.Invoke(new InvokeCallback(UpdateText),new object[]{text});//回调
                else//当前线程是创建线程（界面线程）
                    txt.Text = text;//直接更新
            }
        }
        //消息源
        class MyMessage
        {
            public void Test(object para)
            {
                Form1 form = (Form1)para;
                form.UpdateText("测试");
            }
        }
    }


上面的例子很简单，主要是需要判断一下当前线程是不是控件的创建线程，如果是就直接更新，否则建立一个Invoke对象，设置好代理和参数，然后调用Invoke。需要注意的是建立线程的时候如果需要传参数，应该通过ParameterizedThreadStart建立并且以object格式传递参数。
