---
layout: post
title: "About random shuffle in cplusplus"
date: 2015-02-01 19:14
comments: true
published: true
categories: "C++"
---
   Actually I just want to memorize the usage of STL function random_shuffle. It takes two or threes arguments, the begin iterator, end iterator and a generator. What makes it interesting is the optional third parameter. Random_shuffle will pass the index to generator and takes the output as index to place current element while shuffling. Here is an example:

	#include <iostream>
	#include <algorithm>
	#include <vector>
	#include <ctime>
	#include <cstdlib>

	using namespace std;
	const int POKER_NUM = 52; //52 pocker cards
	void print_poker(int PokerNum)
	{
	    cout << PokerNum << " ";
	}

	class MyRand
	{
	public:
	    int operator()(int index)
	    {
	        return rand() % PockerNum;
	    }
	};

	int main()
	{
	    srand( (unsigned)time(NULL) ); //rand seed
	    vector<int> poker; 
	    //initialize
	    for (int num = 0; num < POKER_NUM; ++num)
	    {
	        poker.push_back(num+1);
	    }

	    //with default random_shuffle
	    random_shuffle(poker.begin(), poker.end());
	    for_each(poker.begin(), poker.end(), print_poker);
	    cout << endl;

	    //use custom random_shuffle
	    random_shuffle(poker.begin(), poker.end(), MyRand());
	    copy(poker.begin(), poker.end(), ostream_iterator<int>(cout, " "));
	    cout << endl;
	}

  I copy it from [here][1]. While I found a mistake in it. The result isn't really random. The pseudo-code of above is :

  	for i in 0..n
  		exchange a[i] and a[random(0..n)]

  We assume a method can generate a sequence(a[0]..[n]) randomly, which means each sequence appears with the probability 1/n!. Take certain sequence a[0']...a[n'] as an example: a[0'] appears with the probability 1/n, so a[1'] should appear with the probability 1/(n-1), etc. The algorithm above find a[1'] in the whole candidates, makes the probability 1/n actually. The right algorithm is like this:

  	for i in 0..n
  		exchange a[i] and a[random(i..n)]

  With a little change in the code:

  	class MyRand
	{
	public:
	    int operator()(int index)
	    {
	        return rand() % (PockerNum - index) + index;
	    }
	};



[1]: http://blog.csdn.net/aheroofeast/article/details/3907192   "random_shuffle算法小例子"
[2]: http://www.amazon.cn/%E7%AE%97%E6%B3%95%E5%AF%BC%E8%AE%BA-Thomas-H-Cormen/dp/B00AK7BYJY "	"Algorithms"

###Bibliography:

>\[1] random_shuffle算法小例子, <http://blog.csdn.net/aheroofeast/article/details/3907192>

>\[2] 	"Algorithms, <http://www.amazon.cn/%E7%AE%97%E6%B3%95%E5%AF%BC%E8%AE%BA-Thomas-H-Cormen/dp/B00AK7BYJY>