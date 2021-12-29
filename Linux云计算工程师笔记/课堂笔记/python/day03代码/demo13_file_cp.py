# 模拟 cp 操作
# 1. 创建 cp.py 文件
# 2. 将 /usr/bin/ls   "拷贝" 到 /tmp/list
# 3. 不要修改原始文件
# cp /usr/bin/ls /tmp/list
src_fname = "/usr/bin/ls"  # 要复制的文件
dst_fname = "/tmp/list"  # 复制写入的位置
frb = open(src_fname, mode="rb")
fwb = open(dst_fname, mode="wb")
while True:
    data = frb.read(4096)  # 4k
    if not data:  # 如果读取到的数据为空，终止循环
        break
    fwb.write(data)  # 读取到的数据写入
frb.close()
fwb.close()

