### 练习 1：简单的加减法数学游戏
# **需求**
# - 随机生成两个100以内的数字 random.randint(1,100)
# - 随机选择加法或是减法 random.choice(["+", "-"])
# - 总是使用大的数字减去小的数字 list.sort()
# - 如果用户答错三次，程序给出正确答案 while else
import random
def exam():
    # 1. 随机生成两个100以内的数字
    nums=[random.randint(1,100) for i in range(2)]
    # 2. 随机选择加法或是减法
    op = random.choice(["+", "-"])
    nums.sort()  # 3. 列表排序
    if op == "+":  # res: 正确答案
        res = nums[1] + nums[0]
    else:
        res = nums[1] - nums[0]
    # 4.用户算结果
    counter = 0  # 记录用户计算错题目的次数
    while counter < 3:  # 0 1 2
        answer = int(input("%s %s %s = ???, answer:"%(nums[1], op, nums[0])))
        if answer == res:
            print("Very Good~")
            break
        else:
            print("Wrong answer~")
            counter += 1  # 算错则counter+1
    else:
        print("res:", res)
if __name__ == '__main__':  # 10:05上课
    exam()








