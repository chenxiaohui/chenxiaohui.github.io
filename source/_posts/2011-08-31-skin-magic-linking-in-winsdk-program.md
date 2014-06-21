---
title: SkinMagic在WinSDK程序中的链接
author: Harry Chen
layout: post

categories:
  - MFC
  - 与技术相关
tags:
  - SkinMagic
  - WinSDK
---
# 

  其实这种诡异的搭我配估计没人会遇到。我只是想在SDK程序里做一下美化而已。

  SkinMagic在MFC程序里的使用还是很常见的，网上代码有的是，至于大家手里的SkinMagic库，恐怕没有几个是正版的吧？有木有有木有！

  其实在SDK下使用SkinMagic还是比较简单的事情，主要解决两个问题：

  1. 库的链接
  2. 皮肤的导入

  第一个其实好说，注意InitSkinMagicLib传入WinMain的hInstance：


    VERIFY( 1 == InitSkinMagicLib(hInstance, NULL , NULL, NULL ));
    VERIFY( 1 == LoadSkinFromResource(NULL,MAKEINTRESOURCE(IDR_SKIN5),"skin"));
    VERIFY( 1 == SetDialogSkin( "Dialog" ) );

  然后记得导入库就行


    #pragma  comment(lib,"SkinMagicTrial")
    #include "SkinMagicLib.h"

  第二个问题，由于是SDK程序，所以需要手动添加资源，然后在资源里建立SKIN项，再导入皮肤，这时候VS会自动建立resource.h文件。

![image][1] 然后就OK啦。如果自己建立窗口，记得对ShowWindow之前调用一下SetWindowSkin。我只弹了个对话框，效果如下

![image][2]

   [1]: http://www.roybit.com/wp-content/uploads/2011/08/image_thumb.png (image)
   [2]: http://www.roybit.com/wp-content/uploads/2011/08/image_thumb1.png (image)
