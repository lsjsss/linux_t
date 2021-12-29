# if 条件表达式:
#     条件表达式为True的逻辑代码
# else:
#     条件表达式为False的逻辑代码
# bool(): 将其他的数据转换成True或者False，用于if判断
# 非空字符串，列表，元组，字典，
# 非零的数字表示的bool结果都为True
# None的bool结果为False
if -0.0:
    print("YES")
else:
    print("0的bool结果都为False")

if " ":  # 空字符串的布尔结果而False
    print("yes")
else:
    print("str NO")

if [False]:  # 空列表的布尔结果而False
    print("list yes")
else:
    print("list NO")

if (False, ):  # 空元组的布尔结果而False
    print("tuple yes")
else:
    print("tuple NO")

if {}:  # bool({})  空字典的布尔结果而False
    print("dict Yes")
else:
    print("dict No")
# None
if None:
    print("YES")
else:
    print("No")
# None   ""   []   ()    {}








# score = 59.9
# if score >= 60:
#     print("mom see no beat")
# else:
#     print("let me say you what good")
