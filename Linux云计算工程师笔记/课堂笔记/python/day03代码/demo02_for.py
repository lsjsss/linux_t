# for
# for 变量 in 可迭代对象:
#     for 循环逻辑
# cart 表示购物车
cart = ["巧克力派", "鱿鱼丝", "碎冰冰", "Python从入门到入坟"]
for item in cart:
    print("saoma: " + item)
print("*" * 30)
# 求总价
total_price = 0
cart_price = [10, 15, 5, 99.99]
for price in cart_price:
    total_price += price
print("total price: " + str(total_price))
