nmcli connection modify ens33 ipv4.method manual ipv4.addresses 192.168.4.10/24 connection.autoconnect yes
nmcli connection up ens33
mount /dev/cdrom /mnt

echo "[development]
name=Centos7.5
baseurl=file:///mnt
enabled=1
gpgcheck=0" > /etc/yum.repos.d/mnt.repo 

rm -rf /etc/yum.repos.d/C*
yum clean all 
yum repolist

setenforce 0
systemctl stop firewalld.service 
yum -y install httpd
yum -y install dhcp
rpm -q dhcp
systemctl restart dhcpd
ss -anptu | grep 67

echo "subnet 192.168.4.0 netmask 255.255.255.0 {
  range 192.168.4.100 192.168.4.200;
  option domain-name-servers 192.168.4.10;
  option routers 192.168.4.254;
  default-lease-time 600;
  max-lease-time 7200;
  next-server 192.168.4.10;
  filename \"pxelinux.0\";
}" > /etc/dhcp/dhcpd.conf 

systemctl restart dhcpd
yum -y install tftp-server.x86_64 
systemctl restart tftp
ss -anptu | head -69
yum provides */pxelinux.0
yum -y install syslinux
rpm -ql syslinux | grep pxelinux.0
cp /usr/share/syslinux/pxelinux.0  /var/lib/tftpboot/
mkdir /var/lib/tftpboot/pxelinux.cfg
cp /mnt/isolinux/isolinux.cfg /var/lib/tftpboot/pxelinux.cfg/default
cp /mnt/isolinux/vesamenu.c32 /mnt/isolinux/splash.png /mnt/isolinux/initrd.img /mnt/isolinux/vmlinuz /var/lib/tftpboot/

sed -i '61d' /var/lib/tftpboot/pxelinux.cfg/default 
sed -i '61d' /var/lib/tftpboot/pxelinux.cfg/default 
sed -i '61d' /var/lib/tftpboot/pxelinux.cfg/default
sed -i '61d' /var/lib/tftpboot/pxelinux.cfg/default

sed -i "61a label linux" /var/lib/tftpboot/pxelinux.cfg/default 
sed -i "62a   menu default" /var/lib/tftpboot/pxelinux.cfg/default 
sed -i "63a   kernel vmlinuz" /var/lib/tftpboot/pxelinux.cfg/default 
sed -i "64a   append initrd=initrd.img ks=http://192.168.4.10/ks.cfg" /var/lib/tftpboot/pxelinux.cfg/default 

systemctl restart dhcpd
systemctl restart tftp
setenforce 0
yum -y install httpd
systemctl restart httpd
mkdir /var/www/html/centos
mount /dev/cdrom /var/www/html/centos/
yum -y install system-config-kickstart.noarch 
yum -y install system-config-kickstart

echo "install
keyboard 'us'
rootpw --iscrypted $1$6/ldzaKw$dsdWMg2fX1l40RTZ2BoN50
url --url=\"http://192.168.4.10/centos\"
lang en_US
auth  --useshadow  --passalgo=sha512
graphical
firstboot --disable
selinux --disabled
firewall --disabled
network  --bootproto=dhcp --device=eth0
reboot
timezone Asia/Shanghai
bootloader --location=mbr
zerombr
clearpart --all --initlabel
part / --fstype=\"xfs\" --grow --size=1

%packages
@base

%end" > /var/www/html/ks.cfg

systemctl restart httpd.service 
systemctl restart dhcpd.service 
systemctl restart tftp.service

