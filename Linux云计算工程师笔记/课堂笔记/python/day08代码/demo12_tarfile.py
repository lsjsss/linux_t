# tarfile" 文件的打包与解包
import tarfile
# # 1. 数据打包
# tar = tarfile.open("/tmp/demo.tar.gz", "w:gz")
# # add 添加需要压缩的文件
# tar.add("/etc/passwd")
# tar.add("/etc/hosts")
# tar.close()  # 关闭文件
# 2. 数据解包
tar1 = tarfile.open("/tmp/demo.tar.gz")
tar1.extractall(path="/var/tmp")  # 解压的路径
tar1.close()
# ls /var/tmp/etc/hosts
# ls /var/tmp/etc/passwd

