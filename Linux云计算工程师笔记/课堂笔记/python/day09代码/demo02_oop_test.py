### 练习 3：编写游戏人物
# **需求：**
# - 创建游戏角色类 Role
# - 游戏人物角色拥有名字name、武器weapon等属性
# - 游戏人物具有攻击的方法(attack)
#               我是？，我用？武器攻击
# - 武器通过武器类实现  属性: wname strength
class Weapon:
    def __init__(self, wname, strength):
        self.wname = wname
        self.strength = strength
class Role:
    def __init__(self, name, weapon):  # 初始化/构造函数
        self.name = name
        self.weapon = weapon
    def attack(self, target):
        print("我是%s，我用%s武器攻击%s, %s" %
              (self.name, self.weapon.wname, target, self.weapon.strength))
w1 = Weapon("丈八蛇矛", 100)  # 创建Weapon类对象
r1 = Role("张飞", w1)
r1.attack("吕布")

# r1 = Role("张飞", "丈八蛇矛")
# print(r1.name, r1.weapon)








