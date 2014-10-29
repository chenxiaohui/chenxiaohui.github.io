---
layout: post
title: "虚函数模板和模板类中的虚函数"
date: 2014-10-29 21:05
comments: true
categories: "C++"
---
  自从知道了C++不支持虚函数模板之后就觉得相关的一概不支持，今天写程序的时候想把基类做成模板，然后继承基类。以为也不支持，写了一下才发现支持的，无论是非模板类继承一个特化之后的模板还是模板类继承包含虚函数的模板基类都是没问题的。从实现上看，反正使用的时候都会特化的，特化之后虚函数表指针是固定的。不存在像函数模板这种类生成的时候无法确定虚函数表的情况。

  例子如下：

<!--more-->

  	enum SessionType
	{
	  ROSession,
	  RWSession,
	  RPSession
	};
	class BaseTransCtx
	{
	  public:
	    BaseTransCtx (){}
	    virtual ~BaseTransCtx (){}
	};
	template<typename Type>
	class ISessionCtxFactory
	{
	  public:
	    ISessionCtxFactory(){};
	    ~ISessionCtxFactory() {};
	  public:
	    virtual BaseTransCtx *alloc(const Type type) = 0;
	    virtual void free(BaseTransCtx *ptr) = 0;
	};
	typedef ISessionCtxFactory<SessionType> SessionMgr;
	class TransSessionMgr: public SessionMgr
	{
	  public:
	    TransSessionMgr (){}
	    virtual ~TransSessionMgr (){}

	    BaseTransCtx *alloc(const SessionType type)
	    {
	      return NULL;
	    }

	    void free(BaseTransCtx *ptr)
	    {
	      if (ptr != NULL)
	      {
	        delete ptr;
	      }
	    }
	};
  	int main(int argc, const char *argv[])
	{
	  TransSessionMgr trans;
	  BaseTransCtx* ctx = trans.alloc(RWSession);
	  trans.free(ctx);
	  return 0;
	}
  
  模板类继承虚基类也可以。

	template<typename Type>
	class ISessionCtxFactory
	{
	  public:
	    ISessionCtxFactory(){};
	    ~ISessionCtxFactory() {};
	  public:
	    virtual BaseTransCtx *alloc(const Type type) = 0;
	    virtual void free(BaseTransCtx *ptr) = 0;
	};
	template<typename Type>
	class TransSessionMgr: public ISessionCtxFactory<Type>
	{
	  public:
	    TransSessionMgr (){}
	    virtual ~TransSessionMgr (){}

	    BaseTransCtx *alloc(const Type type)
	    {
	      return NULL;
	    }

	    void free(BaseTransCtx *ptr)
	    {
	      if (ptr != NULL)
	      {
	        delete ptr;
	      }
	    }
	};

  但是这样就不行了

	class ISessionCtxFactory
	{
	  public:
	    ISessionCtxFactory(){};
	    ~ISessionCtxFactory() {};
	  public:
	    template<typename Type>
	      virtual BaseTransCtx *alloc(const Type type) = 0;
	    virtual void free(BaseTransCtx *ptr) = 0;
	};
	class TransSessionMgr: public ISessionCtxFactory
	{
	  public:
	    TransSessionMgr (){}
	    virtual ~TransSessionMgr (){}

	    template<typename Type>
	      BaseTransCtx *alloc(const Type type)
	      {
	        return NULL;
	      }

	    void free(BaseTransCtx *ptr)
	    {
	      if (ptr != NULL)
	      {
	        delete ptr;
	      }
	    }
	};
