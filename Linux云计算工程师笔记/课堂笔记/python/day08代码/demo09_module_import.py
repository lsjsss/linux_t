# 模块导入
# 1. shell: export PYTHONPATH=/tmp
#    shell: python3 xxx.py
#    使/tmp成为模块的搜索路径(终端测试)
# 2. sys.path:
#    将/tmp添加到sys.path的列表中，然后再去导入指定的模块
import sys
sys.path.append("/tmp")
import my_module
res = my_module.my_func(1, 2)
print(res)  # 3
