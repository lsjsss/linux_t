# shutil
import shutil
# 1. shutil.copyfileobj(fr, fw)  fr, fw: 文件操作对象
# fr = open("/etc/passwd", mode="r")
# fw = open("/tmp/passwd_copy", mode="w")
# shutil.copyfileobj(fr, fw)
# fr.close()
# fw.close()
# 2. shutil.copyfile(src, dest)  src,dest: 路径
#    只复制文件的内容
# shutil.copyfile("/etc/passwd", "/tmp/my_pass")
# 3. shutil.copy(src, dest)  src,dest: 路径
#    复制内容和权限  休息到 16:20
# shutil.copy("/usr/bin/ls", "/tmp/my_ls")
# 移动文件 shutil.move(src, dest)
# shutil.move("/tmp/my_pass", "/tmp/my_pass2")
# 目录操作
# 1. 复制目录  cp -r
# shutil.copytree("/etc/security", "/tmp/security")
# 2. 删除目录
# shutil.rmtree("/tmp/security")
# 权限管理
# 1. 复制权限
# shutil.copymode("/usr/bin/ls", "/tmp/my_pass2")
# 2. 只复制文件的元数据信息
# shutil.copystat("/usr/bin/ls", "/tmp/my_pass2")
# 2.1 复制文件内容和文件的元数据信息
# shutil.copy2("/usr/bin/ls", "/tmp/my_pass2")
# 3. 修改文件的属主属组信息   useradd nfx
shutil.chown("/tmp/my_pass2",user="nfx",group="nfx")






