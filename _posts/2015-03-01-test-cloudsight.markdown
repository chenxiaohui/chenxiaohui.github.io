---
layout: article
title: "测试下CloudSight的图像识别"
date: 2015-03-01 20:58
comments: true
published: true
categories: "其他"
---
  偶然看到[这个][1]链接，一个识别图像并标注的，还蛮有意思。代码直接用示例里面的就可以, 需要注意两个问题：

  1. [注册一个项目][2]。ResponseType选择Product。
  2. 必须上传网络链接，不能使用文件。

  测试几个效果（多次返回结果不一定一样）：

  1. [百度首页][4]，识别为"百度标志"
  2. [陈吉宁校长的头像][3]，识别为"男人的黑色西装外套" 或 "男人的蓝色西装"
  3. [我博客一张背景图][5]，识别为"女性的黑色T恤" 或 "红色的通勤自行车"

  让我突然对这个tag算法很感兴趣。

  [1]: http://buzz.beebeeto.com/topic/45/   "使用CloudSight API进行图像识别的Python脚本"
  [2]: https://cloudsightapi.com/api_clients/new "New Project"
  [3]: http://ww4.sinaimg.cn/bmiddle/61d83ed4jw1epqi6itn8mj20az08caa8.jpg "陈吉宁校长"
  [4]: http://www.baidu.com/img/bdlogo.png "百度标识"
  [5]: http://cxh.me/images/common/baiyipiaopiao.jpg "背景图"