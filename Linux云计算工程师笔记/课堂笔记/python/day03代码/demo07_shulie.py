# 练习：斐波那契数列
# 1. 斐波那契数列就是某一个数，总是前两个数之和，
# 比如 0，1，1，2，3，5，8
# 2. 使用for循环和range函数编写一个程序，
# 计算有10个数字的斐波那契数列
# 3. 改进程序，要求用户输入一个数字，
# 可以生成用户需要长度的斐波那契数列
# fib = [0, 1, 1, 2, 3, 5, 8, 13]
# fib.append(fib[-1] + fib[-2])
fib = [0, 1]
length = int(input("num: "))
for i in range(length-2):  # 控制循环次数
    fib.append(fib[-1] + fib[-2])
print(fib)