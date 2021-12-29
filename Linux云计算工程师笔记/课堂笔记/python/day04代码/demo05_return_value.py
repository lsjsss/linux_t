# 函数的返回值  return 返回值
# 计算两个数的和并返回
# res = cal_two_num03(1, 2)   res: 3
def cal_two_num03(a, b):
    a = int(a)
    b = int(b)
    if a > b:
        return a - b
    else:
        return a + b  # 把结果返回来
res = cal_two_num03(1, 2)  # res = 3
print(res)
# 有返回值可以做后续的操作: 例如判断两个数的和是不是偶数
# if res % 2 == 0:
#     print("偶数")


def cal_two_num(a, b):
    print(int(a) + int(b))
    return None
res = cal_two_num(1, 2)
print("res:", res)  # res: None
