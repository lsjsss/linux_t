# 终极练习：备份程序
# **需求**
# - 需要支持完全和增量备份
# - 周一执行完全备份
# - 其他时间执行增量备份
# - 备份文件需要打包为 tar 文件并使用 gzip 格式压缩
import time,os,tarfile,hashlib,pickle
def check_md5(fname):
    m = hashlib.md5()
    with open(fname, mode="rb") as frb:
        while True:
            data = frb.read(4096)
            if data == b"":  # 和字节串比较
                break
            m.update(data)
    return m.hexdigest()  # 返回为文件的MD5值
# src = "/tmp/demo/security"
# /tmp/demo/backup/security_full_20211026.tar.gz

def full_backup(src, dst, md5file):
    # security_full_20211026.tar.gz
    fname = "%s_full_%s.tar.gz"%\
            (os.path.basename(src),
             time.strftime("%Y%m%d"))
    fname = os.path.join(dst, fname)
    # 文件打包
    tar = tarfile.open(fname, "w:gz")
    tar.add(src)
    tar.close()
    md5dict = {}  # 记录指定目录下所有文件的md5值
    for path, folders, files in os.walk(src):
        for file in files:
            # 文件的绝对路径
            key = os.path.join(path, file)
            print(key)
            md5dict[key] = check_md5(key)
    with open(md5file, mode="wb") as fwb:
        pickle.dump(md5dict, fwb)

def incr_backup(src, dst, md5file):
    # security_incr_20211026.tar.gz
    fname = "%s_incr_%s.tar.gz" % \
            (os.path.basename(src),
             time.strftime("%Y%m%d"))
    fname = os.path.join(dst, fname)
    md5dict = {}  # 当天最新
    # 找那些文件的md5值发生了变化
    for path, folders, files in os.walk(src):
        for file in files:
            key = os.path.join(path, file)
            md5dict[key] = check_md5(key)
    # 读取前一天md5file
    with open(md5file, mode="rb") as frb:
        old_md5 = pickle.load(frb)
    tar = tarfile.open(fname, "w:gz")
    for key in md5dict:  # key: 文件的路径
        if old_md5.get(key) != md5dict[key]:
            tar.add(key)
    tar.close()  # tar包中只存放了变化了的文件
    # 把今天文件的MD5 dump一次
    with open(md5file, mode="wb") as fwb:
        pickle.dump(md5dict, fwb)


if __name__ == '__main__':
    src = "/tmp/demo/security"
    dst = "/tmp/demo/backup"
    md5file = "/tmp/demo/md5.data"
    # %a: 表示周几
    if time.strftime("%a") == "Wed":  # 表示周三
        full_backup(src, dst, md5file)
    else:
        incr_backup(src, dst, md5file)
