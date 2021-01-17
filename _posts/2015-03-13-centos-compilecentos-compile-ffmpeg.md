---
layout: article
title: "centos下编译ffmpeg"
key: centos-compilecentos-compile-ffmpeg
date: 2015-03-13 11:27
comments: true
published: true
categories: "Linux"
---

  先安装能通过yum直接安装的

    yum install autoconf automake gcc gcc-c++ git libtool make nasm pkgconfig wget zlib-devel
  	yum install yasm SDL SDL-devel dirac dirac-devel gsm gsm-devel libvpx libvpx-devel gnutls gnutls-devel freetype freetype-devel openjpeg openjpeg-devel opus opus-devel

  剩下lame lame-devel libvpxlame-devel xvidcore xvidcore-devel faac faac-devel opencore-amr opencore-amr-devel faad2 a52dec libfaac 手动安装

<!--more-->

  安装libfaac
  
  	wget http://downloads.sourceforge.net/project/faac/faac-src/faac-1.28/faac-1.28.tar.gz
	  tar xvfz faac-1.28.tar.gz
	  cd faac-1.28/
	  修改源码：
	  ./bootstrap
	  ./configure --prefix=$HOME --enable-shared
	  make
	  make install
  
  安装libfdk_aac

  	wget http://jaist.dl.sourceforge.net/project/opencore-amr/fdk-aac/fdk-aac-0.1.4.tar.gz
  	tar zxvf fdk-aac-0.1.4.tar.gz
    cd fdk-aac-0.1.4
  	./autogen.sh
  	./configure --prefix=$HOME --enable-shared
	  make
	  make install
  
  安装mp3lame

  	wget http://jaist.dl.sourceforge.net/project/lame/lame/3.99/lame-3.99.5.tar.gz
  	tar zxvf lame-3.99.5.tar.gz
  	cd lame-3.99.5.tar.gz
    ./configure --prefix=$HOME --enable-shared
	  make
	  make install	

  安装opencore-amr

    wget http://jaist.dl.sourceforge.net/project/opencore-amr/opencore-amr/opencore-amr-0.1.3.tar.gz
    tar zxvf opencore-amr-0.1.3.tar.gz
    cd opencore-amr-0.1.3
    ./configure --prefix=$HOME --enable-shared
	  make
	  make install	
 
  安装 vo_aacenc

  	wget http://heanet.dl.sourceforge.net/project/opencore-amr/vo-aacenc/vo-aacenc-0.1.3.tar.gz
	  tar zxvf vo-aacenc-0.1.3.tar.gz
	  cd vo-aacenc-0.1.3
	  ./configure --prefix=$HOME --enable-shared
	  make
	  make install
  
  安装libx264

  	git clone git://git.videolan.org/x264.git
  	cd x264
	  ./configure --prefix=$HOME --enable-shared
	  make 
	  make install


  安装ffmpeg

  	git clone git://source.ffmpeg.org/ffmpeg.git ffmpeg
  	cd ffmpeg
    ./configure --prefix=$HOME --enable-libfaac --enable-libfreetype --enable-libmp3lame --enable-libopencore-amrnb --enable-libopencore-amrwb --enable-libopenjpeg --enable-libvo-aacenc --enable-libvorbis --enable-libvpx --enable-shared --enable-libx264 --enable-gpl --enable-nonfree --enable-version3 --enable-openssl --enable-gnutls --enable-zlib --extra-cflags="-I $HOME/include" --extra-ldflags="-L $HOME/lib"
  	make 
  	make install

  安装libav

  	wget https://libav.org/releases/libav-11.2.tar.gz
  	tar zxvf libav-11.2.tar.gz
  	cd libav-11.2
  	export PKG_CONFIG_PATH=$HOME/lib/pkgconfig
  	./configure --prefix=$HOME --enable-libfaac --enable-libfdk-aac --enable-libfreetype --enable-libmp3lame --enable-libopencore-amrnb --enable-libopencore-amrwb --enable-libopenjpeg --enable-libopus --enable-libvo-aacenc --enable-libvorbis --enable-libvpx --enable-shared --enable-libx264 --enable-gpl --enable-nonfree --enable-version3 --enable-openssl --enable-gnutls --enable-zlib --extra-cflags="-I $HOME/include" --extra-ldflags="-L $HOME/lib"
  	make 
  	make install

  安装mplayer，只用来编解码，不需要界面

    ./configure --prefix=$HOME --disable-gui --codecsdir=DIR

  去掉了一些不用的：

  	--enable-rtmp --enable-libschroedinger   --enable-libspeex --enable-libtheora
