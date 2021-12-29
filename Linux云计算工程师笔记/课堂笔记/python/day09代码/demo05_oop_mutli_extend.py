# 多继承
class A:
    def func1(self):
        print("A func")
    def func4(self):
        print("A func4")
class B:
    def func2(self):
        print("B func")
    def func4(self):
        print("B func4")
class C(B, A):  # C继承A也继承B
    pass
    # def func4(self):
    #     print("C func4")
c2 = C()
c2.func4()
