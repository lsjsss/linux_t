# 生成器
# 生成器函数：yield就是一个人生成器
def test_gen(list_temp):
    for item in list_temp:
        return item  # 函数碰到return就终止执行
def test_gen1(list_temp):
    for item in list_temp:
        yield item  # 函数碰到yield就暂停执行
res = test_gen1([1, 2, 3])  # res: 生成器
# 生成器也是迭代器 可以通过next或者for获取元素
print(next(res))
print(next(res))
print(next(res))

def test_gen3():
    a = 1
    yield a
    c = 2
    yield c
gen = test_gen3()  # <genxxxx    0x32131212>
a = next(gen)
print(a)
vale = next(gen)
print(vale)

