# 字符串格式化
name = "zs"
age = 18
# 姓名：zs，年龄：18
# 拼接
# print("姓名：" + name + ", 年龄：" + str(18))
# 格式化
print("姓名：%s, 年龄：%d" % (name, age))
print("整数不足5位，左边补0  %05d   " % 22)
# 11:23上课
print("浮点数：%f,%f " % (1, 22.22))
print("浮点数保留两位小数：%.2f  " % 22.222)
# %s: 包罗万物，接收其他类型的数据
print("%s, %s, %s" % (1, 1.1, ["aaa", 1]))

# format
# 最常用的方式: 按照默认位置复制
print("{}:{}".format("zs", 18))
# 22, 11没有用，因为点名道姓
print("{name}:{key}".format(
        22, 11, name="帅哥", key=18
    )
)
# test给到没有点名道姓的坑 {}
print("{name}:{key}:{}".format(
    "test", name="帅哥", key=18))

