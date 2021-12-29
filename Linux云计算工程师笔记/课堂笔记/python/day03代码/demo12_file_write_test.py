# 练习:
# 将下列内容写到 ./a.py 中之后运行该Python文件
fw = open("./a.py", mode="w")
fw.write('num01 = int(input("num01: "))\n')
fw.write('num02 = int(input("num02: "))\n')
fw.write('res = num01 + num02\n')
fw.write("print('res: ' + str(res))\n")
fw.close()
#   num01 = int(input("num01: "))
#   num02 = int(input("num02: "))
#   res = num01 + num02
#   print('res: ' + str(res))