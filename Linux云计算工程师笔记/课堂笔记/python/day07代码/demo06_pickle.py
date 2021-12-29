# pickle
# pickle.dump(obj, fobj)
# pickle.load(file)
import pickle
fwb = open("/tmp/a.data", mode="wb")
user = {"name": "nfx", "age": 18}
pickle.dump(user, fwb)  # 将字典写入文件
fwb.close()
frb = open("/tmp/a.data", mode="rb")
adict = pickle.load(frb)  # 将字典数据读取出来
for key in adict:
    print(key, adict[key])
