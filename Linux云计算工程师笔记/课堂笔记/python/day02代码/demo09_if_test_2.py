### 练习 3：编写石头剪刀布小游戏
# 1. 计算机随机出拳
# 2. 玩家自己决定如何出拳
# 任务：判断谁赢谁输
import random  # 借别人的工具
all_choices = ["st", "jd", "bu"]
# 定义玩家获胜情况的列表
win_list=[["st", "jd"],["jd", "bu"],["bu", "st"]]
computer = random.choice(all_choices)# 1. 计算机随机出拳
print("computer:", computer)
player = input("请出拳(st/jd/bu): ")# 2. 玩家自己决定如何出拳
if player == computer:
    print("平局")
elif [player, computer] in win_list:
    print("player win~")
else:
    print("computer win~")

