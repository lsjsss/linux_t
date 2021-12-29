# Python异常处理
# res = 10 / 0  # ZeroDivisionError
# print("a" + 5)  # TypeError
# print(["a", "b", "c"][10])  # IndexError
# int("abc")  # ValueError
# ctrl+c: KeyboardInterrupt
# ctrl+d: EOFError
# 异常处理  try-except
# 关键字
#   else:如果try中代码没有出现异常，则执行else中的逻辑
#   finally:不管代码有没有异常，都会执行finally中的内容
try:
    # 将可能出现问题的代码放到try包裹
    n1 = int(input("number1: "))
    n2 = int(input("number2: "))
    print(n2 / n1)
except ValueError as e:  # 如果出现了ValueError，planB
    print("输入的内容非法", e)
except (KeyboardInterrupt, EOFError):
    print("ByeBye~")
except Exception as result: # 捕获未知的异常
    print(result)  # 打印报错信息
else:  # 11:23  上课
    print("没有异常")
finally:
    # try:     fr = open(fname, mode="r")
    # finally: fr.close()
    print("关闭资源的代码")
