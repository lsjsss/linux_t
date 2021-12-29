# 文件的迭代(遍历)
fr = open("/etc/passwd", mode="r")
# line_list = fr.readlines()
# for line in line_list:  # 遍历
#     print(line, end="")
for line in fr:  # 等同于for line in fr.readlines()
    print(line, end="")
fr.close()
