---
title: c++的线程传参
layout: article
key: cplusplus_thread_ref
date: 2021-02-14 14:21
---

平时我们经常thread传递参数的时候看到std::ref，之前一直简单理解这个是给智能指针增加了一个引用，后来想不对啊，智能指针拷贝本身就是增加引用。

翻了下StackOverflow发现想错了，一个例子如下：


	```c++
	struct fst {
	  int test(std::string & str) const {
	    str = "bbb";
	    std::cout<< __FILE__ << ":"<< __LINE__<< ":=>" << str << std::endl;
	    return 0;
	  }
	};

	int main(int argc, char *argv[])
	{
	    std::string str = "aaa";
	    fst a;
	    std::thread t(&fst::test,  &a, str);
	    t.join();
	    std::cout << str << std::endl;
	    return 0;
	}
	```

这里并发的问题先不管，实际上是无法通过编译的，std::thread的传参对非const引用要求了类型兼容。所以简单的解决方案是传递str的时候改成std::ref。

但是对智能指针其实没什么影响。

	```
	struct fst {
	  int test(const std::shared_ptr<std::string> & str) const {
	    *str = "bbb";
	    std::cout<< __FILE__ << ":"<< __LINE__<< ":=>" << *str << std::endl;
	    return 0;
	  }
	};

	int main(int argc, char *argv[])
	{
	    std::shared_ptr<std::string> str = std::make_shared<std::string>("aaa");
	    fst a;
	    std::thread t(&fst::test,  &a, str);
	    t.join();
	    std::cout << *str << std::endl;
	    return 0;
	}
	```

因为只能指针的const跟引用对象的const并没有关联。所以实际工作中看到有些std::ref(shared_ptr)其实是没有意义的。
