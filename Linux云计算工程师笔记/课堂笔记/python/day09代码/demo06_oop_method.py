# 魔术方法: __str__   __call__
class Role:
    def __init__(self, name, weapon):
        self.name = name
        self.weapon = weapon
    def __str__(self):  # 修改print(r1)的结果
        return "name: %s, weapon: %s" % \
               (self.name, self.weapon)
    def __call__(self):
        print("%s使用了%s" % (self.name, self.weapon))
r1 = Role("zs", "shouqiang")
# print(r1)  # <__main__.Role object at 0x7fb8f99f8438>
print(r1)  # name: zs, weapon: shouqiang
r1()  # 当成函数调用. 调用__call__()
