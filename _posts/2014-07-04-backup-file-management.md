---
layout: article
title: "关于备份文件管理"
key: backup-file-management
date: 2014-07-04 11:20
comments: true
categories: "C++"
---

  最近在写一个备份的工作，备份线程每次会把需要备份的数据写到文件，同时需要保存一定数量的旧文件。

  首先为了写失败的时候不会损坏之前的旧备份文件，我们需要写一个临时文件然后覆盖回去。同时，为了保存旧文件，需要每次写一个不同的文件，同时维护一个当前的最新文件，然后删除超过了一定期限的文件，假定临时文件名是file.bin.2014xxxx，最新文件名是file.bin，有如下三个方法：

  1. 每次写临时文件，同时写一个内容一样的file.bin。造成空间浪费。
  2. 每次写临时文件，同时更新软链接file.bin。不兼容非linux系统。
  3. 写manifest，文件内容是当前最新文件名。比较麻烦。

  最后还是按2方案实现的，代码如下：

<!--more-->

	int overwrite_tmp_file(const char * filename, const int64_t version)
	{
	  char tmp_path[OB_MAX_FILE_NAME_LENGTH] ={'\0'};
	  int ret = OB_SUCCESS;
	  if (filename == NULL)
	  {
	    ret = OB_INVALID_ARGUMENT;
	  }
	  else
	  {
	    char time_str[OB_MAX_TIME_STR_LENGTH] = {'\0'};
	    tbsys::CTimeUtil::timeToStr(ObTimeUtility::extract_second(version), time_str);
	    int len = snprintf(tmp_path, sizeof(tmp_path), "%s.%s", filename, time_str);
	    if (0 > len || len >= static_cast<int32_t>(sizeof(tmp_path)))
	    {
	      ret = OB_ERR_UNEXPECTED;
	      TBSYS_LOG(WARN, "No file name specified!");
	    }
	    else
	    {
	      struct stat buf;
	      if (0 == lstat(filename, &buf))
	      {
	        if (0 != ::unlink(filename))
	        {
	          TBSYS_LOG(WARN, "fail to remove old file, msg: [%s]", strerror(errno));
	          ret = OB_ERR_SYS;
	        }
	      }
	      if (OB_SUCCESS == ret)
	      {
	        if (0 != ::symlink(basename(tmp_path), filename))
	        {
	          TBSYS_LOG(WARN, "fail to link backup file, msg: [%s]", strerror(errno));
	          ret = OB_ERR_SYS;
	        }
	        else if (OB_SUCCESS != clean_old_files(filename))//do not need to return error
	        {
	          TBSYS_LOG(WARN, "failed to remove old files");
	        }
	      }
	    }
	  }
	  return ret;
	}

	
	const static int64_t KEEP_FILE_RANGE = 3600 * 24 * 7;//7d,unit:s

	int clean_old_files(const char * filename)
	{
	  int ret = OB_SUCCESS;
	  if (filename == NULL)
	  {
	    ret = OB_INVALID_ARGUMENT;
	  }
	  else
	  {
	    char tmp_path[OB_MAX_FILE_NAME_LENGTH] ={'\0'};
	    glob_t globbuf;
	    globbuf.gl_offs = 0;
	    int len = snprintf(tmp_path, sizeof(tmp_path), "%s.*", filename);
	    if (len < 0 || len >= static_cast<int32_t>(sizeof(tmp_path)))
	    {
	      ret = OB_ERR_UNEXPECTED;
	    }
	    else if (0 != glob(tmp_path, GLOB_DOOFFS, NULL, &globbuf))
	    {
	      ret = OB_ERR_SYS;
	    }
	    else
	    {
	      int64_t cur_time = ObTimeUtility::extract_second(tbsys::CTimeUtil::getTime());
	      for(unsigned int i = 0; i < globbuf.gl_pathc; ++i)
	      {
	        int64_t version = tbsys::CTimeUtil::strToTime(globbuf.gl_pathv[i] + strlen(filename) + 1);
	        if (cur_time - version > KEEP_FILE_RANGE)
	        {
	          //delete file
	          if (0 != unlink(globbuf.gl_pathv[i]))
	          {
	            TBSYS_LOG(WARN, "fail to remove old file, msg: [%s]", strerror(errno));
	          }
	        }
	      }
	    }
	    globfree(&globbuf);
	  }
	  return ret;
	}
  
  需要注意的大概只有软连接文件属性获取是lstat而不是stat。另外，由于子文件夹的存在，建立软链接的symlink参数需要指定相对路径，也就是说，如果我们要让etc目录下的file.bin指向file.bin.2014xxxx，需要：

	ln -s file.bin etc/file.bin.2014xxx

  而不是

	ln -s etc/file.bin etc/file.bin.2014xxx  
  
  上面会导致链接文件指向etc/etc/file.bin.2014xxx而失效。