### 练习 3：比较文件内容
# 需求
# - 有两个文件：/tmp/a.log 和 /tmp/b.log
# - 两个文件中有大量重复内容
# - 取出只有在 b.log 中存在的行
fname1 = "/tmp/a.log"  # 15:05 上课
fname2 = "/tmp/b.log"
fr1 = open(fname1, mode="r")
fr2 = open(fname2, mode="r")
aset = set(fr1.readlines())
bset = set(fr2.readlines())
res = bset - aset  # 取出只有在 b.log 中存在的行
print(res)
fr1.close()
fr2.close()
