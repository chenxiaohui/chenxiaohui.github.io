---
layout: post
title: "命名空间和友元冲突"
date: 2014-07-10 19:09
comments: true
categories: "C++"
---

  今天遇到一个问题，需要跨namespace定义友元，这种情况比较常见的是测试类需要访问源码类，gtest据说有个FRIEND_TEST宏，以前用过好像有问题。这里我们直接用友元:

  	namespace oceanbase
  	{
	  	namespace election
	    {
	    	class ObElectionServer : public ObSingleServer
	    	{
	    		friend class ObElectionTester;
	    		...
	    	}
	    }
	}
	namespace oceanbase
	{
	  namespace tests
	  {
	    namespace election
	    {
		    class ObElectionTester : public ObElectionServer
		    {
		    	...
		    }
		}
	}


  这样是肯定不行的，这等于告诉ObElectionServer在自己的namespace下找ObElectionTester。改成如下：

<!--more-->

  	namespace oceanbase
  	{
	  	namespace election
	    {
	    	class ObElectionServer : public ObSingleServer
	    	{
	    		friend class oceanbase::tests::election::ObElectionTester;
	    		...
	    	}
	    }
	}
  
  这样也不行，ObElectionServer不知道ObElectionTester是个包含namespace的类名。所以我们需要前向声明一下类。

	namespace oceanbase
	{
	  namespace tests
	  {
	    namespace election
	    {
	      class ObElectionTester;
	    }
	  }
	  namespace election
	  {
	    class ObElectionServer : public ObSingleServer
	    {
	        friend class oceanbase::tests::election::ObElectionTester;
	        ....
	    }
	  }
	}



