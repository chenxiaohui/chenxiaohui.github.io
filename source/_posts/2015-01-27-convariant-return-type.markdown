---
layout: post
title: "协变返回类型"
date: 2015-01-27 15:48
comments: true
published: true
categories: "C++"
---
  
  协变返回类型（Convariant Return Type）是指override的函数，返回值有继承关系（子类函数返回类型是父类返回类型的子类）。例子如下：

<!--more-->

	class Base
	{
	  public:
	    Base (){}
	    virtual void print(){
	      printf("Base");
	    }
	};

	class Derived : public Base
	{
	  public:
	    Derived(){}
	    virtual ~Derived (){}
	    void print(){
	      printf("Derived");
	    }
	};

	class TestBase
	{
	  public:
	    TestBase (){}
	    virtual Base* getObject(){
	      return new Base();
	    }
	};

	class TestDerived : public TestBase
	{
	  public:
	    TestDerived (){}
	    virtual ~TestDerived (){}
	    Derived* getObject(){
	      printf("invoke here\n");
	      return new Derived;
	    }
	};

	int main(int argc, const char *argv[])
	{
	  TestBase * base = new TestDerived();
	  Base* b = base->getObject();
	  b->print();
	  return 0;
	}

   	结果：
   	invoke here
   	Derived

  java同理，只不过验证起来比较容易。直接打印对象就行。

	public class BaseClass {
	}
	public class DerivedClass extends BaseClass{
	}

	public class TestBase {
		public BaseClass getObject(){
			return new BaseClass();
		}
	}

	public class TestDerived extends TestBase{
		public DerivedClass getObject(){
			return new DerivedClass();
		}
		public static void main(String[] args) {
			TestBase base = new TestDerived();
			System.out.println(base.getObject());
		}
	}

	返回值：
	test.server.others.DerivedClass@5d1eb50b

  这里想验证的其实是返回引用是可以的。返回对象是不行的。java只有返回引用，所以都可以。可自行验证。
  