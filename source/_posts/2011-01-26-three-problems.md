---
title: 记三个小问题
author: Harry Chen
layout: post

categories:
  - Others
tags:
  - sql server
  - 安装路径
  - 引导菜单
  - 拒绝访问
  - 默认
---
# 

今天遇到的三个小问题，这里记下来，留个备份吧。

第一个是装机的时候想要是能自动安装软件到D盘就好了，省了每次手动填写安装路径的麻烦，解决方法其实很简单：

> 开始菜单里的“运行”，输入“regedit”，来运行注册表编辑器，展开
“HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion”分支。在右侧的窗口中，把“ProgramFilesDir”和“CommonFilesDir”字符串值改为其它目录即可

第二个问题是恢复数据库的时候，遇到一个错误提示：

> System.Data.SqlClient.SqlError: 在对 ‘C:\Program Files\Microsoft SQL Server\MSSQL.1\MSSQL\BusinessDB.mdf’ 尝试 ‘RestoreContainer::ValidateTargetForCreation’ 时，操作系统返回了错误 ’5(拒绝访问)’

其实主要的问题在于没有对"C:\Program Files\Microsoft SQL Server\MSSQL.1\MSSQL\"创建文件的权限（可以把它复制到data），这是SQL2005对文件夹的安全性限制。所以把还原路径换成别的即可。

第三个问题是关于多windows系统安装的引导菜单修改，这个问题就更简单了，只需要在系统属性\高级\启动和故障恢复里，点手动编辑，之后的文件格式通俗易懂，不需要多说。

最后鄙视一下360，客户端软件真是流氓的天下，只有流氓才TM能生存，360真是拿顾客当小白鼠了……

参考文献：

[1]通过注册表修改软件默认安装目录，

[2]解决SQL Server 2005 还原数据库错误，
