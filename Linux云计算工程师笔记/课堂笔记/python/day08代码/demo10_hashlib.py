# hashlib: 计算文件的hash值
import hashlib
# 一次性计算
m = hashlib.md5(b"123456")
print(m.hexdigest())  # 以16进制显示md5值
# 分批计算
m1 = hashlib.md5()
m1.update(b"12")
m1.update(b"34")
m1.update(b"56")
print(m1.hexdigest())

