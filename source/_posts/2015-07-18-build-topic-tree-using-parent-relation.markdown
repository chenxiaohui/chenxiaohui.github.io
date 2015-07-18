---
layout: post
title: "通过父子关系构建话题树"
date: 2015-07-18 11:35
comments: true
published: true
categories: "基础理论"
---
  
  一道题目，本来觉得挺简单的，后来卡在一个小问题上。mark一下：

  给定一个数据库表，存了所有话题的关系，形式是：parent->child，表示前面是后面话题的父话题。根据这个关系构建出话题树并打印。

  	eg:
  	输入：
	  	a b
	  	c a
	  	d e
	  	e f
	  	r c
	  	r d
	输出：
		 r
		   c
		     a
		       b
		   d
		     e
		       f
	题目隐含：
		1. DAG：有向无环
		2. 节点不重复

  直观看类似于Graphviz的算法，只不过保证了是棵树。C++实现上可以直接通过树来做，这里用了Python。

<!--more-->

  思路上先找到父节点，再找到子节点，如果都找到，那么移动子节点到父节点下形成一个新的成员，如果父节点没找到，让其成为root节点（加一个叫root的dummynode，反正是话题，我们保证这个话题是保留字）的子节点，如果子节点没找到，让其形成一个新的空节点。

  Python下数据结构类似于：

    ret = {
        "root": {
            "r": {
                "c": {
                    "a":{
                    	"b":{}
                    	},
                },
                "d":{
                    "e":{
                    	"f":{}
                    }
                }
            }
        }
    }

  叶节点都保留了一个空的子节点集合。

  代码如下：

	default_indent = 2
	filename='topic'

	def print_result(tree, indent):
	    """"""
	    for key, value in tree.items():
	       if key:
	           print ' ' * indent, key
	       if value:
	           print_result(value, indent + default_indent)


	def find_node(tree, element):
	    """"""
	    for key, value in tree.items():
	        if key == element:
	            return tree, tree[key]
	        elif value:
	            parent, child = find_node(value, element)
	            if parent:
	                return parent, child
	    return None, None

	def parse_file(ret, fp):
	    """"""
	    for pair in fp:
	        pair = pair.strip("\n")
	        if pair:
	            parent, child = pair.split()
	            _, parent_element = find_node(ret, parent)
	            child_parent, child_element = find_node(ret, child)

	            if parent_element == None:
	                ret["root"][parent] = {}
	                parent_element = ret["root"][parent]
	            if child_element == None:
	                child_element = {}

	            parent_element[child] = child_element
	            if child_parent:
	                del child_parent[child]

	if __name__ == '__main__':
	    ret = {"root":{}}
	    try:
	        with open(filename, 'r') as fp:
	            parse_file(ret, fp)
	    except Exception:
	        raise

	    print_result(ret['root'], 0)
  
  之前出的错误是：

1. python毕竟是引用计数，把一个节点变成另外一个节点的子节点的时候忘了remove旧的节点
2. 深度优先搜索找节点的时候直接return find_node(xxx)了，这样的话深度完一个子节点，不会再继续本层循环了。这个也是大意了，随手一测这个find_node函数就没再看。

  性能提升的办法主要是：
1. hash一下所有的节点。把遍历查找的复杂度降下来
2. 先排序（按照parent)，然后把reduce，这样会先把相同的部分生成一个集合，比如a:[b,c,d]这种。
