# os操作系统
import os
# os.path.abspath(): 生成绝对路径
print(os.path.abspath("abc"))
# os.path.join():  /tmp/abc/def
print(os.path.join("/tmp/abc", "def"))
# os.path.basename()    def
print(os.path.basename("/tmp/abc/def"))
# os.path.dirname()
print(os.path.dirname("/tmp/abc/def"))
# os.path.split()
print(os.path.split("/tmp/abc/def"))
# os.path.isxxx
print(os.path.isabs("/a/b"))
print(os.path.isdir("/etc/passwd"))  # False
print(os.path.isfile("/etc/passwd"))  # True
print(os.path.islink("/etc/passwd"))  # False
print(os.path.ismount("/etc/passwd"))  # False
# zui qiang
print(os.path.exists("/etc/passwd123"))
