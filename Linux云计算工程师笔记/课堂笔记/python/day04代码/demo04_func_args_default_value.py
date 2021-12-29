# 在函数内部可以调用函数，例如在函数内部print()数据
# 正确姿势:
def cal_two_num(num01, num02=10):
    print(int(num01) + int(num02))
cal_two_num(1, 2)#如果实参赋值，会替换掉形参已有的默认值
cal_two_num(20)

# 有默认值的参数一定要放到形参列表的末尾
# def cal_two_num02(num01=10, num02):  错误
#     print(int(num01) + int(num02))
# cal_two_num02(10)
