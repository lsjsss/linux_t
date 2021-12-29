### 练习 3：编写石头剪刀布小游戏
# 1. 计算机随机出拳
# 2. 玩家自己决定如何出拳
# 任务：判断谁赢谁输
import random  # 借别人的工具
all_choices = ["st", "jd", "bu"]
# 1. 计算机随机出拳
computer = random.choice(all_choices)
print("computer:", computer)
# 2. 玩家自己决定如何出拳
player = input("请出拳(st/jd/bu): ")
# 以玩家为基准
if player == "st":
    if computer == "st":
        print("平局")
    elif computer == "jd":
        print("player win~")
    else:
        print("computer win~")
elif player == "jd":
    if computer == "st":
        print("computer win~")
    elif computer == "jd":
        print("平局")
    else:
        print("player win~")
else:  # player: bu
    if computer == "st":
        print("player win~")
    elif computer == "jd":
        print("computer win~")
    else:
        print("平局")









