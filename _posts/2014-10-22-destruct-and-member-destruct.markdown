---
layout: article
title: "析构函数和成员析构的先后顺序"
date: 2014-10-22 17:57
comments: true
categories: "C++"
---

  肖总问到这个问题，写了个程序验证：
  	class Member
	{
	 public:
	   Member (){}
	   virtual ~Member (){printf("member destruct\n");}
	};
	class Base
	{
	  public:
	    Base (){}
	    virtual ~Base (){ printf("destruct\n");}
	  private:
	    Member member_;
	};
	int main(int argc, const char *argv[])
	{
	  Base c;
	  return 0;
	}
  
  结果是：

	  destruct
	  member destruct

  可见析构的时候先调用析构函数，最后析构成员对象。