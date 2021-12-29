## 练习 2：测试字符串是否为合法标识符
# 需求  9:45
# 1.编写用于测试字符串的函数(是合法标识符返回True否则False)
# 2.函数用于确定字符串是否为合法标识符
#   - 第一个字符必须是字母或下划线 _
#   - 剩下的字符可以是字母和数字或下划线
# 3.字符串不能为关键字
#   ('xxx' in keyword.kwlist 为False表示不是关键字)
from string import ascii_letters, digits
import keyword
print()
def check_bsf(bsf):  # 10:15上课
    if bsf in keyword.kwlist:  # 判断是不是关键字
        return False
    if bsf[0] not in ascii_letters + "_":
        return False  # 判断首字符
    for item in bsf[1:]:  # 判断剩余字符
        if item not in digits+ascii_letters+"_":
            return False
    return True
if __name__ == '__main__':
    print(check_bsf("for123"))




