import random

list01=[random.randint(1, 100) for i in range(10)]

list02 = []
for item in list01:
    if item % 2 == 0:
        list02.append(item)

res = filter(lambda a: True if a % 2 == 0 else False, list01)
print(res)
print(list(res))




