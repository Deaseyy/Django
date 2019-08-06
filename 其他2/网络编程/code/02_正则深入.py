''''''

'''
复习：
    正则表达式
        re.match()
        re.search()
        re.findall()
    
    符号：
        -- 单个字符 --
            . 表示单个任意字符，除了换行
            [] 表示单个字符的范围
                [0-9] [a-z] [1-9]
            \d \D
            \w \W
            \s \S
        
        -- 出现次数 --
            *  任意多次0~n
            +  1次或多次 1~n
            ?  0次或1次
            {} 指定次数范围
                {5} {2,5} {4,} {,5}
        
        -- 边界 --
            ^ 
            $
            ^ $
        
        -- 分组 --
            ()
            (?P<name>\d+)
            
        -- 其他 --
            | 或
            \ 转义
'''

import re

# 正则的拆分
string = 'hello world-你-好-吗'
print(re.split(' |-', string))

# 正则的替换
string = '川普是大佬,金三胖是大佬,金大胖是大佬'
print(re.sub('.{2,3}是', '习大大是', string))

print(re.subn('.{2,3}是', '习大大是', string))


# 正则编译
#   ：可以提交正则效率
comp = re.compile('g.gle')
print(comp.search('gogle'))
print(comp.match('gogle'))
print(comp.findall('gogle'))


# findall
print(re.findall('((\d{4})-(\d{8}))', '0755-99998888'))

# finditer
res = re.finditer('\d+', '0755-99998888')
for i in res:
    print(i)
    print(i.group())
    print(i.span())












