# 练习 4：  in
# 将 192.168.1 网段的 ip 添加到新的列表 dest 中
# （要求使用 continue 关键字）
index = -1  # 表示列表的索引
dest = []  # 创建了一个空列表
ips = [
    "192.168.1.100", "192.168.1.101",
    "192.168.2.100", "192.168.3.100",
    "192.168.1.200"]
while index < len(ips)-1:
    index += 1
    if "192.168.1." not in ips[index]:
        continue
    dest.append(ips[index])
print(dest)

