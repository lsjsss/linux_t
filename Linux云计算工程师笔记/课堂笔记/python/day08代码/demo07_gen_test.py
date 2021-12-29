### 练习 4：文件生成器
# **需求**：通过生成器完成以下功能
# - 使用函数实现生成器   yield
# - 函数接受一个文件对象作为参数
# - 生成器函数每次返回文件的 10 行数据
def gen_block(fname):
    lines = []
    fr = open(fname, mode="r")
    for line in fr:  # fr.readlines():
        lines.append(line)
        if len(lines) == 10:  # 当列表长度为10的时候
            yield lines
            lines = []  # 列表置空
    if lines != []:
        yield lines  # 将不足10行的数据再次弹出
    fr.close()
if __name__ == '__main__':
    line_gen = gen_block("/etc/passwd")
    for line_10 in line_gen:
        print(line_10)  # line_10 长度=10的列表
        print("*" * 30)
