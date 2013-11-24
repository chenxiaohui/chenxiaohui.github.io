---
layout: post
title: "Thinking In Java读书笔记"
date: 2013-11-24 20:32
comments: true
categories: "其他"
---

  静态成员只有被引用（首次生成所在类的对象或者被首次访问，即使从为生成过那个类的对象）的时候才会初始化。

  一般情况下Java成员变量初始化顺序是，静态成员/静态快->直接初始化的类成员->构造函数

  一个简单的例子如下:

<!-- more -->

  **Cup.java**

	public class Cup {
		public Cup(int i)
		{
			System.out.println("constructor" + i);
		}
	}


  **TestJava.java**
	public class TestJava {
		public Cup cup;
		public Cup cup3 = new Cup(3);
		public static Cup cup1 = new Cup(1);
		public static Cup cup2;
		static{
			cup2 = new Cup(2);
		}
		public TestJava(){
			cup = new Cup(0);
		}
		public static void main(String[] args) {
			new TestJava();
		}
	}

  **执行结果是**

	constructor1
	constructor2
	constructor3
	constructor0
