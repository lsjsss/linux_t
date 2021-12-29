alist = [1, 2, 3]
blist = alist[:]  # 切片赋值
# blist = alist  # 列表直接赋值
print(id(alist), id(blist))
print(alist, blist)
blist.append(4)
print(blist)  # [1, 2, 3, 4]
# alist 切片赋值[1, 2, 3]   直接赋值[1, 2, 3, 4]
print(alist)





# print(id(alist), id(blist))
# print(alist, blist)
# blist.append(4)
# print(blist)
# print(alist)  # [1, 2, 3]   [1, 2, 3, 4]