---
layout: post
title: "跨线程解锁安全的spinlock"
date: 2016-06-13 17:36
comments: true
published: true
categories: "基础理论"
---


  在C语言下面我们可能会写出如下的代码：

	static pthread_spinlock_t lock;

	__attribute__((constructor))
	void lock_constructor () {
	    if ( pthread_spin_init ( &lock, 0 ) != 0 ) {
	        exit ( 1 );
	    }
	}

	int func(xx) {
	  int ret = 0;
	  if (xx) {
	    ret = ERR1;
	    goto exit;
	  }
	  pthread_spin_lock(&lock);
	  if (xx) {
	    ret = ERR2;
	    goto exit;
	  }
	exit:
	  pthread_spin_unlock(&lock);
	  return 0;
	}

	__attribute__((destructor))
	void lock_destructor () {
	    if ( pthread_spin_destroy ( &lock ) != 0 ) {
	        exit ( 3 );
	    }
	}

  这段代码存在下面几个问题：

  	1. spinlock没有静态初始化函数，需要确保使用前调用了pthread_spin_init.
  	2. 跳转到exit标记去unlock的时候，并不能保证lock已经被加过锁了。
  	3. func本身存在潜在的并发问题，一个线程可能跳转到exit去解别的线程加的锁。

  根据[文档][1]这几种情况下的行为是未定义的。


	  The pthread_spin_lock() function shall lock the spin lock referenced by lock. The calling thread shall acquire the lock if it is not held by another thread. Otherwise, the thread shall spin (that is, shall not return from the pthread_spin_lock() call) until the lock becomes available. The results are undefined if the calling thread holds the lock at the time the call is made. The pthread_spin_trylock() function shall lock the spin lock referenced by lock if it is not held by any thread. Otherwise, the function shall fail.

	  The results are undefined if any of these functions is called with an uninitialized spin lock.

  为了情况1，我们可以考虑通过原子操作实现spin_lock，用一个volatile int64类型的整数来标识当前锁的状态。nginx里面的实现如下：

	    /* 
	     * Copyright (C) Igor Sysoev 
	     * Copyright (C) Nginx, Inc. 
	     */  
	      
	      
	    #include <ngx_config.h>  
	    #include <ngx_core.h>  
	      
	    //Function: to achieve spin atomic operation lock method based on ngx_spinlock  
	    //Parameter interpretation:   
	    //lock: Lock the atomic variable expression  
	    //value: Flag, whether the lock is a process  
	    //spin: In a multi processor system, when the ngx_spinlock method did not get the lock, the current process in a scheduling kernel in the waiting for the other processors to release the lock time  
	    void  
	    ngx_spinlock(ngx_atomic_t *lock, ngx_atomic_int_t value, ngx_uint_t spin)  
	    {  
	      
	    #if (NGX_HAVE_ATOMIC_OPS)//Support atomic operations  
	      
	        ngx_uint_t  i, n;  
	      
	        //Has been in circulation, until the lock is acquired  
	        for ( ;; ) {  
	      
	            //Lock 0 said no other process holding the lock, then the lock value indicates the current process holding the lock is set to value parameters  
	            if (*lock == 0 && ngx_atomic_cmp_set(lock, 0, value)) {  
	                return;  
	            }  
	      
	            //If it is a multi processor system  
	            if (ngx_ncpu > 1) {  
	                for (n = 1; n <spin; n <<= 1) {  
	                    //With the increasing number of the actual to wait, inspection interval and lock more  
	                    for (i = 0; i <n; i++) {  
	                        ngx_cpu_pause();//Tell CPU now in the spin lock wait state  
	                    }  
	      
	                    //Check the lock is released  
	                    if (*lock == 0 && ngx_atomic_cmp_set(lock, 0, value)) {  
	                        return;  
	                    }  
	                }  
	            }  
	      
	            //The current process for the processor, but still in the executable state  
	            ngx_sched_yield();  
	        }  
	      
	    #else  
	      
	    #if (NGX_THREADS)  
	      
	    #error ngx_spinlock() or ngx_atomic_cmp_set() are not defined !  
	      
	    #endif  
	      
	    #endif  
	      
	    }    	

  简单解释几个关键点：

  nginx的实现解决了静态初始化的问题，但是解决不了上述问题2和3。为此我们可以考虑在表征spinlock状态的整形变量中加入线程id，来区分操作者是否是锁持有者。参考实现如下：

	typedef volatile int64_t Atomic;

	#define _spin_unlock_safe   _unlock_safe

	typedef struct {
	 union {
	  struct {
	    int32_t tid;
	    int32_t atomic32;
	  };
	  volatile int64_t atomic;
	 };
	} CACHE_ALIGNED SpinLock;

	static __inline__ int64_t _get_tid() {
	  static __thread int64_t tid = -1;
	  if _unlikely(tid == -1) {
	    tid = (int64_t)(syscall(__NR_gettid));
	  }
	  return tid;
	}

	static __inline__ int _try_lock_safe(SpinLock *lock) {
	  SpinLock lock_val = {{{.tid = (int32_t)_get_tid(), .atomic32 = 1}}};
	  return lock->atomic == 0 && _atomic_cmp_set(&lock->atomic, 0, lock_val.atomic);
	}

	static __inline__ int _unlock_safe(SpinLock *lock) {
	  SpinLock lock_val = {{{.tid = (int32_t)_get_tid(), .atomic32 = 1}}};
	  return _atomic_cmp_set(&lock->atomic, lock_val.atomic, 0);
	}

	static __inline__ void _spin_lock_safe(SpinLock *lock) {
	  int i, n;
	  SpinLock lock_val = {{{.tid = (int32_t)_get_tid(), .atomic32 = 1}}};
	  for (; ;) {
	    if (lock->atomic == 0 && _atomic_cmp_set(&lock->atomic, 0, lock_val.atomic)) {
	      return;
	    }

	    for (n = 1; n < 1024; n <<= 1) {

	      for (i = 0; i < n; i++) {
	        __asm__(".byte 0xf3, 0x90");
	      }

	      if (lock->atomic == 0 && _atomic_cmp_set(&lock->atomic, 0, lock_val.atomic)) {
	        return;
	      }
	    }

	    sched_yield();
	  }
	}

	static __inline__ void _spin_lock(Atomic *lock) {
	  int i, n;
	  for (; ;) {
	    if (*lock == 0 && _atomic_cmp_set(lock, 0, 1)) {
	      return;
	    }

	    for (n = 1; n < 1024; n <<= 1) {

	      for (i = 0; i < n; i++) {
	        __asm__(".byte 0xf3, 0x90");
	      }

	      if (*lock == 0 && _atomic_cmp_set(lock, 0, 1)) {
	        return;
	      }
	    }

	    sched_yield();
	  }
	}
  
  简单解释几个问题：

  1.  __asm__(".byte 0xf3, 0x90");是intel的一条指令，实际上就是上面的ngx_cpu_pause
  2. sched_yield实现等同于ngx_sched_yield
  2. 

[1]: http://pubs.opengroup.org/onlinepubs/009695399/functions/pthread_spin_lock.html "The Open Group Base Specifications Issue 6
IEEE Std 1003.1, 2004 Edition"