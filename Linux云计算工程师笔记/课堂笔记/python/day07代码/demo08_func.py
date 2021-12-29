# 函数不允许在函数未声明之前，对其进行引用或者调用
# def foo():
#     print("in foo")
# def bar():
#     print("in bar")
# bar()
# foo()

# 关键字参数：指名道姓赋值，不关心位置
# 位置参数应写在关键字参数前面
def get_age(name, age):
    print("%s is %s years old" % (name, age))
get_age("zs", 18)  # 位置传参
get_age(18, "zs")
get_age(age=18, name="zs")  # 关键字传参
get_age("nfx", age=19)
# get_age(name="nfx", 20)


