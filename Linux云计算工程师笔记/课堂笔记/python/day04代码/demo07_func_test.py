def copy(src_fname, dst_fname):
    frb = open(src_fname, mode="rb")
    fwb = open(dst_fname, mode="wb")
    while True:
        data = frb.read(4096)  # 4k
        if not data:  # 如果读取到的数据为空，终止循环
            break
        fwb.write(data)  # 读取到的数据写入
    frb.close()
    fwb.close()
welcome = "Hello"  # 属性
# __name__: python解释器提供的变量，直接使用
# 如果在本模块执行，__name__: __main__
# 如果是被导入的情况，__name__:模块名(demo07_func_test)
if __name__ == "__main__":
    print(__name__)
    copy("/etc/hosts", "/tmp/hosts.bak")
    print("yes")
    print("我自动开机，不用你管")
