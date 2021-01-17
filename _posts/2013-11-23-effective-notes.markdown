---
layout: article
title: "Effective C++ 读书笔记"
date: 2013-11-23 16:41
comments: true
categories: "C++"
---


  Effective前面有几节是说构造析构赋值过程中基类和派生类的调用关系的，做了一个综合一点的例子，来验证一下这个问题。代码如下，话说贴代码是在是很没溜的做法，尤其是如果在出版的书中看到的话，这种行为基本属于骗稿费的...

<!-- more -->

  **object.h**

	#ifndef OCEANBASE_OBJECT_H_
	#define OCEANBASE_OBJECT_H_

	#include "base_object.h"
	class Object: public BaseObject
	{
	  public:
	    Object ();
	    Object (int magic);
	    Object (const Object & obj);
	    virtual ~Object ();
	    virtual void print_info();
	    Object& operator= (const Object& obj);
	    const int & get_magic() const;
	    const int & get_magic();
	  private:
	    /* data */
	    int magic_;
	};

	#endif //OCEANBASE_OBJECT_H_


  **object.cpp**

	#include <stdio.h>
	#include "object.h"

	Object::Object():magic_(0)
	{
	  printf("construct in derived \n");
	}

	Object::Object (int magic):magic_(magic), BaseObject(magic)
	{
	  printf("construct in derived with magic\n");
	}

	Object::Object (const Object & obj)
	  : BaseObject(obj)
	{
	  printf("copy construct in derived\n");
	  magic_ = obj.magic_;
	}

	Object::~Object()
	{
	  printf("destructor in derived\n");
	}

	const int & Object::get_magic() const
	{
	  printf("const\n");
	  return magic_;
	}

	const int & Object::get_magic()
	{
	  printf("non const\n");
	  return magic_;
	}

	Object& Object::operator= (const Object& obj)
	{
	  printf("operator = in derived\n");
	  //BaseObject::operator =(obj);
	  magic_ = obj.magic_;
	}

	void Object::print_info()
	{
	  BaseObject::print_info();
	  printf("derived:magic_%d\n", magic_);
	}

  **base_object.h**
	
	#ifndef OCEANBASE_BASE_OBJECT_H_
	#define OCEANBASE_BASE_OBJECT_H_
	class BaseObject
	{
	  public:
	    BaseObject ();
	    BaseObject (int base_magic);
	    BaseObject (const BaseObject &obj);
	    virtual ~BaseObject ();
	    //BaseObject & operator= (const BaseObject & obj);
	    virtual void print_info();
	  private:
	    /* data */
	    int base_magic_;
	};

	#endif //OCEANBASE_BASE_OBJECT_H_

  **base_object.cpp**

	#include <stdio.h>
	#include "base_object.h"
	BaseObject::BaseObject():base_magic_(0)
	{
	  printf("construct in base\n");
	}

	BaseObject::BaseObject(int base_magic):base_magic_(base_magic)
	{
	  printf("construct in base with magic\n");
	}

	BaseObject::BaseObject (const BaseObject &obj)
	{
	  printf("copy construct in base\n");
	  base_magic_ = obj.base_magic_;
	}

	BaseObject::~BaseObject()
	{
	  printf("destructor in base\n");
	}

	//BaseObject & BaseObject::operator= (const BaseObject & obj)
	//{
	  //printf("operator = in base\n");
	  //base_magic_ =  obj.base_magic_;
	//}

	void BaseObject::print_info()
	{
	  printf("base_object: base_magic_%d\n", base_magic_);
	}


  **main.cpp**

	#include <stdio.h>
	#include "object.h"
	int main(int argc, const char *argv[])
	{
	  printf("\n");
	  printf("obj1\n");
	  Object obj1(1);

	  printf("\n");
	  printf("obj2\n");
	  Object obj2(2);

	  printf("\n");
	  obj2=obj1;

	  printf("\n");
	  printf("obj1.print_info()\n");
	  obj1.print_info();

	  printf("\n");
	  printf("obj2.print_info()\n");
	  obj2.print_info();

	  printf("\n");
	  return 0;
	}


  **Makefile**

	objects= main.o object.o base_object.o
	outfile= out
	flag= -g
	cc= g++

	$(outfile):$(objects)
		$(cc) $(flag) -o $(outfile) $(objects)

	object.o:object.h
	base_object.o:base_object.h
	main.o:object.h base_object.h


	.PHONY:clean
	clean:
		-rm -f $(outfile) $(objects)


执行结果是：

	obj1
	construct in base with magic
	construct in derived with magic

	obj2
	construct in base with magic
	construct in derived with magic

	operator = in derived

	obj1.print_info()
	base_object: base_magic_1
	derived:magic_1

	obj2.print_info()
	base_object: base_magic_2
	derived:magic_1

	destructor in derived
	destructor in base
	destructor in derived
	destructor in base


  可以自行调整并执行，主要说明几个问题而已：

  1. Object c2=c1;这种会被编译器优化成拷贝构造，中间不会有=运算符的调用。
  1. 没有显式声明的时候编译器为类生成默认构造函数，没有显示指明的情况下派生类构造函数自动调用基类的默认构造函数，如果基类有需要初始化的一定要手动声明并调用带参构造函数。 
  2. 没有显式声明的时候编译器为类生成默认拷贝构造函数，没有指明的情况下拷贝构造的时候派生类不会调用基类的拷贝构造，只会调用基类的默认构造函数来内部的基类对象，所以需要自己调用基类的拷贝构造。
  2. 编译器不会为=运算符自动生成重载，=运算符也不调用基类的=运算符重载，所以需要自己声明并调用，这也是书中强调的。
  3. 没有=运算符重载的情况下遇到=操作，拷贝对象每个字段。

  总结一下如下表：

   \{\% pandoc cpp_construct.md \%\}

  注：虽然应该是c++标准，但是还是限制一下编译器版本吧，在gcc4.4.6下验证通过（ob的编译器版本）
