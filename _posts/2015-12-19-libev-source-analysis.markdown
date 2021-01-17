---
layout: article
title: "libev源码分析"
date: 2015-12-19 16:29
comments: true
published: true
categories: "C++"
---
  
  本文源码以libev4.20为准，其他版本大同小异。

  libev是广泛使用的事件库，是一个功能强大的reactor，可以把Timer、IO、进程线程事件放在一个统一的框架下进行管理。如果有其他的事件触发需求也可以改libev源码把该事件加入libev的框架中（当前前提是得理解libev的设计）。有文章说libev性能比libevent好，没实验过，但是从源码角度看，libev要更简洁，当然更费解一点。作者为了追求代码的整洁和统一使用了大量的宏，造成了阅读的不便。这里我们从宏观分析一下libev的设计实现，然后穿插分析一些小的trick。旨在学习总结libev设计中优雅的地方。

### 基本概念

  首先是一些主要的概念和数据结构。
  
  libev通过定义watcher来关注一个事件，并且把事件类型和对应的毁回调函数关联起来。libev定义了多种事件类型，同时可以在框架中自己添加感兴趣的事件，libev保证了事件触发的顺序性，并在多线程环境下保证事件的串行触发。

  每一种类型的watcher都包含几个基本的成员，通过EV_WATCHER和EV_WATCHER_LIST宏实现。EV_WATCHER_LIST比EV_WATCHER多了一个纸箱下一个watcher的指针。EV_WATCHER_TIMER是定时器的基类，多一个timestamp。这几个宏这里留一个小的trick分析，在后面阐述。

<!--more-->

	/* shared by all watchers */
	#define EV_WATCHER(type)			\
	  int active; /* private */			\
	  int pending; /* private */			\
	  EV_DECL_PRIORITY /* private */		\
	  EV_COMMON /* rw */				\
	  EV_CB_DECLARE (type) /* private */

	#define EV_WATCHER_LIST(type)			\
	  EV_WATCHER (type)				\
	  struct ev_watcher_list *next; /* private */

	#define EV_WATCHER_TIME(type)			\
	  EV_WATCHER (type)				\
	  ev_tstamp at;     /* private */

   举一个例子，IO事件watcher：ev_io

    /* invoked when fd is either EV_READable or EV_WRITEable */
	/* revent EV_READ, EV_WRITE */
	typedef struct ev_io
	{
	  EV_WATCHER_LIST (ev_io)

	  int fd;     /* ro */
	  int events; /* ro */
	} ev_io;
  
  可以看到ev_io相当于继承了基类ev_watcher_list，并派生出自己的成员，fd和events，分别用来存储文件描述符和事件标识。类似的watcher有：

  1. 基类ev_watcher，ev_watcher_list, ev_watcher_time.
  2. io：ev_io
  3. 周期触发定时器：ev_periodic
  4. 定时器：ev_timer
  4. 信号：ev_signal
  5. 子进程：ev_child
  6. 文件stat：ev_stat
  7. 一些内部流程watcher：ev_idle，ev_prepare，ev_check， ev_fork, ev_cleanup
  8. 异步触发：ev_async

### 使用流程

  libev库的基本使用流程是：

  1. 生成一个循环(loop)对象，单线程情况下直接使用default_loop，多线程的情况下使用ev_loop_new来创建。
  1. 调用ev_xx_init先注册一个感兴趣的watcher。把这个watcher跟事件、回调关联起来。
  2. 调用ev_xx_start把事件添加到loop的待处理（后述）列表中。
  4. 调用ev_run执行循环。

  一个简单的使用例程如下（来自官方sample，可见官方风格是大括号换行的....鄙视）：
	
	// a single header file is required
	#include <ev.h>

	#include <stdio.h> // for puts

	// every watcher type has its own typedef'd struct
	// with the name ev_TYPE
	ev_io stdin_watcher;
	ev_timer timeout_watcher;

	// all watcher callbacks have a similar signature
	// this callback is called when data is readable on stdin
	static void
	stdin_cb (EV_P_ ev_io *w, int revents)
	{
	  puts ("stdin ready");
	  // for one-shot events, one must manually stop the watcher
	  // with its corresponding stop function.
	  ev_io_stop (EV_A_ w);

	  // this causes all nested ev_run's to stop iterating
	  ev_break (EV_A_ EVBREAK_ALL);
	}

	// another callback, this time for a time-out
	static void
	timeout_cb (EV_P_ ev_timer *w, int revents)
	{
	  puts ("timeout");
	  // this causes the innermost ev_run to stop iterating
	  ev_break (EV_A_ EVBREAK_ONE);
	}

	int
	main (void)
	{
	  // use the default event loop unless you have special needs
	  struct ev_loop *loop = EV_DEFAULT;

	  // initialise an io watcher, then start it
	  // this one will watch for stdin to become readable
	  ev_io_init (&stdin_watcher, stdin_cb, /*STDIN_FILENO*/ 0, EV_READ);
	  ev_io_start (loop, &stdin_watcher);

	  // initialise a timer watcher, then start it
	  // simple non-repeating 5.5 second timeout
	  ev_timer_init (&timeout_watcher, timeout_cb, 5.5, 0.);
	  ev_timer_start (loop, &timeout_watcher);

	  // now wait for events to arrive
	  ev_run (loop, 0);

	  // break was called, so exit
	  return 0;
	}
  
### 实现分析：

  下面我们针对上述程序分析一下libev的实现。
   
  首先直接采用了default_loop，这里没有使用多线程支持。如果需要开启的话，记得define一下EV_MULTIPLICITY，源码中有大量的对EV_MULTIPLICITY的判断，如果define了则增加一个loop入参来指定运行的线程，否则就直接用默认的。源码实现如下（这里只给出了ev_loop定义）：

	#if EV_MULTIPLICITY

	  struct ev_loop
	  {
	    ev_tstamp ev_rt_now;
	    #define ev_rt_now ((loop)->ev_rt_now)
	    #define VAR(name,decl) decl;
	      #include "ev_vars.h"
	    #undef VAR
	  };
	  #include "ev_wrap.h"

	  static struct ev_loop default_loop_struct;
	  EV_API_DECL struct ev_loop *ev_default_loop_ptr = 0; /* needs to be initialised to make it a definition despite extern */

	#else

	  EV_API_DECL ev_tstamp ev_rt_now = 0; /* needs to be initialised to make it a definition despite extern */
	  #define VAR(name,decl) static decl;
	    #include "ev_vars.h"
	  #undef VAR

	  static int ev_default_loop_ptr;

	#endif
  
  var这里留一个小trick分析，在后面来阐述。

  sample之后调用了两个init来关联事件、watcher和回调函数。对应的定义如下：

	/* these may evaluate ev multiple times, and the other arguments at most once */
	/* either use ev_init + ev_TYPE_set, or the ev_TYPE_init macro, below, to first initialise a watcher */
	#define ev_init(ev,cb_) do {			\
	  ((ev_watcher *)(void *)(ev))->active  =	\
	  ((ev_watcher *)(void *)(ev))->pending = 0;	\
	  ev_set_priority ((ev), 0);			\
	  ev_set_cb ((ev), cb_);			\
	} while (0)

	#define ev_io_set(ev,fd_,events_)            do { (ev)->fd = (fd_); (ev)->events = (events_) | EV__IOFDSET; } while (0)
	#define ev_timer_set(ev,after_,repeat_)      do { ((ev_watcher_time *)(ev))->at = (after_); (ev)->repeat = (repeat_); } while (0)

    #define ev_io_init(ev,cb,fd,events)          do { ev_init ((ev), (cb)); ev_io_set ((ev),(fd),(events)); } while (0)
	#define ev_timer_init(ev,cb,after,repeat)    do { ev_init ((ev), (cb)); ev_timer_set ((ev),(after),(repeat)); } while (0)
  
  可以看到，每种类型的init都是定义了一些赋值操作，由于各种watcher都是从ev_watcher "派生" 而来的，所以可以用ev_watcher向上转换来访问公共成员。这里只是定义了对象，不涉及事件的注册等操作。

  之后sample通过调用xx_start把事件添加到了关注列表中。ev_io_start的源码如下：

	void noinline
	ev_io_start (EV_P_ ev_io *w) EV_THROW
	{
	  int fd = w->fd;

	  if (expect_false (ev_is_active (w)))//当前watcher是否已经active
	    return;

	  assert (("libev: ev_io_start called with negative fd", fd >= 0));
	  assert (("libev: ev_io_start called with illegal event mask", !(w->events & ~(EV__IOFDSET | EV_READ | EV_WRITE))));

	  EV_FREQUENT_CHECK;//周期性的检查

	  ev_start (EV_A_ (W)w, 1);
	  array_needsize (ANFD, anfds, anfdmax, fd + 1, array_init_zero);
	  wlist_add (&anfds[fd].head, (WL)w);//添加到watcher list

	  /* common bug, apparently */
	  assert (("libev: ev_io_start called with corrupted watcher", ((WL)w)->next != (WL)w));

	  fd，change (EV_A_ fd, w->events & EV__IOFDSET | EV_ANFD_REIFY);//加入事件变更
	  w->events &= ~EV__IOFDSET;

	  EV_FREQUENT_CHECK;//周期检查
	}

  代码主要的逻辑在三个地方，ev_start、wlist_add和fd_change。ev_start的比较简单，主要是标记了一下当前watcher已经actived，这是所有的xx_start函数都有的逻辑。

	  inline_speed void
	ev_start (EV_P_ W w, int active)
	{
	  pri_adjust (EV_A_ w);
	  w->active = active;
	  ev_ref (EV_A);
	}

  之后的部分每个不同的watcher实现不同。针对io_watcher，由于fd分配是连续的，所以这个长度可以进行大小限制的，我们用一个连续的数组来存储fd/watcher信息，如[下图所示][2]，用anfd[fd] 就可以找到对应的fd/watcher信息，如果遇到anfd超出我们的buffer长度情形，可以动态扩容。这里直接用了文献2里面的图。

  ![](http://static.data.taobaocdn.com/up/nodeclub/2011/09/seQHQpwHRHOicrTFuDaCs8w.png)

  wlist_add完成向anfd数组对应位置的链表增加事件的工作。更详细的过程可以参考文献2。
  
  最后fd_change完成增加事件变更的任务。libev会根据之前的wlist来判断一个事件是否需要调用对应的处理函数向系统添加监听，比如针对epoll，如果第一次在一个watcher(fd）上调用io_start，那么fdchanges数组中会增加一项，表明下个事件循环周期内需要调用epoll_ctl增加监听。如果之前已经有对应的事件监听存在，则判断是否要替换，不需要再调用epoll_ctl更改epoll的事件注册。源码如下：

	/* something about the given fd changed */
	inline_size void
	fd_change (EV_P_ int fd, int flags)
	{
	  unsigned char reify = anfds [fd].reify;
	  anfds [fd].reify |= flags;

	  if (expect_true (!reify))
	    {
	      ++fdchangecnt;
	      array_needsize (int, fdchanges, fdchangemax, fdchangecnt, EMPTY2);
	      fdchanges [fdchangecnt - 1] = fd;
	    }
	}


  到底位置libev只是完成了一些初始化操作，表明需要对什么事件进行什么处理，但事件流程并没有run起来，最后需要做的是调用ev_run来起线程，并进入事件循环。整个ev_run函数较长，大概有两百多行，这里就不列出代码了，只把程序的主要逻辑列出来。

	  int
	ev_run (EV_P_ int flags)
	{
	  ...
	  do
	    {
	      ...
	      //如果这个进程是新fork出来的，执行ev_fork事件的回调
	      ...
	      //执行ev_prepare回调，也就是每次poll前执行的函数
	      ...
	      //执行监听有改变的事件
	      ...
	      //计算poll应该等待的时间,这个时间和设置以及定时器超时时间有关
	      ...
	      //调用后台I/O复用端口等待事件触发
	      backend_poll (EV_A_ waittime);
	      ...
	      //将定时器事件放入pending数组中
	      ...
	      //将ev_check事件翻入pending数组中
	      ...
	      //执行pending数组中所有的回调
	      EV_INVOKE_PENDING;
	    }
	  while (调用了stop);
	}

  backend_poll封装了不同系统的多路复用机制，在不同的情况下会映射成不同的实现，如epoll、kequque等。对于epoll而言，在每次epoll_wait之前会执行fd_reify(loop)。 fd_reify中会遍历fdchanges数组，把对fd事件的修改通过调用epoll_modify来做真正的修改，这里才真正完成了事件监听向系统的注册。这里有个小的trick再后面分析。

  具体的代码中，程序使用queue_events将要运行的事件放入一个叫做pending的二维数组中，其第一维是优先级，第二维是动态分配的，存放具体事件。之后程序会在适当的地方调用宏EV_INVOKE_PENDING，将pending数组中的事件按优先级从高到低依次执行。

  基本流程图可以看这里，转自[阿里核心系统团队博客][1]：

  ![](http://csrd.aliapp.com/wp-content/plugins/libev_loop2.png)

### 一些技巧

1. 首先是通过define来模拟了继承。libev用宏定义了ev_watcher等基类的成员，实现派生类的时候只需要先用宏把公共成员包含进来，然后定义各个子类自己的成员即可。这种技巧也广泛用在其他一些开源项目中。
 
2. 通过重新define var关键字和重新包含vars头文件的方式，可以把一组变量变换成不同的形式：

	    #define VAR(name,decl) decl;
	      #include "ev_vars.h"
	    #undef VAR

		#define VAR(name,decl) static decl;
		  #include "ev_vars.h"
		#undef VAR
	  
  	这个技巧也被用在s3_error.h里面，用来同时生成一个错误码的定义和其字符串描述。

3. 最后编译libev的时候会发现像epoll.c poll.c等平台相关的backend定义实际上没有加入Makefile。libev实现的时候其实直接在源码里面根据define来包含了c文件。大部分时候我们都是只include头文件，所以这里在使用的时候需要稍加注意。


### 总结

libev虽然代码比较晦涩，但是实现还是很清楚的，设计思想对于实现底层系统很有启发，值得仔细研读。时间有限，只涵盖了一下基本框架，如果有兴趣还是自己改写一下，会更有收获。


[1]: http://csrd.aliapp.com/?p=1604 "libev ev_io源码分析"
[2]: https://cnodejs.org/topic/4f16442ccae1f4aa270010a3 "libev 设计分析"

#### 参考文献:

>\[1] libev ev_io源码分析, <http://csrd.aliapp.com/?p=1604>

>\[2] libev 设计分析, <https://cnodejs.org/topic/4f16442ccae1f4aa270010a3>