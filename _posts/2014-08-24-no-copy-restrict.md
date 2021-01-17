---
layout: article
title: "C++的限制拷贝"
key: no-copy-restrict
date: 2014-08-24 12:44
comments: true
categories: "C++"
---

  如果需要禁止一个类的拷贝（多鉴于RAII的资源类），按习惯我们会把拷贝构造函数和赋值运算符重载设置为私有的。比如：

	class Base
	{
	  public:
	    Base (int a)
	    {
	      cout <<"construct"<<endl;
	    }
	    virtual ~Base (){}

	  private:
	    Base(const Base& b)
	    Base & operator=(const Base& b)
	};

	int main(int argc, const char *argv[])
	{
	  Base b(1);//ok
	  Base c=1;//error[1]
	  Base d=c;//error
	  c = d;//error
	  return 0;
	}

  但是问题在于[1]这里没有道理被屏蔽掉，应该会被优化成Base c(1)。如下代码可以证明：
	
	class Base
	{
	  public:
	    Base (int a)
	    {
	      cout <<"construct"<<endl;
	    }
	    virtual ~Base ()
	    {
	    }
	    Base(const Base& b)
	    {
	      cout<<"copy consturct" <<endl;
	    }
	};

	int main(int argc, const char *argv[])
	{
	  Base c=1;
	  return 0;
	}

  运行结果：

	construct

  后来我试了一下才发现，首先这个优化是编译器层面的，所以不同的编译器处理应该是不一样的，虽然我们见到的编译器应该都支持。其次这个优化不是语法检查前做的，也就意味着，在**构造函数没有被声明为explicit的时候**，语法检查会把这个认为是先做了类型转换，然后调用拷贝构造函数，也就是如下：

	Base c = Base(1);

  这就在编译的时候报错了。