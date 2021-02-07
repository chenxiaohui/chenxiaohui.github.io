---
layout: article
title: "c++11的不定参数"
date: 2021-01-01 22:03
comments: true
published: true
categories: "C++"
---

  不定参数之前其实用的比较少，一个项目里面能用到的大概只有log函数什么的。C++11支持了新的不定参数定义，之前也看过，但是毕竟使用的场景少，也没怎么研究。最近看了一下，感觉还是挺有意思的，至少比C++11之前方便了非常多，可以灵活的应用到很多场景里面，特别是模板。

  之前C++ 或者C语言里面经常会看到这种写法：

    ```C++
	#define log(...) \
	    printf(__VA_ARGS__);

	// tuple example
	template<typename ... T>
	void f(T ... args) 
	{
	    cout << sizeof...(args) << endl; //打印变参的个数
	    log(args...);
	}
	// template <typename T>
	// void fun(const T& t){
	    // cout << t << '\n';
	// }

	// template <typename T, typename ... Args>
	// void fun(const T& t, Args ... args){
	    // cout << t << ',';
	    // fun(args...);//递归解决，利用模板推导机制，每次取出第一个，缩短参数包的大小。
	// }

	template<typename ...T>
	void func( T... args) {
	    // f(&args...); // expands to f(&E1, &E2, &E3)
	    // f(++args...); // expands to f(n, ++E1, ++E2, ++E3);
	    // f(const_cast<const Args*>(&args)...);
	    f(args...);
	}
	// f(h(E1,E2,E3) + E1, h(E1,E2,E3) + E2, h(E1,E2,E3) + E3)
	int main(int argc, const char *argv[]) {
	    func("%d = %d", 1, 2);
	    return 0;
	}
    ```
TODO
