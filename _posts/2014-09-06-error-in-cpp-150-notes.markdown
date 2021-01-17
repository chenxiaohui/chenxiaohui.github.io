---
layout: article
title: "《改善C++程序的150个建议》勘误"
date: 2014-09-06 11:41
comments: true
categories: "C++"
---
  翻了一下编写高质量代码：改善C++程序的150个建议，感觉一般，主要是能下到pdf。看到两个错误。

  第一个错误是内存池的那里，内部类使用了外部类的成员变量，这是C++啊，不是java，内部类默认不持有外部类指针。

	class MemPool
	{
	  public:
	    MemPool (int nItemSize, int nMemBlockSize = 2048):
	      m_nItemSize(nItemSize),
	      m_nMemBlockSize(nMemBlockSize),
	      m_pMemBlockHeader(NULL),
	      m_pFreeNodeHeader(NULL)
	    {}
	    virtual ~MemPool (){}
	    void * Alloc();
	    void Free();
	  private:
	    /* data */
	    const int m_nMemBlockSize;
	    const int m_nItemSize;
	    struct _FreeNode
	    {
	      _FreeNode* pPrev;
	      char data[m_nItemSize - sizeof(_FreeNode*)];
	    };
	    struct _MemBlock
	    {
	      _MemBlock * pPrev;
	      _FreeNode data[m_nMemBlockSize/m_nItemSize];
	    };
	    _MemBlock* m_pMemBlockHeader;
	    _FreeNode* m_pFreeNodeHeader;
	};
  
  第二个错误是作者强调nocopyable基类是需要私有继承的，其实不需要，public继承足够了，public继承又不会把基类的private成员继承下来。

	class nocopyable
	{
	  public:
	    nocopyable (){}
	    virtual ~nocopyable (){}

	  private:
	    /* data */
	    nocopyable (const nocopyable&);
	    nocopyable& operator=(const nocopyable&);
	};
	class Base : public nocopyable

  太tm不严谨了。