# 战士类(Warrior)和法师类(Mage)都是Role的子类
class Role:
    def __init__(self, name, weapon):
        self.name = name
        self.weapon = weapon
    def show_me(self):
        print("我是%s 我的武器是%s"
              %(self.name, self.weapon))
class Warrior(Role):  # Role是Warrior父类
    # 第一种：抄一遍父类init函数, 不推荐
    # def __init__(self, name, weapon, ride):
    #     self.name = name
    #     self.weapon = weapon
    #     self.ride = ride  # 添加坐骑
    def __init__(self, name, weapon, ride):
        # 调用父类当中的init函数
        Role.__init__(self, name, weapon)
        self.ride = ride
    def attack(self,target):#子类封装自己特有的方法即可
        print("与 %s 近身肉搏" % target)
    def show_me(self):  # 重写父类的方法
        print(self.name, self.weapon, self.ride)


class Mage(Role):
    def attack(self, target):
        print("远程打击 %s " % target)
lb = Warrior("吕布", "方天画戟", "赤兔马")
lb.show_me()  # 调用的warrior类中的show_me
lb.attack("貂蝉")
zgl = Mage("诸葛亮", "羽扇")
zgl.show_me()
zgl.attack("黄月英")
