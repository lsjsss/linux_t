# 云计算网络周测

案例二
二，ISCSI服务 虚拟磁盘技术
svr7服务端添加一块10G的硬盘
操作
fdisk /dev/sdb
n +5G

yum -y install targetcli
targetcli
/> backstores/block create dev=/dev/sdb1 name=iscsi store
/> iscsi/ create iqn.2019-09.cn.example:server
/> iscsi/ipn.2019-09.cn.example:server/tpg/luns create /backstores/block /iscsi store
/> iscsi/iqn.2019-09.cn.example:server/tpg/acls  create iqn.2019-09.cn.example:desktop
/> exit
systemctl restart target-service
systemctl enable tsrget-service
pc207客户端操作
yum -y install iscsi-initiator-utils
vim /etc/iscsi/initiatorname.iscsi
                =iqn.2019-09.cn.example:desktop
systemctl restart iscsid
man iscsiadm
/example
复制
粘贴
systemctl restart iscsi
systemctl enable iscsi
lsblk
fdisk /dev/sdb 
n +()
lsblk
mkdir /data
mkfs.xfs  /dev/sdb1
mount /dev/sdb1 /data  
df -h
vim /etc/fstab
/dev/sdb1  xfs  /data  defaults  0  0 
mount -a

三，构建web服务 
案例三
svr7
yum -y install httpd
vim  /etc/httpd/conf/httpd.conf
    "/war/www/webroot"                       # 改变网页存放路径
mkdir /var/www/webroot
echo "卖火柴的小女孩" > /var/www/webroot/index.html
systemctl restart httpd
 pc207
curl 192.168.4.7

案例四 虚拟web主机

Svr7
vim  /etc/httpd/conf.d/nsd01.conf
<virtualhost *：80>
     ServerName   server.example.com
DocumentRoot    /var/www/server
</virtualhost>
<virtualhost *：80>
     ServerName   desktopr.example.com
DocumentRoot    /var/www/desktop
</virtualhost>
<virtualhost *：80>
     ServerName   webapp.example.com
DocumentRoot    /var/www/webapp
</virtualhost>
Mkdir   /var/www/server   /var/www/desktop   /var/www/webapp
Echo ““  >   /var/www/server/index.html
Echo ““  >   /var/www/desktop/index.html
Echo ““  >   /var/www/webapp/index.html

Systemctl  restart  httpd

Pc207 
Vim /etc/hosts
192.168.4.7   server.example.com desktopr.example.com webapp.example.com
Curl  webapp.example.com

案例五 普通NFS共享
Svr7
Yum -y install nfs-utils
 Mkdir  /public
,mkdir /protected
Vim /etc/exports
/public 192.168.4.0/24(ro)
/protected  (rw)
Systemctl restart nfs-server
Systemctl enable nfs-server
Pc207
Yum -y install nfs-utils
Showmount -e 192.168.4.7
Mkdir /nsd
Mount 192.168.4.7:/public /nsd
Df -h
Ls /nsd
Vim /etc/fstab
192.168.4.7:/public /nsd  nsd  defaults,_netdev  0  0
Mount -a
Yum  -y install autofs
Systemctl restart autofs
Vim /etc/auto.misc
Autonfs  -fstype=nfsmount    192.168.4.7:/protected
Systemctl restart autofs
Ls /misc
Cd  /misc/autonfs  
Df -ah

案例六 构建DNS服务
Svr7
Yum -y install bind bind-chroot
Vim /etc/named.conf
Zone “sina.com” IN {
		Type master;
		File “sina.com.zone”;
}；
Cp -p /var/named/named.localhost   /var/named/sina.com.zone
Vim /var/named/sina.com.zone
Sina.com.  NS  svr7
Svr7   A  192.168.4.7
www A 10.11.12.13
systemctl restart named
pc207
yum -y install bind-utils
nslookup  www.sina.com 192.168.4.7


案例七 构建多区域DNS服务
Vim /etc/named.conf
Zone “sina.com” IN {
		Type master;
		File “sina.com.zone”;
}；
Zone “qq.com” IN {
		Type master;
		File “qq.com.zone”;
}；
Zone “baidu.com” IN {
		Type master;
		File “baidu.com.zone”;
}；

Cp -p /var/named/named.localhost   /var/named/qq.com.zone
Vim /var/named/qq.com.zone
qq.com.  NS  svr7
Svr7   A  192.168.4.7
www A 192.168.4.100

Cp -p /var/named/qq.com.zone   /var/named/baidu.com.zone
Vim   /var/named/baidu.com.zone
baidu.com.  NS  svr7
Svr7   A  192.168.4.7
www A 192.168.10.100
systemctl restart named

pc207
yum -y install bind-utils
nslookup  www.qq.com 192.168.4.7
nslookup  www.baidu.com 192.168.4.7

案例八 构建邮件服务
Svr7
Vim /etc/named.conf
Zone “example.com” IN {
	TYPE master;
	

};
Cp -p /var/named/named.localhost   /var/named/example.com.zone
Vim /var/named/example.com.zone
Example.com.  NS svr7
Example.com.  MX 10  mail
Svr7   A  192.168.4.7
Mail     A 192.168.4.207
Systemctl restart named
Pc207
Echo nameserver 192.168.4.7 > /etc/resolv.conf
Host -t MX example.com
Host mail.example.com
Rpm -q podtfix
 Vim /etc/postfix/main.cf
99   myorigin=example.com
116  inet_interfaces=all
164   =example.com
Systemctl restart postfix
Useradd natasha
Useradd tom 
Echo ““ | mail -s  “test01” -r natasha tom
Mail -u tom


案例9：构建DNS分离解析
1、在虚拟机svr7上构建DNS分离解析，要求如下：
   1）客户端192.168.4.207----> www.qq.com----> 192.168.4.110
2) 客户端为其他地址---→ www.qq.com----> 10.20.30.40 
3）客户端为192.168.4.10 ---→ www.baidu.com-----> 192.168.10.100
4）客户端为其他地址---→ www.qq.com-----> 5.6.7.8
   2、在虚拟机pc207和虚拟机A进行测试验证

