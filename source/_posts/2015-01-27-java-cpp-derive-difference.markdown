---
layout: post
title: "Java和C++继承上的一点不同"
date: 2015-01-27 14:51
comments: true
published: true
categories: "Java"
---
   之前没注意过这里：

   java继承的时候只会隐藏父类同名同类型的函数。C++直接隐藏了同名的所有函数，如下：

	public class BaseClass {
		public void Print(String str){
			System.out.println("String" + str);
		}
		public void Print(int num){
			System.out.println(num);
		}
	}
	public class TestDerived extends BaseClass {
		public void Print(String str) {
			System.out.println("String" + str);
		}
		public static void main(String[] args) {
			new TestDerived().Print(121);
		}
	}

  输出结果是121

  而同样的实现C++中直接会找不到父类的函数。

<!--more-->

	#include <stdio.h>
	class Base
	{
	  public:
	    Base (){}
	    void Print(const char* str);
	    void Print(int num);
	};
	void Base::Print(const char* str)
	{
	  printf(str);
	}
	void Base::Print(int num)
	{
	  printf("%d", num);
	}

	class Derived : public Base
	{
	  public:
	    Derived(){}
	    void Print(const char* str);
	};
	void Derived::Print(const char* str)
	{
	  printf("%s", str);
	}

	int main(int argc, const char *argv[])
	{
	  Derived d;
	  d.Print(11);
	  return 0;
	}
