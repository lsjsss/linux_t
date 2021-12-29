# 逻辑运算符
# & | !    -->   and  or  not
# and最后结果为真, 保证and左右两边的表达式同时为真
res = 3 > 1 and 3 > 2  # and 并且
res = 3 > 1 and 3 < 2  # and 并且
# or 或者: or左右两边有一边儿为真，则整个表达式的结果为真
res = 3 > 1 or 3 < 2
print(res)
res = 3 < 1 or 3 < 2
print(res)
# not 非, 取反:
# 原表达式为真加not则为假  原表达式为假加not则为真
print(not 1 > 0)
print(not 1 != 1)








