---
layout: article
title: "Linux ssh免密登陆和调试"
date: 2015-03-07 17:56
comments: true
published: true
categories: "Linux"
---
   把一个公钥上传到服务器配置了免密登陆，ok之后再配置几台服务器之间的免密，发现不成功。尝试了如下几种定位方法：

 1. ssh目录权限。修改成.ssh 700，下面文件600。解决了一个的问题。其他几台还是不行。
 2. 查看sshd_config是否允许公钥登陆。看来不是这个问题。
 2. ssh -v 看调试信息，发现尝试过publickey但是验证未通过。手动比对ssh 公钥发现无误。
 3. 搜索错误信息：Offering public key: /root/.ssh/id_rsa，有人说[是因为.ssh目录没有ssh_home_t标签][1]， 通过这个命令查看文件夹或文件的标签

		[root@localhost ~]# ls -laZ
	
	通过
		
		restorecon -r -vv /root/.ssh

	来重置标签，但是没起作用。

 4. 设想可能是手动建立.ssh目录的问题，删除.ssh，通过ssh-keygen本地生成密钥并建立目录。问题解决。

   补充一点细节。bash下似乎单行的function必须以分号结尾，我说怎么server登陆总报error end line xxx..


 [1]: http://segmentfault.com/q/1010000000445726   "CentOS SSH公钥登录问题"
 [2]: