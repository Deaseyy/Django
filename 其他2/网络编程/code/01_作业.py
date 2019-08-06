import re
import requests

# 中文

chinesePattern = "[\u4e00-\u9fa5]+"
print(re.search(chinesePattern, 'hello世界'))

# 匹配手机号:
pattern = '^1\d{10}$'
print(re.search(pattern, '13988887777'))

# 匹配qq号： 5-11位, 第一位不能为0
pattern = '^[1-9]\d{4,10}$'
print(re.search(pattern, '610567895'))

# 匹配任意一个邮箱   如：jack@163.com，11@qq.com, aaa@sina.com.cn
pattern = '^\w+@\w+(\.\w+)+$'
print(re.search(pattern, 'aaa@sina.com.cn'))

# 匹配身份证: 18位，最后一位可能是X
pattern = '^\d{17}(\d|X)$'
print(re.search(pattern, '888888888888888123'))

# 邮政编码(共6位数字, 第一位不能为0)
pattern = '^[1-9]\d{5}$'

# 用户名(只能使用数字字母下划线, 且数字不能开头, 长度在6-15位)
pattern = '^[a-zA-Z_]\w{5,14}$'

# 简单日期格式 如："2017-11-11"，"2017-1-1"
pattern = '^\d{4}-\d{1,2}-\d{1,2}$'

# 图片文件格式 如："nbb.jpg", "aa.jpeg","aa.png", "aa.gif"
pattern = '^\w+\.(jpg|jpeg|png|gif)$'

# 匹配网址
# 1,匹配下列url网址
# http://www.baidu.com
# https://org.baidu.net
# https://www.sina.com.cn
reg = "https?://(\w+\.)+\w+"


# 2,匹配1和下列url网址
# https://www.baidu.com/index.html
# https://www.baidu.com:8080/aaa/bbb/index.asp
# https://www.baidu.com:80/ccc/ddd/login.html
reg = "https?://(\w+\.)+\w+(:\d+)?(/\w+)*(\.\w+)?"


# 3,匹配1和2以及下列带参数的url网址
# http://www.sina.cn:80/index.html?username=goudan
# https://org.baidu.com/login.asp?username=goudan&passwd=222
# https://www.sina.cn:8080/aaa/bbb/index.html?username=goudan&passwd=222&age=333
reg = "(https?://(\w+\.)+\w+(:\d+)?(/\w+)*(\.\w+)?(\?\w+=\w+)?(&\w+=\w+)*)"
print(re.findall(reg, 'https://www.sina.cn:8080/aaa/bbb/index.html?username=goudan&passwd=222&age=333'))

# https://org.baidu.com/login.asp?username=goudan&passwd=222
#   https:// : 网络协议
#   org.baidu.com ： 域名，域名包裹了IP, DNS域名解析（域名<==>IP）
#     80 ： 端口，对应电脑的某个程序
#   /login.asp : 路径
#   ?username=goudan&passwd=222  ： 参数
#

# 扩展：爬取51job的岗位名称和薪资
# url = "https://search.51job.com/list/040000,000000,0000,00,9,99,python,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare="

url = 'https://search.51job.com/list/040000,000000,0000,00,9,99,python,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='
res = requests.get(url)
string = res.content.decode('gbk')

pattern1 = '<div class="el">(.*?)</div>'
div_list = re.findall(pattern1, string, re.S)
# print(len(div_list))

for div in div_list:
    t2 = re.findall('<span class="t2">(.*?)</span>', div, re.S)
    t4 = re.findall('<span class="t4">(.*?)</span>', div, re.S)

    # print(t2)
    # print(t4)

    company = re.findall('<a target="_blank" title="(.*?)"', t2[0], re.S)[0]
    salary = t4[0]
    print(company, salary)



