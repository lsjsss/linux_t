@[TOC]( K8S Resource object management & service and load balancing & Ingress | Cloud computing )

---

# 1. 创建DaemonSet资源文件

## 1.1 问题

本案例要求创建DaemonSet资源文件，具体要求如下：

1. 设置污点策略

## 1.2 步骤

实现此案例需要按照如下步骤进行。

**步骤一：创建daemonset资源（在master主机操作）**

1）查看、学习daemonset资源文件（仅查看即可）。

资源文件在云盘第四阶段kubernetes/v1.17.6/config/目录下。

```shell
[root@master ~]# vim mynginx.yaml
---
kind: DaemonSet
apiVersion: apps/v1
metadata:
  name: mynginx
spec:
  selector:
    matchLabels:
      myapp: nginx
  template:
    metadata:
      labels:
        myapp: nginx
    spec:
      containers:
      - name: nginxcluster
        image: 192.168.1.100:5000/myos:nginx
        stdin: false
        tty: false
        ports:
        - protocol: TCP
          containerPort: 80
      restartPolicy: Always
[root@master ~]# kubectl apply -f mynginx.yaml 
daemonset.apps/mynginx created
[root@master ~]# kubectl get pod -o wide
NAME            READY   STATUS    RESTARTS   AGE   IP            NODE
mynginx-77jtf   1/1     Running   0          6s    10.244.3.9    node-0001
mynginx-cwdzt   1/1     Running   0          6s    10.244.1.9    node-0003
mynginx-z2kl6   1/1     Running   0          6s    10.244.2.10   node-0002
[root@master ~]#
```

**步骤二：设置污点策略（在master主机操作）**

1）查看污点标签

污点标签包括：

- NoSchedule 不会被调度
- PreferNoSchedule 尽量不调度
- NoExecute 驱逐节点

```shell
[root@master ~]# kubectl describe node master
... ...
Taints:             node-role.kubernetes.io/master:NoSchedule
... ...
```

2）设置、删除污点标签

注意：可以自定义添加修改标签

注意：不要修改所有系统默认自带的标签

```shell
[root@master ~]# kubectl taint node node-0001 key=value:NoSchedule
# 给node-0001节点设置污点标签，设置NoSchedule标签
[root@master ~]# kubectl taint node node-0001 key-
# 删除node-0001的污点标签
```

**步骤二：设置污点策略（在master主机操作）**

nodeSelector是节点选择约束的最简单推荐形式。

我们可以给节点打上标签，根据标签来选择需要的节点

```shell
查看标签的命令：
[root@master ~]# kubectl  get node --show-labels
设置标签的命令
[root@master ~]# kubectl  label nodes <node-name> <label-key>=<label-value>
删除标签的命令
[root@master ~]# kubectl  label nodes <node-name> <label-key>-
```

污点案例：

```shell
[root@master ~]# kubectl delete -f mynginx.yaml 
daemonset.apps "mynginx" deleted
[root@master ~]# kubectl describe nodes |grep -P "^Taints"
Taints:             node-role.kubernetes.io/master:NoSchedule
Taints:             <none>
Taints:             <none>
Taints:             <none>
[root@master ~]# kubectl taint node node-0001 k1=v1:NoSchedule
node/node-0001 tainted
[root@master ~]# kubectl apply -f mynginx.yaml 
daemonset.apps/mynginx created
[root@master ~]# kubectl get pods
NAME            READY   STATUS    RESTARTS   AGE
mynginx-f2rxh   1/1     Running   0          4s
mynginx-n7xsw   1/1     Running   0          4s
[root@master ~]# kubectl taint node node-0001 k1-
node/node-0001 untainted
[root@master ~]# kubectl get pods
NAME            READY   STATUS    RESTARTS   AGE
mynginx-f2rxh   1/1     Running   0          105s
mynginx-hp6f2   1/1     Running   0          2s
mynginx-n7xsw   1/1     Running   0          105s
[root@master ~]#
```



# 2. 驱逐容器案例

```shell
[root@master ~]# kubectl apply -f myapache.yaml 
deployment.apps/myapache created
[root@master ~]# kubectl scale deployment myapache --replicas=3
deployment.apps/myapache scaled
[root@master ~]# kubectl get pod -o wide
NAME                       READY   STATUS    RESTARTS   AGE     IP            NODE
myapache-7d689bf8f-xq7l6   1/1     Running   0          2m23s   10.244.3.11   node-0001
myapache-7d689bf8f-b4d5f   1/1     Running   0          9s      10.244.2.14   node-0002
myapache-7d689bf8f-mzcgw   1/1     Running   0          9s      10.244.1.13   node-0003
mynginx-hp6f2              1/1     Running   0          5m25s   10.244.3.10   node-0001
mynginx-f2rxh              1/1     Running   0          7m8s    10.244.2.11   node-0002
mynginx-4f7tl              1/1     Running   0          20s     10.244.1.12   node-0003
[root@master ~]# kubectl taint node node-0003 k1=v1:NoExecute
node/node-0003 tainted
[root@master ~]# kubectl get pod -o wide
NAME                       READY   STATUS    RESTARTS   AGE     IP            NODE
myapache-7d689bf8f-xq7l6   1/1     Running   0          2m23s   10.244.3.11   node-0001
myapache-7d689bf8f-b4d5f   1/1     Running   0          9s      10.244.2.14   node-0002
myapache-7d689bf8f-mzcgw   1/1     Running   0          9s      10.244.2.15   node-0002
mynginx-hp6f2              1/1     Running   0          5m25s   10.244.3.10   node-0001
mynginx-f2rxh              1/1     Running   0          7m8s    10.244.2.11   node-0002
[root@master ~]# kubectl taint node node-0003 k1-
node/node-0003 untainted
[root@master ~]# kubectl get pod -o wide
NAME                       READY   STATUS    RESTARTS   AGE     IP            NODE
myapache-7d689bf8f-xq7l6   1/1     Running   0          2m23s   10.244.3.11   node-0001
myapache-7d689bf8f-b4d5f   1/1     Running   0          9s      10.244.2.14   node-0002
myapache-7d689bf8f-mzcgw   1/1     Running   0          9s      10.244.2.15   node-0002
mynginx-hp6f2              1/1     Running   0          5m25s   10.244.3.10   node-0001
mynginx-f2rxh              1/1     Running   0          7m8s    10.244.2.11   node-0002
mynginx-9s9z4              1/1     Running   0          34s     10.244.1.14   node-0003
[root@master ~]#
```



# 3. job和cronjob控制器的创建资源文件

## 4.1 问题

本案例练习书写job和cronjob控制器的资源文件。

1. 熟悉job控制器的资源文件
2. 熟悉cronjob控制器的资源文件

## 4.2 步骤

实现此案例需要按照如下步骤进行。

注意：资源文件在云盘第四阶段kubernetes/v1.17.6/config/目录下。

各位同学需要提前将该目录下的素材下载到master主机。

**步骤一：创建job计划任务控制器（在master主机操作）**

job任务是单任务

```shell
[root@master ~]# vim myjob.yaml
---
apiVersion: batch/v1
kind: Job
metadata:
  name: pi
spec:
  template:
    spec:
      containers:
      - name: pi
        image: 192.168.1.100:5000/myos:v1804
        command: ["perl",  "-Mbignum=bpi", "-wle", "print bpi(2000)"]
      restartPolicy: OnFailure
[root@master config]# kubectl apply -f myjob.yaml 
job.batch/pi created
[root@master config]# kubectl get job
NAME   COMPLETIONS   DURATION   AGE
pi     1/1           2s         7s
[root@master config]# kubectl get pod
NAME                     READY   STATUS      RESTARTS   AGE
pi-gvfwj                 0/1     Completed   0          15s
# 查看终端结果
[root@master config]# kubectl logs pi-gvfwj
```

**步骤二：创建cronjob计划任务控制器（在master主机操作）**

cronjob任务的本质是多次创建job（周期性计划任务）

```shell
[root@master ~]# vim mycronjob.yaml 
---
apiVersion: batch/v1beta1
kind: CronJob
metadata:
  name: cronjob-pi
spec:
  schedule: "*/1 * * * *"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: pi
            image: 192.168.1.100:5000/myos:v1804
            command: ["perl",  "-Mbignum=bpi", "-wle", "print bpi(2000)"]
          restartPolicy: OnFailure
[root@master ~]# kubectl apply -f mycronjob.yaml 
cronjob.batch/cronjob-pi created
[root@master ~]# kubectl get cronjobs.batch 
NAME         SCHEDULE           SUSPEND   ACTIVE        LAST SCHEDULE   AGE
cronjob-pi   */1 * * * *        False     0             <none>          10s
[root@master ~]# kubectl get pod
NAME                            READY     STATUS      RESTARTS          AGE
cronjob-pi-1595410620-vvztx     0/1       Completed   0                 62s
```

提示：需要等待 1 分钟才能看到变化。



# 4. 编写service资源文件（一）

## 4.1 问题

本案例要求学习service资源文件，具体要求如下：

1. 创建service服务，访问后端apache
2. 测试负载均衡
3. Headless 服务

## 4.2 方案

注意事项：

今日课程所用到的案例需要依赖前面docker课程中制作的镜像，必须将前面课程中的镜像全部导入到私有仓库（192.168.1.100服务器），镜像列表如下：

busybox:latest

myos:v1804

myos:httpd

myos:php-fpm

myos:nginx

## 4.3 步骤

实现此案例需要按照如下步骤进行。

**步骤一：创建service资源（在master主机操作）**

1）创建2副本的Web服务容器

资源文件已经共享在云盘第四阶段kubernetes/v1.17.6/config/apache-example.yaml，各位同学需要提前下载至自己的master主机。

使用资源文件创建一个多部分的容器环境，默认多副本会自动分配到不同的主机上运行。

2）删除一个pod，观察变化

当发现某一个pod不能使用的时候RS会在其他机器上在创建一个相同的pod，及其对应的容器。

```shell
[root@master ~]# kubectl apply -f myapache.yaml 
deployment.apps/myapache created
[root@master ~]# kubectl scale deployment myapache --replicas=2
deployment.apps/myapache scaled
[root@master ~]# kubectl get pod -o wide
NAME                       READY   STATUS    RESTARTS   AGE   IP            NODE
myapache-7d689bf8f-c268l   1/1     Running   0          13s   10.244.2.16   node-0002
myapache-7d689bf8f-4z225   1/1     Running   0          5s    10.244.1.15   node-0003
[root@master ~]# kubectl delete pod myapache-7d689bf8f-4z225 
pod "myapache-7d689bf8f-4z225" deleted
[root@master ~]# kubectl get pod -o wide
NAME                       READY   STATUS    RESTARTS   AGE   IP            NODE
myapache-7d689bf8f-c268l   1/1     Running   0          38s   10.244.2.16   node-0002
myapache-7d689bf8f-mccqv   1/1     Running   0          13s   10.244.3.12   node-0001
[root@master ~]#
```

3）service

因为容器随时都也被重建，其IP地址也跟着随机变化，我们如何访问容器呢？

service就是解决这一个问题的方法，service会创建一个cluster ip，service总能找到对应的 pod，且 cluster ip保持不变，如果有pod对应多个容器，service 会自动在多个容器间实现负载均衡。

创建service的资源文件已经共享在云盘第四阶段kubernetes/v1.17.6/config/service-example.yaml，各位同学提前下载该资源文件。

```shell
[root@master ~]# vim clusterip.yaml 
---
kind: Service
apiVersion: v1
metadata:
  name: myapache
spec:
  ports:
  - protocol: TCP
    port: 80
    targetPort: 80
  selector:
    myapp: httpd      # 标签必须与 deploy 资源文件中一致
  type: ClusterIP
[root@master config]# kubectl apply -f clusterip.yaml 
service/myapache created
[root@master config]# kubectl get service
NAME         TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)   AGE
kubernetes   ClusterIP   10.254.0.1       <none>        443/TCP   22h
myapache     ClusterIP   10.254.235.248   <none>        80/TCP    4s
```

4）验证效果

Service提供的集群IP，仅可以在集群内可以直接访问服务，但集群外无法访问服务。

下面测试访问使用的集群IP是随机的，不能照抄！！！

```shell
[root@master ~]# kubectl apply -f mypod.yaml 
pod/mypod created
[root@master ~]# kubectl exec -it mypod -- /bin/bash
[root@mypod /]# curl http://10.254.235.248/info.php
<pre>
Array
(
    [REMOTE_ADDR] => 10.244.1.16
    [REQUEST_METHOD] => GET
    [HTTP_USER_AGENT] => curl/7.29.0
    [REQUEST_URI] => /info.php
)
php_host:     myapache-7d689bf8f-mccqv
1229
[root@mypod /]# curl http://10.254.235.248/info.php
<pre>
Array
(
    [REMOTE_ADDR] => 10.244.1.16
    [REQUEST_METHOD] => GET
    [HTTP_USER_AGENT] => curl/7.29.0
    [REQUEST_URI] => /info.php
)
php_host:     myapache-7d689bf8f-c268l
1229
[root@mypod /]#
# 在master上执行扩容节点
[root@master ~]# kubectl scale deployment myapache --replicas=3
# 服务本质是LVS规则
[root@master ~]# ipvsadm -L -n
TCP  10.254.235.248:80 rr
  -> 10.244.1.17:80               Masq    1      0          0         
  -> 10.244.2.16:80               Masq    1      0          0         
  -> 10.244.3.12:80               Masq    1      0          0        
-----------------------------------------------------------------------------------------
# 在pod里访问
[root@pod-example /]# curl http://10.254.78.148/info.php
... ...
php_host:     myapache-7d689bf8f-lpt89
... ...
php_host:     myapache-7d689bf8f-mccqv
... ...
php_host:     myapache-7d689bf8f-c268l
```

**步骤二：使用nodeport发布服务（在master主机操作）**

```shell
[root@master ~]# vim mynodeport.yaml 
---
kind: Service
apiVersion: v1
metadata:
  name: mynodeport
spec:
  ports:
  - protocol: TCP
    port: 80
    targetPort: 80
  selector:
    myapp: httpd
  type: NodePort     # 指定服务类型
[root@master ~]# kubectl apply -f mynodeport.yaml 
[root@master ~]# kubectl get service
NAME         TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)        AGE
mynodeport   NodePort    10.254.105.233   <none>        80:31410/TCP   4s
#---------------------------所有node节点31410端口均可访问-----------------------------------
# 在跳板机上访问服务
[root@ecs-proxy ~]# curl http://192.168.1.31:31410/info.php
[root@ecs-proxy ~]# curl http://192.168.1.32:31410/info.php
[root@ecs-proxy ~]# curl http://192.168.1.33:31410/info.php
```



# 5. 编写service资源文件（二）

## 5.1 问题

本案例要求创建 headless 服务，具体要求如下：

1. 创建headless服务，并从集群外部测试访问效果

## 5.2 步骤

实现此案例需要按照如下步骤进行。

**步骤一：创建nodeport服务（在master主机操作）**

```shell
[root@master ~]# vim myheadless.yaml 
---
kind: Service
apiVersion: v1
metadata:
  name: myheadless
spec:
  ports:
  - protocol: TCP
    port: 80
    targetPort: 80
  selector:
    myapp: httpd
  type: ClusterIP
  clusterIP: None      # 新添加
[root@master ~]# kubectl apply -f myheadless.yaml 
service/myheadless created
[root@master ~]# kubectl get service
NAME         TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)   AGE
kubernetes   ClusterIP   10.254.0.1       <none>        443/TCP   22h
myapache     ClusterIP   10.254.235.248   <none>        80/TCP    7m52s
myheadless   ClusterIP   None             <none>        80/TCP    3s
#-----------------------------------进入pod查看解析结果------------------------------------
[root@master ~]# kubectl exec -it pod-example -- /bin/bash
[root@mypod /]# yum install -y bind-utils
[root@mypod /]# host myheadless.default.svc.cluster.local
myheadless.default.svc.cluster.local has address 10.244.3.12
myheadless.default.svc.cluster.local has address 10.244.1.17
myheadless.default.svc.cluster.local has address 10.244.2.16
```



# 6. 对外发布服务

## 6.1 问题

本案例主要练习ingress控制器，分别实现以下目标：

1. 安装配置ingress控制器
2. 通过ingress向外发布服务

## 6.2 步骤

实现此案例需要按照如下步骤进行。

**步骤一：安装ingress控制器（在master主机操作操作）**

ingress控制器对应的镜像文件已经共享在云盘第四阶段kubernetes/v1.17.6/ingress/ingress-nginx.tar.gz。各位同学需要提前下载。

1) 首先需要将ingress镜像上传至私有镜像仓库（192.168.1.100服务器）

```shell
[root@master ~]# docker load -i ingress-nginx.tar.gz
[root@master ~]# docker tag  quay.io/kubernetes-ingress-controller/nginx-ingress-controller  192.168.1.100:5000/nginx-ingress-controller:0.30.0
[root@master ~]# docker push 192.168.1.100:5000/nginx-ingress-controller:0.30.0
```

2) 验证仓库

```shell
[root@master ~]#curl http://192.168.1.100:5000/v2/nginx-ingress-controller/tags/list
{"name":"nginx-ingress-controller","tags":["0.30.0"]}
[root@master ~]# kubectl apply -f httpd-example-v1.yaml 
deployment.apps/web-example configured
```

3) 创建ingress资源

资源文件已经共享在云盘第四阶段kubernetes/v1.17.6/ingress/目录下，各位同学需要自行下载该资源文件，并需要修改该文件才可以使用。

修改资源文件mandatory.yaml，指定启动ingress容器时应该从私有仓库下载镜像，而默认指定的是官网。

```shell
[root@master ~]# vim ingress/mandatory.yaml            #修改镜像文件image的路径
221:  image: 192.168.1.100:5000/nginx-ingress-controller:0.30.0
[root@master ~]# kubectl create -f ingress/mandatory.yaml       #创建资源
namespace/ingress-nginx created
[root@master ~]# kubectl -n ingress-nginx  get  pod              #查看资源
NAME                                              READY       STATUS     RESTARTS   AGE
nginx-ingress-controller-fc6766d7-xtsp2       1/1         Running    0              50m
```

**步骤二：通过ingress对外发布容器服务（在master主机操作操作）**

1）创建资源，通过ingress映射内部服务

```shell
[root@master ~]# vim  ingress-example.yaml
---
apiVersion: extensions/v1beta1
kind: Ingress                            # 资源对象类型
metadata:
  name: my-app                        # ingress 资源名称
  annotations:
    kubernetes.io/ingress.class: "nginx"
spec:
  backend:                            # 后端服务
    serviceName: apache-service        # service 名称，需要查看之前实验创建的名称
    servicePort: 80                    # 服务端口号，是服务的 Port 
#注意：这里的apache-service是前面实验创建的service的名称
#前面service创建的集群IP只能在内部访问，现在通过inpress映射service
#用户访问ingress生成的IP就会自动映射到service的集群IP，集群IP再映射到容器IP
[root@master ~]# kubectl apply -f ingress-example.yaml
```

2）验证效果

```shell
[root@master ~]# kubectl  get  ingress       #查看ingress资源，查看inpressIP地址
NAME          HOSTS         ADDRESS          PORTS         AGE
my-app           *            192.168.1.31      80            16s
------------------------------------------------------------------------------
[root@localhost ~]# curl http://192.168.1.31           #现在，任意主机都可以访问服务
<pre>
Array
(
    [REMOTE_ADDR] => 10.244.6.1
    [REQUEST_METHOD] => GET
    [HTTP_USER_AGENT] => curl/7.29.0
    [REQUEST_URI] => /
)
php_host:     apache-example-9d8577cf-lw74h
```
> 如有侵权，请联系作者删除
