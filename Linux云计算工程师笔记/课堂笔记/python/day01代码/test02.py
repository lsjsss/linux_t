# 练习 1：买包子
# 包子的价格是 1.5 元/个
# 买了10个包子
# 今天老板高兴，总价打 9 折
# 计算付款金额
price = 1.5
number = 10
money = price * number
# 总价打 9 折
money *= 0.9  # 与money = money * 0.9含义相同
# str(变量)  int -> str
# int(变量)  str -> int
print("总价是: " + str(money) + " 元")
