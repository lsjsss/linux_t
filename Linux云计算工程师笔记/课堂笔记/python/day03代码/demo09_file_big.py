# 案例：读取大文件的正确姿势
# 1. 打开文件
fr = open("/etc/passwd", mode="r")
# open(filename, mode="rb")读二进制
# 2. 读取文件  fr.readline()
while True:  # 死循环
    text = fr.readline()
    if not text:  # if text == "":
        break  # 文件读完了
    print(text, end="")
# 3. 关闭资源
fr.close()
