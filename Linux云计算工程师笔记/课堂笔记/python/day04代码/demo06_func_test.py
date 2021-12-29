### 练习 3：斐波那契数列函数
# 斐波那契数列函数
# - 将斐波那契数列代码改为函数
# - 数列长度由用户指定
# - 要求把结果用 return 返回
def gen_fib(length):  # length = 10
    fib = [0, 1]
    for i in range(length-2):  # 控制循环次数
        fib.append(fib[-1] + fib[-2])
    return fib
res_fib = gen_fib(10)
print(res_fib)