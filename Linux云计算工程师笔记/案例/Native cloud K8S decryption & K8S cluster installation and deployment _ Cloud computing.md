@[TOC]( Native cloud K8S decryption & K8S cluster installation and deployment & K8S network plug-in | Cloud computing )

---

# 1. 准备虚拟机环境

## 1.1 问题

本案例要求准备虚拟机环境，具体要求如下：

1. 在跳板机配置YUM源服务器
2. 准备虚拟机master实验环境
3. 最低配置：2cpu，2G内存
4. 卸载防火墙 firewalld-*
5. 禁用 selinux 和 swap
6. 配置yum仓库，安装kubeadm、kubelet、kubectl、docker-ce
7. 配置docker私有镜像仓库和cgroup驱动（daemon.json）
8. 配置内核参数（/etc/sysctl.d/k8s.conf）

## 1.2 方案

完成后续课程的学习需要提前准备实验用的虚拟机，实验虚拟机列表如表-1所示。

所有主机的主机名和IP必须与列表相同!!!

否则后续所有试验都无法顺利完成！！！

表-1

![img](https://img-blog.csdnimg.cn/img_convert/23e1f23bedd7c95516826b2b93f45dd4.png)

## 1.3 步骤

实现此案例需要按照如下步骤进行。

步骤一：在跳板机配置YUM源服务器（在跳板机主机操作）

Kubernetes相关软件已经提前共享到云盘，各位同学需要提前下载，并传到跳板机主机。云盘资料在第四阶段kubernetes/v1.17.6/k8s-install/目录下。

1）将所有软件资料放到跳板机的YUM共享目录。

```shell
[root@localhost ~]# rsync -avXSH --delete \
kubernetes/v1.17.6/k8s-install /var/ftp/localrepo/
```

2)更新YUM共享服务器数据

```shell
[root@server ~]# cd /var/ftp/localrepo
[root@server localrepo]# createrepo --update .
```

步骤二：安装管理节点所需软件包（在master主机操作）

1）设置yum源

```shell
[root@master ~]# vim /etc/yum.repos.d/local.repo 
[local_repo]
name=CentOS-$releasever – Localrepo
baseurl=ftp://192.168.1.252/localrepo
enabled=1
gpgcheck=0
[root@master ~]# yum makecache
```

2）安装软件

```shell
[root@master ~]# yum install -y kubeadm kubelet kubectl docker-ce
```

3）修改docker配置，指定使用私有镜像仓库

私有镜像仓库已经在前面课程搭建完成（在192.168.1.100服务器上）！！！

```shell
[root@master ~]# vim /etc/docker/daemon.json 
{
    "exec-opts": ["native.cgroupdriver=systemd"],
    "registry-mirrors": ["https://hub-mirror.c.163.com"],
    "insecure-registries":["192.168.1.100:5000", "registry:5000"]
}
```

4）修改内核参数

```shell
[root@master ~]# vim /etc/sysctl.d/k8s.conf      #没有该文件，需要新建文件
net.bridge.bridge-nf-call-ip6tables = 1          # 开启桥设备内核监控（ipv6）
net.bridge.bridge-nf-call-iptables = 1               # 开启桥设备内核监控（ipv4）
net.ipv4.ip_forward = 1                             # 开启路由转发
[root@master ~]# modprobe br_netfilter             #加载内核模块
[root@master ~]# sysctl --system                    # 加载上面的k8s.conf配置文件
* Applying /etc/sysctl.d/k8s.conf ...
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
net.ipv4.ip_forward = 1
... ...
```

5）了解kubeadm命令

```shell
kubeadm 命令
config: 配置管理命令
help:   查看帮助
init:   初始命令
join:   node加入集群的命令
reset:  还原状态命令 
token:  token凭证管理命令
version:查看版本
```



# 2. 配置私有仓库

## 2.1 问题

本案例要求上传镜像到私有仓库（192.168.1.100:5000），具体需要上传的镜像列表如下：

1. 192.168.1.100:5000/kube-apiserver:v1.17.6
2. 192.168.1.100:5000/kube-controller-manager:v1.17.6
3. 192.168.1.100:5000/kube-scheduler:v1.17.6
4. 192.168.1.100:5000/kube-proxy:v1.17.6
5. 192.168.1.100:5000/pause:3.1
6. 192.168.1.100:5000/etcd:3.4.3-0
7. 192.168.1.100:5000/coredns:1.6.5

## 2.2 步骤

实现此案例需要按照如下步骤进行。

**步骤一：列出部署kubernetes需要哪些镜像（在master主机操作）**

```shell
[root@master ~]# kubeadm config image list           #列出需要的镜像
k8s.gcr.io/kube-apiserver:v1.17.6
k8s.gcr.io/kube-controller-manager:v1.17.6
k8s.gcr.io/kube-scheduler:v1.17.6
k8s.gcr.io/kube-proxy:v1.17.6
k8s.gcr.io/pause:3.1
k8s.gcr.io/etcd:3.4.3-0
k8s.gcr.io/coredns:1.6.5
```

**步骤二：将所有需要的镜像导入私有仓库（在master或者node-0001主机操作）**

所有实验需要的镜像都已经提前共享在云盘，各位同学需要将所有镜像下载并传到master主机。镜像在云盘第四阶段kubernetes/v1.17.6/base-images目录下。

警告：所有镜像禁止修改名称和标签，必须保留原名称！！！

```shell
[root@master ~]# docker load -i kube-apiserver.tar.gz
#加载kube-apiserver镜像到本地
[root@master ~]# docker tag \
k8s.gcr.io/kube-apiserver:v1.17.6 192.168.1.100:5000/kube-apiserver:v1.17.6
#修改镜像标签（只修改服务器的IP，不要修改镜像名称和后面的版本）
[root@master ~]# docker push 192.168.1.100:5000/kube-apiserver:v1.17.6
#将镜像上传到192.168.1.100私有镜像仓库服务器
[root@master ~]# docker load -i pause.tar.gz
#加载pause镜像到本地
[root@master ~]# docker tag \
k8s.gcr.io/pause:3.1 192.168.1.100:5000/pause:3.1
#修改镜像标签（只修改服务器的IP，不要修改镜像名称和后面的版本）
[root@master ~]# docker push 192.168.1.100:5000/pause:3.1
#将镜像上传到192.168.1.100私有镜像仓库服务器
[root@master ~]# docker load -i kube-proxy.tar.gz
#加载kube-proxy镜像到本地
[root@master ~]# docker tag \
k8s.gcr.io/kube-proxy:v1.17.6 192.168.1.100:5000/kube-proxy:v1.17.6
#修改镜像标签（只修改服务器的IP，不要修改镜像名称和后面的版本）
[root@master ~]# docker push 192.168.1.100:5000/kube-proxy:v1.17.6
#将镜像上传到192.168.1.100私有镜像仓库服务器
[root@master ~]# docker load -i kube-controller-manager.tar.gz
#加载kube-controller-manager镜像到本地
[root@master ~]# docker tag \
k8s.gcr.io/kube-controller-manager:v1.17.6 192.168.1.100:5000/kube-controller-manager:v1.17.6
#修改镜像标签（只修改服务器的IP，不要修改镜像名称和后面的版本）
[root@master ~]# docker push 192.168.1.100:5000/kube-controller-manager:v1.17.6
#将镜像上传到192.168.1.100私有镜像仓库服务器
[root@master ~]# docker load -i kube-controller-manager.tar.gz
#加载kube-controller-manager镜像到本地
[root@master ~]# docker tag \
k8s.gcr.io/kube-controller-manager:v1.17.6 192.168.1.100:5000/kube-controller-manager:v1.17.6
#修改镜像标签（只修改服务器的IP，不要修改镜像名称和后面的版本）
[root@master ~]# docker push 192.168.1.100:5000/kube-controller-manager:v1.17.6
#将镜像上传到192.168.1.100私有镜像仓库服务器
[root@master ~]# docker load -i etcd.tar.gz
#加载etcd镜像到本地
[root@master ~]# docker tag \
k8s.gcr.io/etcd:3.4.3-0 192.168.1.100:5000/etcd:3.4.3-0
#修改镜像标签（只修改服务器的IP，不要修改镜像名称和后面的版本）
[root@master ~]# docker push 192.168.1.100:5000/etcd:3.4.3-0
#将镜像上传到192.168.1.100私有镜像仓库服务器
[root@master ~]# docker load -i coredns.tar.gz
#加载coredns镜像到本地
[root@master ~]# docker tag \
k8s.gcr.io/coredns:1.6.5 192.168.1.100:5000/coredns:1.6.5
#修改镜像标签（只修改服务器的IP，不要修改镜像名称和后面的版本）
[root@master ~]# docker push 192.168.1.100:5000/coredns:1.6.5
#将镜像上传到192.168.1.100私有镜像仓库服务器
```



# 3. 安装master

## 3.1 问题

本案例要求安装部署master，分别实现以下目标：

1. 设置tab键
2. 安装IPVS模式软件包 ipvsadm、ipset
3. 在master上部署kubernetes

## 3.2 步骤

实现此案例需要按照如下步骤进行。

**步骤一：安装部署master管理节点（在master主机操作操作）**

1）设置Tab补齐

kubectl、kubeadm支持自动补全功能，可以节省大量输入，自动补全脚本由 kubectl、kubeadm产生，仅需要在您的 shell 配置文件中调用即可。

```shell
[root@master ~]# kubectl completion bash >/etc/bash_completion.d/kubectl
[root@master ~]# kubeadm completion bash >/etc/bash_completion.d/kubeadm
[root@master ~]# exit
# 注意 ：配置完成以后需要退出，重新登录后才能生效
```

2）安装IPVS代理

```shell
[root@master ~]# yum install -y ipvsadm ipset
```

3）k8s系统初始化

```shell
[root@master ~]# kubeadm init --dry-run
... ...
根据提示信息排错若干
... ...
--------------------------------------------------------------------
[root@master ~]# kubeadm config print init-defaults >kubeadm-init.yaml
```

4）修改配置文件

修改好的配置文件已经共享在云盘，直接使用修改好的配置文件即可。

配置文件在第四阶段kubernetes/v1.17.6/config/kubeadm-init.yaml。

```shell
[root@master ~]# vim  kubeadm-init.yaml
06:    ttl: 24h0m0s                          # token 生命周期
12:    advertiseAddress: 192.168.1.21        # apiserver 的IP地址
32:    imageRepository: 192.168.1.100:5000    # 镜像仓库地址
34:    kubernetesVersion: v1.17.6        # 当前安装的 k8s 版本
36:    dnsDomain: cluster.local        # 默认域名地址
37:    podSubnet: 10.244.0.0/16        # 容器地址cidr，新添加
38:    serviceSubnet: 10.254.0.0/16        # 服务地址cidr
#文件最后手动添加如下4行
---                    
apiVersion: kubeproxy.config.k8s.io/v1alpha1
kind: KubeProxyConfiguration
mode: ipvs
```

5）安装master

```shell
[root@master ~]# kubeadm init --config=kubeadm-init.yaml | tee master-init.log
... ...
Your Kubernetes control-plane has initialized successfully!
To start using your cluster, you need to run the following as a regular user:
  mkdir -p $HOME/.kube
  sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
  sudo chown $(id -u):$(id -g) $HOME/.kube/config
... ...
[root@master ~]# mkdir -p /root/.kube
[root@master ~]# cp -i /etc/kubernetes/admin.conf /root/.kube/config
```

6）启动服务并验证

```shell
[root@master ~]# kubectl  get  componentstatuses
NAME                               STATUS          MESSAGE                 ERROR
controller-manager           Healthy                ok                  
scheduler                         Healthy           ok                  
etcd-0                         Healthy           {"health":"true"}   
[root@master ~]# kubectl version
Client Version: version.Info{Major:"1", Minor:"17", GitVersion:"v1.17.6", GitCommit:"d32... ...", GitTreeState:"clean", BuildDate:"2020-05-20T13:16:24Z", GoVersion:"go1.13.9", Compiler:"gc", Platform:"linux/amd64"}
Server Version: version.Info{Major:"1", Minor:"17", GitVersion:"v1.17.6", GitCommit:"d32... ...", GitTreeState:"clean", BuildDate:"2020-05-20T13:08:34Z", GoVersion:"go1.13.9", Compiler:"gc", Platform:"linux/amd64"}
```



# 4. 安装node节点并加入master

## 4.1 问题

本案例要求安装node节点并加入master，具体要求如下：

1. node主机最低配置：2cpu，2G内存
2. 初始化系统环境（步骤同 master）
3. 设置主机名/etc/hosts
4. master上创建 token
5. 安装 node 并加入集群

### 4.2 步骤

实现此案例需要按照如下步骤进行。

！！！提醒：本案例的所有操作都已经编写了ansible剧本，下面的所有操作步骤都可以通过ansible自动化完成。

各位同学在【跳板机】主机下载ansible配置以及对应的素材，执行剧本即可完成下面的所有操作！

Ansible素材在云盘共享第四阶段kubernetes/v1.17.6/node-install/目录下。

将整个目录下载拷贝到【跳板机】，然后修改剧本中的Token和对应的Hash值。

如果获取Token和对应的Hash值，可以参考下面的【步骤二】。

```shell
[root@localhost node-install]# vim node_install.yaml           # 执行前需要修改剧本
vars:
    master: '192.168.1.21:6443'
    token: ‘fm6kui.mp8rr3akn74a3nyn’       # 设置获取的 token
    token_hash: ‘sha256:f46dd7ee … …’        # 设置获取的 token hash
[root@localhost node-install]# ansible-playbook  node_install.yaml    # 执行剧本
```

**步骤一：初始化node节点（在node-0001主机操作）**

1）关闭防火墙和SELinux。

```shell
[root@node-0001 ~]# vim /etc/selinux/config
... ...
SELINUX=disabled
[root@node-0001 ~]# yum -y remove firewalld-*
... ...
[root@node-0001 ~]# reboot
... ...
[root@node-0001 ~]# sestatus 
SELinux status:                 disabled
```

2）配置YUM源

```shell
[root@node-0001 ~]# vim  /etc/yum.repos.d/local.repo
[local_repo]
name=CentOS-$releasever – Localrepo
baseurl=ftp://192.168.1.252/localrepo
enabled=1
gpgcheck=0
```

3）如果系统中有swap交换分区的话，则禁用该分区，可以在/etc/fstab中禁用。

4）安装软件

```shell
[root@node-0001 ~]# yum install -y kubeadm kubelet docker-ce
```

5）安装IPVS代理

```shell
[root@node-0001 ~]# yum install -y ipvsadm ipset
```

6）修改docker配置，指定使用私有镜像仓库

```shell
[root@node-0001 ~]# vim /etc/docker/daemon.json 
{
    "exec-opts": ["native.cgroupdriver=systemd"],
    "registry-mirrors": ["https://hub-mirror.c.163.com"],
    "insecure-registries":["192.168.1.100:5000", "registry:5000"]
}
```

7）修改内核参数

```shell
[root@node-0001 ~]# vim /etc/sysctl.d/k8s.conf      #没有该文件，需要新建文件
net.bridge.bridge-nf-call-ip6tables = 1          # 开启桥设备内核监控（ipv6）
net.bridge.bridge-nf-call-iptables = 1               # 开启桥设备内核监控（ipv4）
net.ipv4.ip_forward = 1                             # 开启路由转发
[root@node-0001 ~]# modprobe br_netfilter          #加载内核模块
[root@node-0001 ~]# sysctl --system                # 加载上面的k8s.conf配置文件
* Applying /etc/sysctl.d/k8s.conf ...
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
net.ipv4.ip_forward = 1
... ...
```

8）修改/etc/hosts

```shell
[root@node-0001 ~]# vim  /etc/hosts
::1        localhost    localhost.localdomain    localhost6    localhost6.localdomain6
127.0.0.1    localhost    localhost.localdomain    localhost4    localhost4.localdomain4
192.168.1.21    master
192.168.1.31    node-0001
192.168.1.32    node-0002
192.168.1.33    node-0003
192.168.1.34    node-0004
192.168.1.35    node-0005
```

**步骤二：将node加入K8s集群**

1）启动服务器（在node-0001主机操作）

```shell
[root@node-0001 ~]# systemctl enable --now docker kubelet
```

2）查看日志查找下面这一行安装指令的样例（在master主机操作）

```shell
kubeadm join 192.168.1.21:6443 --token <token> \
--discovery-token-ca-cert-hash   sha256: <token ca hash>
```

3）如何获取Token Hash值（在master主机操作）

```shell
[root@master ~]# openssl x509 -pubkey -in /etc/kubernetes/pki/ca.crt |  \
openssl rsa -pubin -outform der |openssl dgst -sha256 -hex
writing RSA key
(stdin)= f46dd7ee29faa3c096cad189b0f9aedf59421d8a881f7623a543065fa6b0088c
```

4）如何获取Token（在master主机操作）

```shell
[root@master ~]# kubeadm token list                # 列出 token
[root@master ~]# kubeadm token delete <token>        # 删除 token
[root@master ~]# kubeadm token create                # 创建 token
[root@master ~]# kubeadm token create --ttl=0 --print-join-command 
... ...
kubeadm join 192.168.1.21:6443 --token fm6kui.mp8rr3akn74a3nyn    
 --discovery-token-ca-cert-hash 
sha256:f46dd7ee29faa3c096cad189b0f9aedf59421d8a881f7623a543065fa6b0088c 
```

5）安装node节点（在node-0001主机操作）

使用刚刚生成的token指令完成node节点安装，下面的Toen和Hash值不能照抄。

```shell
[root@node-0001 ~]# kubeadm join 192.168.1.21:6443 --token \
fm6kui.mp8rr3akn74a3nyn --discovery-token-ca-cert-hash sha256:f46dd7ee29faa3c096cad189b0f9aedf59421d8a881f7623a543065fa6b0088c
```



# 5. 配置flannel网络，完成集群

## 5.1 问题

本案例要求配置flannel网络，完成集群，具体要求如下：

1. 导入镜像到私有仓库
2. 修改配置文件
3. 启动网络组件

## 5.2 步骤

实现此案例需要按照如下步骤进行。

注意：本案例需要的软件都已经共享在云盘，在第四阶段kubernetes/v1.17.6/ flannel目录下。各位同学需要提前将该目录下的素材下载到master主机。

**步骤一：导入并将镜像上传至192.168.1.100私有镜像服务器（在master主机操作）**

安装软件并启动服务

```shell
[root@master ~]# docker load -i flannel.tar.gz
# 加载镜像
[root@master ~]# docker tag \
quay.io/coreos/flannel:v0.12.0-amd64 192.168.1.100:5000/flannel:v0.12.0-amd64
# 修改标签
[root@master ~]# docker push 192.168.1.100:5000/flannel:v0.12.0-amd64
# 上传镜像到192.168.1.100服务器
```

**步骤二：配置flannel网络（master主机操作）**

1）修改资源配置文件

资源配置文件已经共享在云盘第四阶段kubernetes/v1.17.6/ flannel目录下。

```shell
[root@master ~]# vim flannel/kube-flannel.yaml
128: "Network": "10.244.0.0/16",        
# 该地址必须与案例3初始化文件 kubeadm-init.yaml 中的 podSubnet 一致
172: image: 192.168.1.100:5000/flannel:v0.12.0-amd64
186: image: 192.168.1.100:5000/flannel:v0.12.0-amd64
227行到结尾的所有内容全部删除
```

2）创建资源

```shell
[root@master ~]# kubectl apply -f kube-flannel.yml 
podsecuritypolicy.policy/psp.flannel.unprivileged created
clusterrole.rbac.authorization.k8s.io/flannel created
clusterrolebinding.rbac.authorization.k8s.io/flannel created
serviceaccount/flannel created
configmap/kube-flannel-cfg created
daemonset.apps/kube-flannel-ds-amd64 created
```

3）验证效果

```shell
[root@master ~]# ifconfig
flannel.1: flags=4163 ... ...
... ...
[root@master ~]# kubectl get nodes
NAME              STATUS    ROLES    AGE    VERSION
master            Ready    master    26h    v1.17.6
node-0001    Ready    <none>    152m    v1.17.6
```



# 6. 配置所有node节点完成集群部署

## 6.1 问题

本案例要求参考案例4将其他所有node节点加入K8s集群，具体要求如下：

1. 将node-0002加入K8S集群
2. 将node-0003加入K8S集群

## 6.2 步骤

实现此案例需要按照如下步骤进行。

具体操作步骤参考【4】，我们可以直接使用提前准备好的ansible剧本自动化完成添加node节点的任务，也可以尝试自己手动操作。
> 如有侵权，请联系作者删除
