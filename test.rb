#!/usr/bin/env ruby -wKU
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
#File.open(category_path, 'w') { |file| file.write(html) }

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
#category = categories[Integer(i)].gsub(/\s/,'')

