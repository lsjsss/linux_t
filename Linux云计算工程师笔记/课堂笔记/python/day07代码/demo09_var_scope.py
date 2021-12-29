# 变量的作用域
# 全局变量: 在函数外部定义变量  可见性：函数内外
# a = 10
# def func01():
#     print("in func:", a)
# func01()
# print("out func01:", a)
# 局部变量:在函数内部定义变量,在函数内部可见,在函数外部不可见
# def func02():
#     b = 10
#     print("in func02:", b)
# func02()
# print("out func02:", b)  报错
x = 100
def func03():
    x = 200
    print(x)  # 200 优先使用函数内部的局部变量
func03()
print(x)  # 100

c = 1
def func04():
    # 在函数内部声明：使用的是函数外部的全局变量c
    global c
    c = 2  # 对函数外部的全局变量c进行重新赋值
    print(c)
func04()
print(c)  # 1




