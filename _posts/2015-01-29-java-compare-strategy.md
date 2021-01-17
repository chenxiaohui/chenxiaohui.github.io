---
layout: article
title: "Java 中相等的比较"
key: java-compare-strategy
date: 2015-01-29 20:42
comments: true
published: true
categories: "Java"
---

  遇到如下一个问题，java中使用复杂类型做Hashkey的时候，构造另一个值相同的对象作为key无法获取map的value。原因其实是java的==判断的依据是两个引用是否指向了同一个对象。实际调用了hashCode函数。内置对象的逻辑相等比较需要使用equals，比如String。而对于非内置对象，equals也同样调用了hashCode来判断相等。

  所以对于需要逻辑相等判断的对象，需要override两个函数，比如如下一个getkey的类定义了如何从Map中根据path和type得到一个唯一的对象：

  	class ZkEventKey {
		EventType type = null;
		String path = null;
		
		ZkEventKey(EventType type, String path) {
			super();
			this.type = type;
			this.path = path;
		}
		
		EventType getType() {
			return type;
		}
		
		String getPath() {
			return path;
		}

		@Override
		public String toString() {
			return "ZkEventKey [type=" + type + ", path=" + path + "]";
		}
		@Override
		public boolean equals(Object obj) {
			if (this == obj){
				return true;
			}else if (obj == null){
				return false;
			}
			if (getClass() != obj.getClass()){
				return false;
			}
			ZkEventKey other = (ZkEventKey)obj;
			if(type == other.type && path.equals(other.path)){
				return true;
			}
			return false;
		}
		@Override
		public int hashCode() {
		    final int prime = 31;
	        int result = 1;
	        result = prime * result + type.hashCode(); 
	        result = prime * result + path.hashCode(); 
	        return result;
		}
	}

  hashCode取31是一个统计的结论，在接近2^x的质数下，散列冲突最小。没有看到过证明。

<!--more-->

  测试如下，value用String代替了。

	public void Test(){
		Map<ZkEventKey, String> map = new ConcurrentHashMap<TestMap.ZkEventKey, String>();
		ZkEventKey key1 = new ZkEventKey(EventType.NodeChildrenChanged, "/ua_server");
		ZkEventKey key2 = new ZkEventKey(EventType.NodeChildrenChanged, "/ua_server");
		map.put(key1, "Test Value");
		System.out.println(key1.equals(key2));
		System.out.println(map.get(key2));
	}

	结果：
	true
	Test Value




