---
layout: post
title: "自动生成octopress的分类目录"
date: 2015-01-10 22:28
comments: true
published: true
categories: "web相关"
---
  在octopress里面添加一个分类的时候，经常会遇到分类跟导航页面没有同步更新的情况，即加了一个分类，生成了文章，文章被生成在指定的路径下了，但是首页导航栏的分类没有跟着更新。针对这种情况，修改了一下Rakefile，把分类做成了配置，添加分类的时候可以直接修改一下分类信息，然后`rake gen`就可以生成对应的导航栏html代码。

  修改如下（我以前增加过交互的提示选择分类的功能），需要解释的有如下几点：

  1. "----"是分割线，-的数量不能都一样，毕竟是作为map的key的。
  2. 分类做成map是因为category生成的时候名字自动做成了英文/拼音/中横线的形式...我没搞明白怎么弄的。所以自己手动填一下好了。以后有空想做成手动指定的。
  3. system sublime那个是自动打开sublime写博客。我不习惯用vim写中文的博客...

<!--more-->
  
  配置部分

	category_path ='source/_includes/categories.html'
	categories={
	    "技术相关"=>{
	        "软件发布"=>"ruan-jian-fa-bu",
	        "---------"=>"",
	        "C++"=>"c-plus-plus",
	        ".Net"=>"dot-net",
	        "Flex"=>"flex",
	        "基础理论"=>"ji-chu-li-lun",
	        "Latex"=>"latex",
	        "Linux"=>"linux",
	        "MFC"=>"mfc",
	        "Oceanbase"=>"oceanbase",
	        "分布式系统"=>"fen-bu-shi-xi-tong",
	        "PHP"=>"php",
	        "Java"=>"java",
	        "Python"=>"python",
	        "vim"=>"vim",
	        "web相关"=>"web",
	        "其他"=>"others",
	        "----------"=>"",
	        "IT人生"=>"ai-ti-ren-sheng",
	    },
	    "世情百态"=>"shi-qing-bai-tai",
	    "摄影"=>"she-ying",
	    "随笔" =>"sui-bi" }

  rake gen生成导航的html的部分。

	desc "Generate jekyll site"
	task :gen do
	    html=''
	    for key,value in categories
	        if value.is_a?(Hash)
	            html << '<li class="dropdown">' << "\n"
	            html << '<a data-toggle="dropdown" class="dropdown-toggle" href="#">%s<b class="caret"></b></a>'%[key] << "\n"
	            html << '<ul class="dropdown-menu">' << "\n"
	            for key,value in value
	                if key.start_with?('-')
	                    html << "\t"'<li class="divider"></li>' << "\n"
	                else
	                    html << "\t"'<li><a href="{{ root_url }}/category/%s">%s</a></li>'%[value, key.strip] << "\n"
	                end
	            end
	            html << '</ul>' << "\n"
	            html << '</li>' << "\n"
	        else
	            html << '<li><a href="{{ root_url }}/category/%s">%s</a></li>'%[value, key.strip] << "\n"
	        end
	    end
	    File.open(category_path, 'w') { |file| file.write(html) }
	end

  交互提示分类并generate new post的部分。

	# usage rake new_post[my-new-post] or rake new_post['my new post'] or rake new_post (defaults to "new-post")
	desc "Begin a new post in #{source_dir}/#{posts_dir}"
	task :new_post, :title, :category do |t, args|
	  if args.title
	    title = args.title
	  else
	    title = get_stdin("Enter a title for your post: ")
	  end
	  if args.category
	    category = args.category
	  else
	    #output an array
	      category_arr = []
	      category_idx = 0
	      puts "===================================================="
	      for key,value in categories
	          if value.is_a?(Hash)
	              puts key
	              for key,value in value
	                  if not key.start_with?('-')
	                      puts "%d\t%s"%[category_idx, key]
	                      category_arr.push(key)
	                      category_idx +=1
	                  end
	              end
	          else
	              puts "%d %s"%[category_idx, key]
	              category_arr.push(key)
	              category_idx +=1
	          end
	      end
	      puts "===================================================="
	    i = get_stdin("Enter a title for your category: ")
	    category = category_arr[Integer(i)].gsub(/\s/,'')
	  end

	  raise "### You haven't set anything up yet. First run `rake install` to set up an Octopress theme." unless File.directory?(source_dir)
	  mkdir_p "#{source_dir}/#{posts_dir}"
	  filename = "#{source_dir}/#{posts_dir}/#{Time.now.strftime('%Y-%m-%d')}-#{title.to_url}.#{new_post_ext}"
	  system "echo #{filename} |xclip -i -selection clipboard "
	  if File.exist?(filename)
	    abort("rake aborted!") if ask("#{filename} already exists. Do you want to overwrite?", ['y', 'n']) == 'n'
	  end
	  puts "Creating new post: #{filename}"
	  open(filename, 'w') do |post|
	    post.puts "---"
	    post.puts "layout: post"
	    post.puts "title: \"\""
	    post.puts "date: #{Time.now.strftime('%Y-%m-%d %H:%M')}"
	    post.puts "comments: true"
	    post.puts "published: true"
	    post.puts "categories: \"#{category.gsub(/&/,'&amp;')}\""
	    post.puts "---"
	  end
	  system "LD_PRELOAD=~/repo/scripts/libsublime-imfix.so nohup ~/share/sublime/sublime_text #{filename} >/dev/null 2>&1 &"
	end

  修改custom/navigation.html，让导航部分导入生成的categories.html

	<ul class="nav">
	    <li><a href="{{ root_url }}/blog/archives">Archives</a></li>
	    <li class="divider-vertical"></li>
	    {\% include categories.html \%}
	</ul>

