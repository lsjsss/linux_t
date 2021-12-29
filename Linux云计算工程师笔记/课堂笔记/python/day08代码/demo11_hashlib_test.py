### 练习 5：计算文件 md5 值
# **需求**
# - 编写用于计算文件 md5 值的脚本
# - 文件名通过位置参数获得  def check_md5(fname)
# - 打印出文件 md5 值
import hashlib
def check_md5(fname):
    m = hashlib.md5()
    with open(fname, mode="rb") as frb:
        while True:
            data = frb.read(4096)
            if data == b"":  # 和字节串比较
                break
            m.update(data)
    return m.hexdigest()  # 返回为文件的MD5值
if __name__ == '__main__':
    print(check_md5("/etc/passwd"))
    # d8599ff57b4e0d14fa5abb5269a71b71
    # md5sum /etc/passwd
    # d8599ff57b4e0d14fa5abb5269a71b71
