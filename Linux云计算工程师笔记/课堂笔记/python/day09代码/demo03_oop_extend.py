# 继承
class A:
    def test01(self):
        print("test1")
    def test02(self):
        print("test2")
class B(A):  # B继承A类，A是B的父类
    pass
b1 = B()
b1.test01()  # 调用A的test01()方法
b1.test02()
# a1 = A()
# a1.test01()
# a1.test02()
