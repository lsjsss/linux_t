# break: 终止(退出)当前循环
# 打印1~10
counter = 1
while counter <= 100:
    if counter == 11:
        break
        print("ok~")  # 永远不会被执刑
    print(counter)
    counter += 1  # 10 -> 11
print("end while")


# continue: 跳过当次循环
print("*" * 30)
counter = 0
while counter < 9: # 1234 6789
    counter += 1
    if counter == 5:
        continue
        print("ok")  # 永远不会被执刑
    print(counter)






