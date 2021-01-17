---
layout: article
title: "NVI的应用-虚函数模板"
key: nvi-usage-of-virtual-template
date: 2014-07-01 14:52
comments: true
categories: "C++"
---

  我们有时候需要把一个模板函数实现为虚函数，但是C++不支持模板虚函数（至少目前是），所以需要一些方法绕过去。以下是郁白师兄提供的解决方案，确实比较巧妙，之前没想过NVI（NonVirtual Interface）能解决这个问题。

	class IAllocator
	{
	  public:
	    virtual ~IAllocator() {};
	    virtual void *alloc(const int64_t size) = 0;
	};
	template <class T>
	class TAllocator : public IAllocator
	{
	  public:
	    TAllocator(T &allocator) : allocator_(allocator) {};
	    void *alloc(const int64_t size) {return allocator_.alloc(size);};
	  private:
	    T &allocator_;
	};

	class Base
	{
	  public:
	    virtual ~Base() {};
	  public:
	    template <class Allocator>
	    void get_number(Allocator &allocator)
	    {
	      TAllocator<Allocator> ta(allocator);
	      this->get_number_(ta);
	    };
	  private:
	    virtual void get_number_(IAllocator &allocator) = 0;
	};

	class Sub1 : public Base
	{
	  private:
	    void get_number_(IAllocator &allocator)
	    {
	      allocator.alloc(1);
	      fprintf(stdout, "sub1::get_number_ invoked\n");
	    };
	};

	class Sub2 : public Base
	{
	  private:
	    void get_number_(IAllocator &allocator)
	    {
	      allocator.alloc(1);
	      fprintf(stdout, "sub2::get_number_ invoked\n");
	    };
	};

	class PA
	{
	  public:
	    void *alloc(const int64_t sz)
	    {
	      fprintf(stdout, "pa::alloc sz=%ld\n", sz);
	      return NULL;
	    };
	};

	int main()
	{
	  Sub1 s1;
	  Sub2 s2;
	  PA pa;

	  s1.get_number(pa);
	  s2.get_number(pa);
	}

  主要思想是把模板特化，特化之后的函数实现虚函数，把模板遵循的规则转化到继承体系，让一个实例化的模板参数遵循Interface的接口要求。所以TAllocator这个Wrapper至关重要。


[1]: http://www.cnblogs.com/gnuhpc/archive/2012/01/17/2324836.html "【C++程序设计技巧】NVI（Non-Virtual Interface ）"
[2]: http://www.cppblog.com/zhuweisky/archive/2005/09/14/269.html "纯虚函数能为private吗？"


#### 参考文献:

  \[1] 【C++程序设计技巧】NVI（Non-Virtual Interface ）, <http://www.cnblogs.com/gnuhpc/archive/2012/01/17/2324836.html>
 
  \[2] 纯虚函数能为private吗？, <http://www.cppblog.com/zhuweisky/archive/2005/09/14/269.html>
