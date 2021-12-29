import sys  # 10:15上课
# sys.argv: 用列表接收命令行给py脚本传递的参数
def cal_two_num(num01, num02):
    # 通过命令行传递的参数都是字符串类型
    print(int(num01) + int(num02))
# 终端执行: python3 demo03_func.py 1 2
# sys.argv接收的参数是  demo03_func.py 1 2
# 最后拼接成一个列表用于保存:
#   sys.argv的值是: ['demo03_func.py', '1', '2']
# 把接收的1和2传递给函数调用的实参:
#    sys.argv[1]的值是1, sys.argv[2]的值是2
cal_two_num(sys.argv[1], sys.argv[2])