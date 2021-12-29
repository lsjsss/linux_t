# else
# 循环没碰到break正常结束,才会执行else的逻辑
counter = 1
while counter <= 10:
    # if counter == 5:
    #     break  # 1, 2, 3, 4
    print(counter)
    counter += 1
else:
    print("循环没碰到break正常结束,才会执行else的逻辑")