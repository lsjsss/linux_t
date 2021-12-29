# 形参和实参
def washing_machine(something):
    print("打水")
    print("加洗衣粉！！！")
    print("洗" + something)
    print("甩干")
# 洗什么东西是由函数的调用者去决定的
washing_machine("衣服")  # something = "衣服"
washing_machine("床单")  # something = "床单"
washing_machine("被罩")  # something = "被罩"
