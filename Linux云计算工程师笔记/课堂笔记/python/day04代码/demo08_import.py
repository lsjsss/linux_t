# 导入自己写的模块
# 导入模块
# 相当于把导入的模块中的代码
# 从开头执行到结尾
# /etc/passwd /tmp/pa
# 模块导入多次，只会被加载一次
# import demo07_func_test
# demo07_func_test.copy("/etc/passwd", "/tmp/pa")
# print(demo07_func_test.welcome)
import randpass
passwd = randpass.randpass()
print("my passwd:", passwd)

