# 列表的操作
#               添加元素
tedu = ["nn", "kk", "zz", "dd", "nn"]
# 1.append: 尾添加
# 2.insert(插入的索引位置，插入的元素)
# tedu.insert(0, "wzl")
# 3.extend: 扩展元素
# tedu.extend(['aa', 'bb', 'cc'])
# ['nn', 'kk', 'zz', 'dd', 'aa', 'bb', 'cc']
#               删除元素
# 1.remove(元素的值)：没有返回值
# tedu.remove("nn")
# 2.pop(索引):会将删除的元素返回,如果不指定索引弹出尾部元素
# 3. del tedu[0]
# 4. clear(): 清空元素,剩下空列表
# tedu.clear()
#             修改元素
# tedu[0] = "bb"
#             查询元素
# 通过索引
# 通过切片
# 列表的遍历 for
# for name in tedu:
#     print(name, end=", ")
#             其他
# 1. len: 求列表的长度 len(tedu)
# 2. reverse(): 列表反转, 该函数没有返回值
# tedu.reverse()
# 3. sort(): 排序    sort(reverse=True): 倒序
#    没有返回值，在原列表基础上进行排序
# list01 = [2, 1, 0, 10, 7]
# list01.sort(reverse=True)
# 4. count(元素) 求列表中某个元素出现的次数
# print(tedu.count("dd"))
# 5. list(其他类型数据) 将其他类型数据转换成列表类型
res = list("hello world")  # 必须是可迭代对象
print(res)
