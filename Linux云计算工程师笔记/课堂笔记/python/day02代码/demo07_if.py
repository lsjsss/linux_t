# 多分支
# 需求
# 1. 如果成绩大于60分，输出“及格”
# 2. 如果成绩大于70分，输出“良”
# 3. 如果成绩大于80分，输出“好”
# 4. 如果成绩大于90分，输出“优秀”
# 5. 否则输出“你要努力了”
score = int(input("score: "))
if score >= 90:
    print("优秀")
elif score >= 80:
    print("好")
elif score >= 70:
    print("良")
elif score >= 60:
    print("及格")
else:
    print("你要努力了")






