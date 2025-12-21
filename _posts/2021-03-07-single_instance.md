---
title: 单例模式讨论
layout: article
key: single_instance
date: 2021-03-07 16:09
published: true
comments: true
categories: "技术"
---

其实就是记录下。。不算自己写的。

mutex版本：

```cpp

std::shared_ptr<some_resource> resource_ptr;
std::mutex resource_mutex;
void foo() {
	std::unique_lock<std::mutex> lk(resource_mutex); // 所有线程在此序列化 
	if(!resource_ptr)
		{resource_ptr.reset(new some_resource); // 只有初始化过程需要保护
  	lk.unlock();
  resource_ptr->do_something();
}
```
double-checking版本：

```cpp

void undefined_behaviour_with_double_checked_locking()
{
  if(!resource_ptr)  // 1
  {
    std::lock_guard<std::mutex> lk(resource_mutex);
    if(!resource_ptr)  // 2
    {
      resource_ptr.reset(new some_resource);  // 3
    }
  }
  resource_ptr->do_something();  // 4
}
```

call_once版本
```cpp
std::shared_ptr<some_resource> resource_ptr;
std::once_flag resource_flag;  // 1
void init_resource()
{
  resource_ptr.reset(new some_resource);
}
void foo() {
std::call_once(resource_flag,init_resource); // 可以完整的进行一次初始化
  resource_ptr->do_something();
}

```
static instance版本。
```cpp
class my_class;
my_class& get_my_class_instance()
{
  static my_class instance; // 线程安全的初始化过程
  return instance;
}

```