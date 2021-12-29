@[TOC]( Monitor resource usage & manage storage volumes | Cloud computing )

---

# 1. 安装部署metrics-server

## 1.1 问题

本案例要求安装部署metrics-server，具体要求如下：

1. 修改 apiserver 的启动参数，添加聚合API
2. 配置文件路径 /etc/kubernetes/manifests/kube-apiserver.yaml
3. \- --enable-aggregator-routing=true
4. 重启 kubelet 服务
5. 导入镜像，部署metrics-server
6. pdb.yaml, rbac.yaml
7. deployment.yaml, service.yaml,apiservice.yaml
8. 验证 kubectl top node

## 1.2 方案

metrics是一个监控系统资源使用的插件，可以监控node节点上的cpu、内存的使用率，或pod对资源的占用率，通过对资源占用的了解，可以更加合理的部署容器应用

## 1.3 步骤

实现此案例需要按照如下步骤进行。

没有安装部署metrics之前查看node节点信息会失败。

```shell
[root@master ~]# kubectl  top  node
Error from server (NotFound): the server could not find the requested resource (get services http:heapster:)
```

**步骤一：修改kube-apiserver配置文件（在master主机操作）**

1）开启聚合服务

默认K8S不支持聚合服务就没法用metrics，这里首先需要修改配置文件开启该功能。

```shell
[root@master ~]# vim /etc/kubernetes/manifests/kube-apiserver.yaml
#在该文件中找spec.containers.command ，在它的最下面手动添加如下一行内容：
- --enable-aggregator-routing=true
[root@master ~]# systemctl  restart  kubelet             #重启服务
[root@master ~]# kubectl -n kube-system get pod \
kube-apiserver-master -o yaml |grep enable-aggregator-routing
#修改完成后，将kube-apiserver的配置导出查看是否有刚刚添加的参数，有就代表成功了
#这一步是验证的操作
```

2）设置kubelet证书

```shell
[root@master ~]# vim /var/lib/kubelet/config.yaml    #在文件末尾手动添加如下一行
serverTLSBootstrap: true
[root@master ~]# systemctl  restart  kubelet             #重启服务
# 等待几分钟后就能看到了
[root@master ~]# kubectl get certificatesigningrequests
NAME        AGE    REQUESTOR        CONDITION
csr-nvd65        8m          system:node:master            Pending
csr-6qz7b        4m34s       system:node:node-0003        Pending
csr-rft2l        4m46s       system:node:node-0002     Pending
csr-t5fvc        5m2s        system:node:node-0001     Pending
#这里查看到所有的主机都在等待证书的签发
#master主机的证书目前状态为Pending，代表正在等待证书的签发
#node-0003主机的证书目前状态为Pending，代表正在等待证书的签发
#node-0002主机的证书目前状态为Pending，代表正在等待证书的签发
#node-0001主机的证书目前状态为Pending，代表正在等待证书的签发
```

重要：修改配置文件开启证书后，所有主机的证书都没有签发，下面需要给所有主机都签发证书（等于是给证书签个名才能用）

注意：是所有主机的证书都需要签发，如何签发呢？具体语法格式如下：

kubectl certificate approve 名称

这里最后的名称就是上面kubectl get certificatesigningrequests命令查看到的名称

```shell
[root@master ~]# kubectl certificate approve csr-nvd65    # 签发证书
[root@master ~]# kubectl certificate approve csr-6qz7b    # 签发证书
[root@master ~]# kubectl certificate approve csr-rft2l    # 签发证书
[root@master ~]# kubectl certificate approve csr-t5fvc    # 签发证书
#注意：最后的名称不能照抄，一定要自己通过kubectl get certificatesigningrequests查看
```

再次查看证书状态

```shell
[root@master ~]# kubectl get certificatesigningrequests
NAME        AGE    REQUESTOR        CONDITION
csr-nvd65        16m       system:node:master            Approved,Issued
csr-t5fvc        13m       system:node:node-0001     Approved,Issued
csr-rft2l        13m       system:node:node-0002     Approved,Issued
csr-6qz7b        13m       system:node:node-0003     Approved,Issued
#所有证书状态都是Approved（已经被签发了）
```

**步骤二：安装metrics-server（在master主机操作）**

1）导入镜像到私有镜像仓库（192.168.1.100服务器）

镜像及资源文件在云盘第四阶段kubernetes/v1.17.6/metrics/目录下，各位同学需要提前下载。

```shell
[root@master ~]# docker load -i metrics-server.tar.gz
[root@master ~]# docker images            #查看metrics-server镜像的名称
[root@master ~]# docker tag  旧名称   192.168.1.100:5000/metrics-server:master
[root@master ~]# docker push  192.168.1.100:5000/metrics-server:master
```

2）修改资源文件

所有资源文件在云盘第四阶段kubernetes/v1.17.6/metrics/目录下，各位同学需要提前下载。

```shell
[root@master metrics]# vim deployment.yaml           
29： image: 192.168.1.100:5000/metrics-server:master
# 该行原文指向官网地址，我们需要修改为自己的私有镜像仓库
# 启动metrics-server容器时就从私有仓库下载镜像然后再启动容器，否则默认是连接官网找镜像
```

3）依次创建所有资源

```shell
[root@master metrics]# kubectl apply -f rbac.yaml 
[root@master metrics]# kubectl apply -f pdb.yaml 
[root@master metrics]# kubectl create -f deployment.yaml 
[root@master metrics]# kubectl apply -f service.yaml 
[root@master metrics]# kubectl apply -f apiservice.yaml 
```

4）验证

```shell
[root@master metrics]# kubectl -n kube-system get pod           # 验证POD
NAME                     READY       STATUS        RESTARTS   AGE
metrics-server-xxx     1/1      Running          0          9m15s
... ...
[root@master metrics]# kubectl -n kube-system get apiservices     # 验证API
NAME                         SERVICE                          AVAILABLE    AGE
v1beta1.metrics.k8s.io        kube-system/metrics-server     True           15m
[root@master metrics]# kubectl  top  node
error: metrics not available yet    # 你需要等几分钟，还没有收集数据
[root@master metrics]# kubectl  top  node
NAME         CPU(cores)    CPU%       MEMORY(bytes)      MEMORY%   
master        73m             3%       1196Mi             68%       
node-0001       20m              1%     729Mi              41%  
... ...     
```



# 2. 容器资源利用率监控

```shell
[root@master ~]# kubectl apply -f myapache.yaml 
deployment.apps/myapache created
[root@master ~]# kubectl top pod
error: metrics not available yet
# 等待大约 30 秒
[root@master ~]# kubectl top pod
NAME                       CPU(cores)   MEMORY(bytes)   
myapache-7d689bf8f-lfr5h   0m           0Mi   
[root@master ~]# curl http://10.244.2.17/info.php?id=5000000
<pre>
Array
(
    [REMOTE_ADDR] => 10.244.0.0
    [REQUEST_METHOD] => GET
    [HTTP_USER_AGENT] => curl/7.29.0
    [REQUEST_URI] => /info.php?id=5000000
    [id] => 5000000
)
php_host:     myapache-7d689bf8f-lfr5h
[root@master ~]# kubectl top pod
NAME                       CPU(cores)   MEMORY(bytes)   
myapache-7d689bf8f-w4rtt   1000m        8Mi  
[root@master ~]#
```



# 3. configMap练习

## 3.1 问题

本案例主要做configMap练习，具体要求如下：

1. 通过configMap修改nginx的配置文件
2. 让nginx支持php

## 3.2 方案

ConfigMap是在Pod中映射(文件/目录)的一种方式，允许你将配置文件与镜像文件分离，以使容器化的应用程序具有可移植性。

通过ConfigMap我们可以把真机的目录或文件映射到容器中。

## 3.3 步骤

实现此案例需要按照如下步骤进行。

**步骤一：创建configMap资源（在master主机操作）**

1）准备一个nginx的配置文件。

启动一个容器，从容器中将nginx.conf文件拷贝到真机。

```shell
[root@master ~]# mkdir /var/webconf
[root@master ~]# docker run -itd --name mynginx 192.168.1.100:5000/myos:nginx
9f719d0e797f81887b21985a31f426c1f2c48efd24a2c6666ecf41396fb99e93
[root@master ~]# docker cp mynginx:/usr/local/nginx/conf/nginx.conf /var/webconf/
[root@master ~]# docker rm -f mynginx
mynginx
[root@master ~]# ls -l /var/webconf/
total 4
-rw-r--r-- 1 root root 2656 Jul 25  2020 nginx.conf
[root@master ~]# vim /var/webconf/nginx.conf 
... ...
        location ~ \.php$ {
            root           html;
            fastcgi_pass   127.0.0.1:9000;
            fastcgi_index  index.php;
            include        fastcgi.conf;
        }
... ...
[root@master ~]# kubectl create configmap nginx-conf --from-file=/var/webconf/nginx.conf 
configmap/nginx-conf created
[root@master ~]# kubectl get configmaps 
NAME         DATA   AGE
nginx-conf   1      8s
[root@master ~]#
```

2）定义configMap

configMap可以映射单一文件，也可以映射一个目录。

语法格式：kubectl create configmap 名称 --from-file=文件路径

```shell
[root@master ~]# kubectl create configmap nginx-conf --from-file=nginx.conf 
configmap "nginx-conf" created
# 创建一个名称为nginx-conf的configMap，对应的是真机的nginx.conf文件
[root@master ~]# kubectl get configmap nginx-conf       #查看configMap
NAME          DATA          AGE
nginx-conf       1             10s
```

3）使用资源文件启动容器调用前面定义的configMap

资源文件已经工作在云盘第四阶段kubernetes/v1.17.6/config/目录下。

```shell
[root@master ~]# vim webnginx.yaml
---
kind: Deployment
apiVersion: apps/v1
metadata:
  name: webnginx
spec:
  selector:
    matchLabels:
      myapp: nginx
  replicas: 1
  template:
    metadata:
      labels:
        myapp: nginx
    spec:
      volumes:                      # 新添加
      - name: nginx-php             # 新添加（标记1）
        configMap:                  # 新添加
          name: nginx-conf          # 新添加，必须与 configmap 命令创建的名称相同
      containers:
      - name: nginx
        image: 192.168.1.100:5000/myos:nginx
        volumeMounts:               # 新添加
        - name: nginx-php           # 新添加，必须与（标记1）名称相同
          subPath: nginx.conf       # 新添加
          mountPath: /usr/local/nginx/conf/nginx.conf     # 新添加
        ports:
        - protocol: TCP
          containerPort: 80
      restartPolicy: Always
[root@master ~]# kubectl apply -f webnginx.yaml 
deployment.apps/webnginx created
[root@master ~]# kubectl get pod 
NAME                        READY   STATUS    RESTARTS   AGE
webnginx-844859695b-5s7m7   1/1     Running   0          10s
[root@master ~]# kubectl exec -it webnginx-844859695b-5s7m7 -- /bin/bash
[root@webnginx-844859695b-5s7m7 html]# cat /usr/local/nginx/conf/nginx.conf
# 查看配置文件是否改变了
[root@webnginx-844859695b-kmwwh html]# ss -ltun
Netid  State      Recv-Q Send-Q      Local Address:Port      Peer Address:Port            
tcp    LISTEN     0      128                     *:80                   *:*                                
[root@webnginx-844859695b-kmwwh html]# exit
[root@master ~]# kubectl delete -f webnginx.yaml 
deployment.apps "webnginx" deleted
[root@master ~]#
```

4）添加PHP容器，测试网页

```shell
[root@master ~]# vim webnginx.yaml
---
kind: Deployment
apiVersion: apps/v1
metadata:
  name: webnginx
spec:
  selector:
    matchLabels:
      myapp: nginx
  replicas: 1
  template:
    metadata:
      labels:
        myapp: nginx
    spec:
      volumes:
      - name: nginx-php
        configMap: 
          name: nginx-conf
      containers:
      - name: nginx
        image: 192.168.1.100:5000/myos:nginx
        volumeMounts:
        - name: nginx-php
          subPath: nginx.conf
          mountPath: /usr/local/nginx/conf/nginx.conf
        ports:
        - protocol: TCP
          containerPort: 80
      - name: php-backend                       # 新添加
        image: 192.168.1.100:5000/myos:php-fpm  # 新添加
      restartPolicy: Always
[root@master ~]# kubectl apply -f config/webnginx.yaml 
deployment.apps/webnginx created
[root@master ~]# kubectl get pod -o wide
NAME                        READY   STATUS    RESTARTS   AGE    IP            NODE      
webnginx-6c9f6fd675-7rmzk   2/2     Running   0          5s        10.244.2.25   node-0002
[root@master ~]# kubectl exec -it webnginx-6c9f6fd675-7rmzk -c nginx -- /bin/bash
[root@webnginx-6c9f6fd675-7rmzk html]# ss -ltun
Netid  State      Recv-Q Send-Q      Local Address:Port      Peer Address:Port              
tcp    LISTEN     0      128                     *:80                   *:*                  
tcp    LISTEN     0      128                     *:9000                 *:*
[root@webnginx-6c9f6fd675-7rmzk html]# exit
[root@master ~]# curl http://10.244.2.25/info.php
<pre>
Array
(
    [REMOTE_ADDR] => 10.244.0.0
    [REQUEST_METHOD] => GET
    [HTTP_USER_AGENT] => curl/7.29.0
    [REQUEST_URI] => /info.php
)
php_host:     webnginx-6c9f6fd675-7rmzk
1229
[root@master ~]#
```



# 4. 网络存储卷应用案例



# 5 emptydir案例

```shell
[root@master ~]# vim webcache.yaml 
---
kind: Deployment
apiVersion: apps/v1
metadata:
  name: webcache
spec:
  selector:
    matchLabels:
      myapp: cache
  replicas: 1
  template:
    metadata:
      labels:
        myapp: cache
    spec:
      volumes:                       # 新添加
      - name: empty-data             # 新添加
        emptyDir: {}                 # 新添加
      containers:
      - name: apache
        image: 192.168.1.100:5000/myos:httpd
        stdin: false
        tty: false
        volumeMounts:                # 新添加
        - name: empty-data           # 新添加
          mountPath: /var/cache      # 新添加
        ports:
        - protocol: TCP
          containerPort: 80
      restartPolicy: Always
[root@master ~]# kubectl apply -f webcache.yaml 
deployment.apps/webcache created
[root@master ~]# kubectl exec -it webcache-c58847c54-qw9lh -- /bin/bash
[root@webcache-c58847c54-qw9lh html]# df -h
Filesystem       Size   Used       Avail        Use%       Mounted on
/dev/vda1        40G    2.9G       35G          8%         /var/cache
... ...
[root@webcache-c58847c54-qw9lh html]# exit
[root@master ~]#
```



# 6 hostpath案例

```shell
[root@master ~]# cat webcache.yaml 
---
kind: Deployment
apiVersion: apps/v1
metadata:
  name: webcache
spec:
  selector:
    matchLabels:
      myapp: cache
  replicas: 1
  template:
    metadata:
      labels:
        myapp: cache
    spec:
      volumes:
      - name: empty-data
        emptyDir: {}
      - name: log-data                # 新添加
        hostPath:                     # 新添加
          path: /var/weblog           # 新添加
          type: DirectoryOrCreate     # 新添加
      containers:
      - name: apache
        image: 192.168.1.100:5000/myos:httpd
        stdin: false
        tty: false
        volumeMounts:
        - name: empty-data
          mountPath: /var/cache
        - name: log-data             # 新添加
          mountPath: /var/log/httpd  # 新添加
        ports:
        - protocol: TCP
          containerPort: 80
      restartPolicy: Always
[root@master ~]# kubectl apply -f webcache.yaml 
deployment.apps/webcache created
[root@master ~]# kubectl get pod -o wide
NAME                        READY   STATUS    RESTARTS   AGE   IP            NODE
webcache-75588b9cc5-xzkvc   1/1     Running   0          4s    10.244.2.30   node-0002
[root@master ~]# curl http://10.244.2.30/
this is apache
[root@master ~]# ssh 192.168.1.32
root@192.168.1.32's password: 
Last login: Mon Apr 26 10:41:58 2021 from 192.168.1.252
Welcome to Huawei Cloud Service
[root@node-0002 ~]# ls -l /var/weblog/
total 16
-rw-r--r--   1 root root   86 Apr 26 13:12 access_log
-rw-r--r--   1 root root  489 Apr 26 13:12 error_log
[root@node-0002 ~]# cat /var/weblog/access_log 
10.244.0.0 - - [26/Apr/2021:05:12:59 +0000] "GET / HTTP/1.1" 200 15 "-" "curl/7.29.0"
[root@node-0002 ~]#
```



# 7 pv/pvc案例

## 7.1 问题

本案例练习练习使用网络存储卷，具体要求如下。

1. 安装 NFS服务
2. 定义 PV，PVC
3. 在K8S集群中挂载NFS存储卷

## 7.2 步骤

实现此案例需要按照如下步骤进行。

**步骤一：部署NFS服务器（在192.168.1.100主机操作）**

1）部署服务器

```shell
[root@registry ~]# yum install -y nfs-utils
[root@registry ~]# mkdir -m 777 /var/webroot
[root@registry ~]# vim  /etc/exports
/var/webroot    *(rw)
[root@registry ~]# systemctl enable --now nfs
```

2）任意其他主机做客户端测试

```shell
[root@localhost ~]# yum install -y nfs-utils
[root@localhost ~]# showmount -e 192.168.1.100
Export list for 192.168.1.100:
/var/webroot *
```

**步骤二：创建PV/PVC资源（在master主机操作）**

对应的资源文件在云盘第四阶段kubernetes/v1.17.6/config/目录。

1）创建PV资源

```shell
[root@master ~]# vim mypv.yaml 
---
kind: PersistentVolume
apiVersion: v1
metadata:
  name: pv-nfs
spec:
  volumeMode: Filesystem
  capacity:
    storage: 30Gi
  accessModes:
  - ReadWriteOnce
  - ReadOnlyMany
  - ReadWriteMany
  persistentVolumeReclaimPolicy: Retain
  nfs:
    server: 192.168.1.100
    path: /var/webroot
[root@master ~]# kubectl apply -f mypv.yaml 
persistentvolume/pv-nfs created
[root@master ~]# kubectl get pv
NAME     CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS          AGE
pv-nfs   30Gi       RWO,ROX,RWX    Retain           Available       3s
```

2）创建PVC资源（默认情况下PVC与PV会自动匹配容量大小、自动映射）

```shell
[root@master configmap]# vim mypvc.yaml 
---
kind: PersistentVolumeClaim
apiVersion: v1
metadata:
  name: pvc-nfs
spec:
  volumeMode: Filesystem
  accessModes:
  - ReadWriteMany
  resources:
    requests:
      storage: 25Gi
[root@master configmap]# kubectl apply -f mypvc.yaml
[root@master configmap]# kubectl get pv
NAME     CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM
pv-nfs   30Gi       RWX            Retain           Bound    default/pvc-nfs
[root@master configmap]# kubectl get pvc
NAME      STATUS   VOLUME   CAPACITY   ACCESS MODES   STORAGECLASS   AGE
pvc-nfs   Bound    pv-nfs   30Gi       RWO,ROX,RWX                   27s
```

3）创建容器资源，调用PVC

```shell
[root@master ~]# cat webnginx.yaml 
---
kind: Deployment
apiVersion: apps/v1
metadata:
  name: webnginx
spec:
  selector:
    matchLabels:
      myapp: nginx
  replicas: 1
  template:
    metadata:
      labels:
        myapp: nginx
    spec:
      volumes:
      - name: nginx-php
        configMap: 
          name: nginx-conf
      - name: website                     # 新添加
        persistentVolumeClaim:            # 新添加
          claimName: pvc-nfs              # 新添加
      containers:
      - name: nginx
        image: 192.168.1.100:5000/myos:nginx
        volumeMounts:
        - name: nginx-php
          subPath: nginx.conf
          mountPath: /usr/local/nginx/conf/nginx.conf
        - name: website                     # 新添加
          mountPath: /usr/local/nginx/html  # 新添加
        ports:
        - protocol: TCP
          containerPort: 80
      - name: php-backend
        image: 192.168.1.100:5000/myos:php-fpm
        volumeMounts:                       # 新添加
        - name: website                     # 新添加
          mountPath: /usr/local/nginx/html  # 新添加
      restartPolicy: Always
[root@master ~]# kubectl delete -f webnginx.yaml 
deployment.apps "webnginx" deleted
[root@master ~]# kubectl apply -f webnginx.yaml 
deployment.apps/webnginx created
[root@master ~]# kubectl get pod -o wide
NAME                       READY   STATUS    RESTARTS   AGE   IP            NODE
webnginx-d488b9447-t62cl   2/2     Running   0          7s    10.244.2.32   node-0002
[root@master ~]# curl http://10.244.2.32/
# 在 nfs 上创建修改页面，然后在容器端访问测试
```



# 8. 微服务web集群实战

## 8.1 问题

本案例结合前面的实验步骤做一个综合的微服务课外练习，具体要求如下。

1. 使用myos:php-fpm 创建后端应用php-app
2. 创建php-service，为后端应用提供内部clusterIP和负载均衡
3. 使用myos:nginx创建应用，并使用php-service解析php文件
4. 创建web-service，发布nginx应用到nodePort
5. 使用Ingress对外发布服务nginx应用

## 8.2 步骤

实现此案例需要参考前面的案例1至案例5的内容自行完成。

> 如有侵权，请联系作者删除
