# 需求：谁先赢到两局，游戏结束
import random  # 借别人的工具
all_choices = ["st", "jd", "bu"]
# 定义玩家获胜情况的列表
win_list=[["st", "jd"],["jd", "bu"],["bu", "st"]]
c_win = 0  # 计算机获胜的次数
p_win = 0  # 玩家获胜的次数
while c_win < 2 and p_win < 2:
    computer = random.choice(all_choices)# 1. 计算机随机出拳
    print("computer:", computer)
    player = input("请出拳(st/jd/bu): ")# 2. 玩家自己决定如何出拳
    if player == computer:
        print("平局")
    elif [player, computer] in win_list:
        print("player win~")
        p_win += 1  # 玩家获胜次数+1
    else:
        print("computer win~")
        c_win += 1  # 计算机获胜次数+1
