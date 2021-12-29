# 面向对象
# 创建类
class BearToy:
    # 初始化函数：一般用于属性的赋值
    def __init__(self, color, size):  # self: 当前对象
        self.color = color  # 属性
        self.size = size
    def speak(self):  # 行为
        print("你好我是 %s %s 泰迪~"%
              (self.color, self.size))
bear1 = BearToy("red", "big")  # 创建对象
print(bear1.color)
bear1.speak()
bear2 = BearToy("blue", "small")
bear2.speak()



# bear1.size = "big"  # 给对象创建属性并赋值
# bear1.color = "red"
# bear1.lunzi = 4  # 避免出现
# bear1.speak()  # 通过对象的引用调用方法






# bear2 = BearToy()  # 创建对象
# bear2.size = "small"
# bear2.color = "green"
# bear2.speak()
