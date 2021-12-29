# write 方法 —— 写文件
# 1.打开文件
# 读一个不存在的文件，会报错,写一个不存在的文件，不会报错，
# 系统会帮我们创建一个这样的文件
fw = open("/tmp/aaa.txt", mode="w")
# 2.写操作
# fw.write("hello world\n")  1.直接写
line_list = ["hello\n", "world\n", "test\n"]
#       2. 把列表当中的元素按顺序写入文件
#       如果想写多行，需要手动给列表中每个元素后加\n
fw.writelines(line_list)
# 3.关闭资源
fw.close()
