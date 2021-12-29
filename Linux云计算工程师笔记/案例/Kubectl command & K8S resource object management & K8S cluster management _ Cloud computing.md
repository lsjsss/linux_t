@[TOC]( Kubectl explanation & K8S resource object management & K8S cluster management | Cloud computing )

---

# 1. kubectl基本命令

## 1.1 问题

本案例要求学习使用kubectl基本命令来管理kubernetes，具体要求如下：

1. 查询 节点 信息（node）
2. 启动容器（run）
3. 查询资源信息（deployment）
4. 查询容器信息（pod）
5. 进入容器（exec，attach）
6. 删除资源（delete）

## 1.2 方案

Kubectl是用于控制Kubernetes集群的命令行工具。

Kubectl的语法格式如下:

kubectl [command] [TYPE] [NAME] [flags]

command: 子命令，如 create，get，describe，delete

type: 资源类型，可以表示为单数，复数或缩写形式

name: 资源的名称，如果省略，则显示所有资源信息

flags: 指定可选标志，或附加的参数

## 1.3 步骤

实现此案例需要按照如下步骤进行。

**步骤一：kubectl命令练习（在master主机操作）**

1）run创建容器资源。

语法格式：kubectl run 资源名称 -i -t --image=私有仓库镜像名称:标签

```shell
[root@master ~]# kubectl run haha -i -t --image=192.168.1.100:5000/myos:v1804
kubectl run --generator=deployment/apps.v1 is DEPRECATED and will be removed in a future version. Use kubectl run --generator=run-pod/v1 or kubectl create instead.
If you don't see a command prompt, try pressing enter.
[root@haha-8bbd48d7b-wcnkd /]#                           #注意：这里已经进入了容器
[root@haha-8bbd48d7b-wcnkd /]# ifconfig 
eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1450
        inet 10.244.7.2  netmask 255.255.255.0  broadcast 0.0.0.0
```

2)get查询资源

语法格式：

kubectl get node 查询节点状态

kubectl get deployment 查询资源名称

kubectl get pod 查询pod容器资源

kubectl get pod -o wide 查询主机信息

kubectl get pod -o yaml 显示资源文件Yaml格式

```shell
[root@master ~]# kubectl  get  nodes
NAME             STATUS      ROLES       AGE           VERSION
master              Ready     master       12h       v1.17.6
node-0001           Ready    <none>     16h             v1.17.6
node-0002       Ready      <none>      16h             v1.17.6
node-0003       Ready     <none>       16h             v1.17.6
[root@master ~]# kubectl  get  deployment.apps
NAME           READY       UP-TO-DATE     AVAILABLE    AGE
haha           1/1         1                       1                  10m
[root@master ~]# kubectl get pod
NAME    READY    STATUS    RESTARTS       AGE
haha-xxxx    1/1    Running       1          14m
[root@master ~]# kubectl get pod -o wide
NAME    READY    STATUS    RESTARTS     AGE    IP                NODE           ... ...
haha-xxxx    1/1    Running       1        14m    10.244.7.4       node-0003     ... ...
```

3）exec进入一个正在运行的容器中

语法格式：

kubectl exec -it 容器id 执行的命令

```shell
[root@kube-master ~]# kubectl  get  pod
NAME                        READY       STATUS    RESTARTS        AGE
haha-8bbd48d7b-wcnkd       1/1            Running     0             31m
#查看一个容器资源的名称
[root@kube-master ~]# kubectl exec -it haha-8bbd48d7b-wcnkd /bin/bash
# 进入该容器中
[root@haha-8bbd48d7b-wcnkd /]#
```

4）查看资源的详细信息（主要用于排错）

语法格式：

kubectl describe 资源类型 资源名称

```shell
[root@kube-master ~]# kubectl describe  deployment  haha  
# 查看deployment资源的详细信息
Name:                  haha
Namespace:             default
CreationTimestamp:    Wed, 04 Mar 2020 15:50:24 +0800
... ...
[root@kube-master ~]# kubectl describe  pod  haha-8bbd48d7b-wcnkd 
# 查看容器的详细信息
Name:               haha-8bbd48d7b-wcnkd
Namespace:         default
Node:               kube-node1/192.168.1.11
Start Time:         Wed, 04 Mar 2020 15:50:24 +0800
Labels:             pod-template-hash=466804836
... ... 
```

5）查看 console 终端的输出信息

```shell
[root@kube-master ~]# kubectl attach haha-8bbd48d7b-wcnkd -c haha -i -t
If you don't see a command prompt, try pressing enter.
# 先通过attach进入一个容器
[root@haha-8bbd48d7b-wcnkd /]# echo hello world          #在容器中echo输出信息
hello world
[root@haha-8bbd48d7b-wcnkd /]#  Ctrl-p + Ctrl-q           #按快捷键退出
[root@kube-master ~]# 
[root@kube-master ~]# kubectl logs haha-8bbd48d7b-wcnkd 
[root@haha-8bbd48d7b-wcnkd /]# echo hello world
hello world
```

6）delete删除资源

语法格式：

kubectl delete 资源类型 资源名称

```shell
[root@kube-master ~]# kubectl delete pod haha-xxxxxxxx     
pod "haha-8bbd48d7b-wcnkd" deleted
# 删除pod，注意：这里的pod名称不能照抄！！！！
[root@kube-master ~]# kubectl get pod -o wide             # 容器被删除后会自动重建
NAME            READY    STATUS      RESTARTS   AGE     IP                NODE
haha-xxxxxxxx   1/1     Running     0            3s     10.254.9.2       kube-node2
haha-xxxxxxxx   1/1     Terminating  2             1h     10.254.39.2      kube-node1
[root@kube-master ~]# kubectl get deployment                 #查看deployment资源
NAME      DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
haha      1         1         1            1           1h
[root@kube-master ~]# kubectl  delete  deployment  haha  
deployment.extensions "haha" deleted
# 删除deployment资源，容器彻底消失
```



# 2 案例2：资源对象文件

## 2.1 问题

本案例要求熟悉资源文件的语法，具体要求如下：

1. 写一个 deployment 的资源文件
2. 启动一个基本系统(myos.yaml)
3. 启动一个 apache 服务(myweb.yaml)
4. 熟悉 kubectl 查询资源信息（deployment）
5. 熟悉 kubectl 查询容器信息（pod）
6. 熟悉 kubectl 进入容器（exec，attach）
7. 熟悉 kubectl 删除资源（delete）

## 2.2 步骤

实现此案例需要按照如下步骤进行。

**步骤一：查看现有资源的资源对象文件（在master主机操作）**

语法格式：

kubectl get 资源对象 资源名称 -o 格式（json|yaml）

```shell
[root@kube-master ~]# kubectl  get  deployment  apache  -o yaml
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  annotations:
... ...
# 导出deployment资源的资源对象文件，depoyment资源的名称为apache，导出yaml格式
```

**步骤二：编写资源对象文件（在master主机操作）**

注意：所有资源文件都在云盘第四阶段kubernetes/v1.17.6/config/目录有案例！！！

1）Pod资源文件

```shell
[root@master ~]# vim  mypod.yaml
---
kind: Pod
apiVersion: v1
metadata:
  name: mypod
spec:
  containers:
  - name: mylinux
    image: 192.168.1.100:5000/myos:v1804
    stdin: true
    tty: true
         
[root@master ~]# kubectl apply -f mypod.yaml 
pod/mypod created
[root@master ~]# kubectl get pod
NAME    READY   STATUS    RESTARTS   AGE
mypod   1/1     Running   0          13s
[root@master ~]# kubectl delete -f mypod.yaml
pod "mypod" deleted
[root@master ~]#
```

2）Deployment资源文件

```shell
[root@master ~]# vim myapache.yaml 
---
kind: Deployment
apiVersion: apps/v1
metadata:
  name: myapache
spec:
  selector:
    matchLabels:
      myapp: httpd
  replicas: 1
  template:
    metadata:
      labels:
        myapp: httpd
    spec:
      containers:
      - name: webcluster
        image: 192.168.1.100:5000/myos:httpd
        stdin: false
        tty: false
        ports:
        - protocol: TCP
          containerPort: 80
      restartPolicy: Always
[root@master ~]# kubectl apply -f myapache.yaml 
deployment.apps/myapache created
[root@master ~]# kubectl get deployments.apps
NAME       READY   UP-TO-DATE   AVAILABLE   AGE
myapache   1/1     1            1           19s
[root@master ~]# kubectl get pod
NAME                        READY   STATUS    RESTARTS   AGE
myapache-69b494dc5c-bff95   1/1     Running   0          28s
[root@master ~]#
```

3)备注

为了建立控制器和 pod 间的关联，kubernetes 先给每个 pod 打上一个标签（Label），然后再给相应的位置定义标签选择器（Label Selector），引用这些标签，资源文件的效果如下：

```shell
... ...             
 selector:                #声明标签选择器
    app: nginx         #为服务的后端选择标签 
... ...
  metadata:
      labels:          #声明标签
        app: nginx         #定义标签名字(上下标签必须一致)
... ...
```

4）如何使用资源文件

使用资源文件管理对象，语法格式：kubectl (apply|create|delete) -f 资源文件

- create 创建资源对象
- apply 声明更新资源对象
- delete 删除资源对象



# 3 案例3：集群扩容更新与回滚

## 3.1 问题

本案例主要练习集群扩容更新与回滚，分别实现以下目标：

1. 创建一个 myweb.yml 使用 apache 启动
2. 练习集群扩容
3. 更新：
4. 从 Apache 滚动更新到 nginx服务
5. 回滚 nginx 到 apache 服务
6. 验证

## 3.2 步骤

实现此案例需要按照如下步骤进行。

**步骤一：创建一个单节点的Web容器（在master主机操作操作）**

资源文件在云盘的第四阶段kubernetes/v1.17.6/config/目录有案例。

各位同学需要提前下载素材文件并传到master主机。

```shell
[root@master ~]# kubectl get deployments.apps
NAME       READY   UP-TO-DATE   AVAILABLE   AGE
myapache   1/1     1            1           113s
[root@master ~]# kubectl scale deployment myapache --replicas=3
deployment.apps/myapache scaled
[root@master ~]# kubectl get deployments.apps
NAME       READY   UP-TO-DATE   AVAILABLE   AGE
myapache   3/3     3            3           2m12s
[root@master ~]#
```

**步骤二：集群扩容（在master主机操作操作）**

我们可以使用命令行调整容器副本数量，也可以通过修改资源文件、更新资源的方式调整容器副本数量。

```shell
 [root@master ~]# kubectl scale deployment.apps httpd-example --replicas=3
```

**步骤三：集群更新与回滚**

各位同学需要提前下载素材文件并传到master主机。

```shell
[root@master config]# kubectl rollout history deployment myapache 
deployment.apps/myapache 
REVISION  CHANGE-CAUSE
1         <none>
[root@master ~]# curl http://10.244.3.5
this is apache
[root@master ~]# kubectl edit deployments.apps myapache 
deployment.apps/myapache edited
[root@master ~]# curl http://10.244.2.6
this is nginx
[root@master ~]# kubectl rollout history deployment myapache 
deployment.apps/myapache 
REVISION  CHANGE-CAUSE
1         <none>
2         <none>
[root@master ~]# kubectl rollout undo deployment myapache --to-revision=1
deployment.apps/myapache rolled back
[root@master ~]# curl http://10.244.3.6
this is apache
[root@master ~]#
```

**步骤三：节点标签选择器**

```shell
[root@master ~]# vim myapache.yaml 
---
kind: Deployment
apiVersion: apps/v1
metadata:
  name: myapache
spec:
  selector:
    matchLabels:
      myapp: httpd
  replicas: 1
  template:
    metadata:
      labels:
        myapp: httpd
    spec:
      nodeName: node-0001  # 新增一行
      containers:
      - name: webcluster
        image: 192.168.1.100:5000/myos:httpd
        stdin: false
        tty: false
        ports:
        - protocol: TCP
          containerPort: 80
      restartPolicy: Always
[root@master ~]# kubectl delete -f myapache.yaml 
deployment.apps "myapache" deleted
[root@master ~]# kubectl apply -f myapache.yaml 
deployment.apps/myapache created
[root@master ~]# kubectl get pods -o wide
NAME               READY   STATUS    RESTARTS   AGE     IP            NODE
myapache-xxx      1/1     Running   0          3m49s   10.244.3.9    node-0001
```



# 4 多标签节点匹配

```shell
[root@master ~]# kubectl delete -f myapache.yaml
deployment.apps "myapache" deleted
[root@master ~]# kubectl get nodes --show-labels 
NAME        STATUS   ROLES    AGE   VERSION   LABELS
master      Ready    master   10h   v1.17.6   kubernetes.io/hostname=master    ... ...
node-0001   Ready    <none>   10h   v1.17.6   kubernetes.io/hostname=node-0001 ... ...
node-0002   Ready    <none>   10h   v1.17.6   kubernetes.io/hostname=node-0002 ... ...
node-0003   Ready    <none>   10h   v1.17.6   kubernetes.io/hostname=node-0003 ... ...
[root@master ~]# kubectl label nodes node-0002 node-0003 disktype=ssd
node/node-0002 labeled
node/node-0003 labeled
[root@master ~]# kubectl get nodes --show-labels 
NAME        STATUS   ROLES    AGE   VERSION   LABELS
master      Ready    master   10h   v1.17.6   kubernetes.io/hostname=master    ... ...
node-0001   Ready    <none>   10h   v1.17.6   kubernetes.io/hostname=node-0001 ... ...
node-0002   Ready    <none>   10h   v1.17.6   disktype=ssd ... ...
node-0003   Ready    <none>   10h   v1.17.6   disktype=ssd ... ...
[root@master ~]# vim myapache.yaml
---
kind: Deployment
apiVersion: apps/v1
metadata:
  name: myapache
spec:
  selector:
    matchLabels:
      myapp: httpd
  replicas: 1
  template:
    metadata:
      labels:
        myapp: httpd
    spec:
      nodeSelector:        # 新添加
        disktype: ssd   # 新添加
      containers:
      - name: webcluster
        image: 192.168.1.100:5000/myos:httpd
        stdin: false
        tty: false
        ports:
        - protocol: TCP
          containerPort: 80
      restartPolicy: Always
[root@master ~]# kubectl scale deployment myapache --replicas=3
deployment.apps/myapache scaled
[root@master ~]# kubectl get pod -o wide
NAME        READY   STATUS    RESTARTS   AGE   IP           NODE        NOMINATED NODE   
myapache-xxx    1/1     Running   0          9s    10.244.1.7   node-0003   <none>           
myapache-xxx    1/1     Running   0          9s    10.244.2.8   node-0002   <none>           
myapache-xxx    1/1     Running   0          21s   10.244.2.7   node-0002   <none>           
[root@master ~]# kubectl delete -f myapache.yaml
deployment.apps "myapache" deleted
[root@master ~]# kubectl label nodes node-0002 node-0003 disktype-
node/node-0002 labeled
node/node-0003 labeled
[root@master ~]# kubectl get nodes --show-labels 
NAME        STATUS   ROLES    AGE   VERSION   LABELS
master      Ready    master   10h   v1.17.6   kubernetes.io/hostname=master    ... ...
node-0001   Ready    <none>   10h   v1.17.6   kubernetes.io/hostname=node-0001 ... ...
node-0002   Ready    <none>   10h   v1.17.6   kubernetes.io/hostname=node-0002 ... ...
node-0003   Ready    <none>   10h   v1.17.6   kubernetes.io/hostname=node-0003 ... ...
[root@master ~]#
```
> 如有侵权，请联系作者删除
