# read--读取文件
# 1. 打开文件
fr = open("/etc/passwd", mode="r")
# 2. 读取文件
# text = fr.read() # 1.一次性将文件中的内容全部读取出来
# text = fr.read(10)  # 2.读取指定个字符的数据
# print(fr.readline())  # 3.读取一行数据
# 4.把文件中所有的数据按行添加到列表当中
#   列表当中每一个元素就是一行数据
lines = fr.readlines()
print(lines[10])  # 获取第11行数据
print(lines)
# 3. 关闭资源
fr.close()