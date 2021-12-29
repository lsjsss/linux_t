@[TOC]( Deploy Dashboard & Prometheus & HPA clusters | Cloud computing )

---

# 1. 安装部署dashboard

## 1.1 问题

本案例要求安装部署dashboard，具体要求如下：

1. 导入镜像到私有仓库
2. 修改配置文件recommended.yaml
3. 添加NodePort端口
4. 修改镜像地址
5. 部署dashboard
6. 创建管理用户admin-user
7. 使用token登录页面访问

## 1.2 步骤

实现此案例需要按照如下步骤进行。

**步骤一：部署dashboard（在master主机操作）**

所有镜像及资源文件在云盘 kubernetes/v1.17.6/dashboard/目录，各位同学提前下载素材。

1）导入镜像到私有镜像仓库（192.168.1.100服务器）

镜像文件在云盘第四阶段kubernetes/v1.17.6/dashboard/目录下，各位同学需要提前下载。

需要导入的镜像包括：

- dashboard.tar.gz 主服务镜像
- metrics-scraper.tar.gz 收集监控信息插件

```shell
[root@master ~]# docker load  -i dashboard.tar.gz
[root@master ~]# docker images            #查看dashboard镜像的名称
[root@master ~]# docker tag  旧名称   192.168.1.100:5000/dashboard:v2.0.0
[root@master ~]# docker push  192.168.1.100:5000/dashboard:v2.0.0
[root@master ~]# docker load  -i metrics-scraper.tar.gz
[root@master ~]# docker images            #查看metrics-scraper镜像的名称
[root@master ~]# docker tag  旧名称   192.168.1.100:5000/metrics-scraper:v1.0.4
[root@master ~]# docker push  192.168.1.100:5000/metrics-scraper:v1.0.4
```

2）创建相关资源完成部署

资源文件在云盘 kubernetes/v1.17.6/dashboard/目录，各位同学提前下载素材。

```shell
[root@master dashboard]# vim recommended.yaml
          # 190 行修改为
          image: 192.168.1.100:5000/dashboard:v2.0.0
          # 274 行修改为
          image: 192.168.1.100:5000/metrics-scraper:v1.0.4
[root@master dashboard]# kubectl apply -f recommended.yaml
# ---------------------------------- 查询验证 --------------------------------------
[root@master dashboard]# kubectl -n kubernetes-dashboard get pod
NAME                                         READY   STATUS    RESTARTS   AGE
dashboard-metrics-scraper-57bf85fcc9-vsz74   1/1     Running   0          52s
kubernetes-dashboard-7b7f78bcf9-5k8vq        1/1     Running   0          52s
[root@master dashboard]# kubectl -n kubernetes-dashboard get service
NAME                        TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)
dashboard-metrics-scraper   ClusterIP   10.254.76.85     <none>        8000/TCP
kubernetes-dashboard        ClusterIP   10.254.211.125   <none>        443/TCP
# ---------------------------------- 对外发布服务 -----------------------------------
[root@master dashboard]# vim service.yaml
---
kind: Service
apiVersion: v1
metadata:
  labels:
    k8s-app: kubernetes-dashboard
  name: kubernetes-dashboard
  namespace: kubernetes-dashboard
spec:
  ports:
    - port: 443
      nodePort: 30443                # 新添加
      targetPort: 8443
  selector:
    k8s-app: kubernetes-dashboard
  type: NodePort                     # 新添加
[root@master dashboard]# kubectl apply -f service.yaml 
service/kubernetes-dashboard configured
[root@master dashboard]# kubectl -n kubernetes-dashboard get service
NAME                        TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)         AGE
dashboard-metrics-scraper   ClusterIP   10.254.66.25     <none>        8000/TCP        2m6s
kubernetes-dashboard        NodePort    10.254.165.155   <none>        443:30443/TCP   2m6s
[root@master dashboard]#
```

3）验证

浏览器访问任意节点IP的30443端口(http://任意节点:30443 端口

)即可查看Web页面，效果如图-1所示。

![img](https://img-blog.csdnimg.cn/img_convert/70a1de5ea34b921d344c444778840c1d.png)

图-1

4）创建管理用户

素材在云盘 kubernetes/v1.17.6/dashboard/admin-token.yaml

```shell
[root@master dashboard]# cat admin-token.yaml          #查看、学习资源文件
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: admin-user
  namespace: kubernetes-dashboard
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: admin-user
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
- kind: ServiceAccount
  name: admin-user
  namespace: kubernetes-dashboard
[root@master dashboard]# kubectl create -f admin-token.yaml   #创建资源
```

5）查看登录的Token信息

先通过get screts查看名称，该名称是随机的，然后再通过查询到的名称继续查询对应的Token信息。

```shell
[root@master ~]# kubectl -n kubernetes-dashboard get secrets 
NAME             TYPE                                  
admin-user-token-xxx    kubernetes.io/service-account-token  ... ...
[root@master ~]# kubectl -n kubernetes-dashboard describe secrets \
... ...
token:      eyJhbGciOiJSUzI1NiIsImtpZCI6IjJyTE9nZWpWLWFhTXV6cnJla3U4aX
NngxVTZjV2M5Y0FYOWR0ancifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9 ... ...
```

再次使用浏览器访问任意节点IP的30090端口(http://任意节点:30090 端口

)即可查看Web页面，输入Token，效果如图-2所示。

![img](https://img-blog.csdnimg.cn/img_convert/842a1ae8791e7064aefec7c890e4dea4.png)

图-2



# 2. 安装部署pometheus（一）

## 2.1 问题

本案例安装部署pometheus，具体要求如下：

1. 安装Prometheus operator
2. 安装Prometheus server
3. 安装Prometheus adapter
4. 安装metrics-state
5. 安装node-exporter
6. 安装 altermanager
7. 安装 grafana

## 2.2 步骤

实现此案例需要按照如下步骤进行。

**步骤一：导入所有后续需要的镜像到私有镜像仓库（在master主机操作操作）**

所有镜像文件在云盘第四阶段kubernetes/v1.17.6/prometheus/images目录下，各位同学需要提前下载。

需要导入的镜像包括：

- prometheus.tar.gz
- prometheus-operator.tar.gz
- prometheus-config-reloader.tar.gz
- prometheus-adapter.tar.gz
- node-exporter.tar.gz
- kube-rbac-proxy.tar.gz
- kube-metrics.tar.gz
- grafana.tar.gz
- configmap-reload.tar.gz
- alertmanager.tar.gz

注意：tab修改标签时，只需要修改服务器即可，禁止修改镜像原来的名称与标签。

```shell
[root@master ~]# docker load -i prometheus.tar.gz
[root@master ~]# docker images            #查看镜像的名称
[root@master ~]# docker tag  旧名称   192.168.1.100:5000/prometheus:v2.11.0
[root@master ~]# docker push  192.168.1.100:5000/prometheus:v2.11.0
[root@master ~]# docker load -i prometheus-operator.tar.gz
[root@master ~]# docker images            #查看镜像的名称
[root@master ~]# docker tag  \
旧名称  192.168.1.100:5000/prometheus-operator:v0.35.1
[root@master ~]# docker push  192.168.1.100:5000/prometheus-operator:v0.35.1
[root@master ~]# docker load -i prometheus-config-reloader.tar.gz
[root@master ~]# docker images            #查看镜像的名称
[root@master ~]# docker tag  \
旧名称  192.168.1.100:5000/prometheus-config-reloader:v0.35.1
[root@master ~]# docker push \
192.168.1.100:5000/prometheus-config-reloader:v0.35.1
[root@master ~]# docker load -i prometheus-adapter.tar.gz
[root@master ~]# docker images            #查看镜像的名称
[root@master ~]# docker tag  \
旧名称  192.168.1.100:5000/prometheus-operator:v0.35.1
[root@master ~]# docker push 192.168.1.100:5000/prometheus-operator:v0.35.1
[root@master ~]# docker load -i node-exporter.tar.gz
[root@master ~]# docker images            #查看镜像的名称
[root@master ~]# docker tag  \
旧名称  192.168.1.100:5000/node-exporter:v1.0.0
[root@master ~]# docker push 192.168.1.100:5000/node-exporter:v1.0.0
[root@master ~]# docker load -i kube-rbac-proxy.tar.gz
[root@master ~]# docker images            #查看镜像的名称
[root@master ~]# docker tag  \
旧名称  192.168.1.100:5000/kube-rbac-proxy:v0.4.1
[root@master ~]# docker push 192.168.1.100:5000/kube-rbac-proxy:v0.4.1
[root@master ~]# docker load -i kube-metrics.tar.gz
[root@master ~]# docker images            #查看镜像的名称
[root@master ~]# docker tag  \
旧名称  192.168.1.100:5000/kube-state-metrics:v1.9.2
[root@master ~]# docker push 192.168.1.100:5000/kube-state-metrics:v1.9.2
[root@master ~]# docker load -i alertmanager.tar.gz
[root@master ~]# docker images            #查看镜像的名称
[root@master ~]# docker tag  \
旧名称  192.168.1.100:5000/grafana:6.4.3
[root@master ~]# docker push 192.168.1.100:5000/grafana:6.4.3
[root@master ~]# docker load -i    configmap-reload.tar.gz
[root@master ~]# docker images            #查看镜像的名称
[root@master ~]# docker tag  \
旧名称  192.168.1.100:5000/configmap-reload:v0.3.0
[root@master ~]# docker push 192.168.1.100:5000/configmap-reload:v0.3.0
[root@master ~]# docker load -i    alertmanager.tar.gz
[root@master ~]# docker images            #查看镜像的名称
[root@master ~]# docker tag  \
旧名称  192.168.1.100:5000/alertmanager:v0.18.0
[root@master ~]# docker push 192.168.1.100:5000/alertmanager:v0.18.0
```

**步骤二：修改资源文件部署各种容器服务（在master主机操作操作）**

所有资源的素材文件都在云盘第四阶段kubernetes/v1.17.6/Prometheus/目录下。各位同学需要提前下载整个目录到master主机。

1）安装operator

需要修改资源文件，默认资源文件制定的是从官网下载镜像启动容器，我们需要修改为自己的192.168.1.100私有镜像仓库的路径。

```shell
[root@master prometheus]# vim setup/prometheus-operator-deployment.yaml
27  - --config-reloader-image=192.168.1.100:5000/configmap-reload:v0.3.0
28  - --prometheus-config-reloader=192.168.1.100:5000/prometheus-config-reloader:v0.35.1
29  image: 192.168.1.100:5000/prometheus-operator:v0.35.1
#提示：上面这些镜像的链接路径如果不知道，可以使用docker images查看。
[root@master prometheus]# kubectl apply -f setup/
```

2）安装Prometheus server

需要修改资源文件，默认资源文件制定的是从官网下载镜像启动容器，我们需要修改为自己的192.168.1.100私有镜像仓库的路径。

```shell
[root@master prometheus]# vim prom-server/prometheus-prometheus.yaml
14      baseImage: 192.168.1.100:5000/prometheus
34      version: v2.11.0
#提示：上面这些镜像的链接路径如果不知道，可以使用docker images查看。
[root@master prometheus]# kubectl apply -f prom-server/
```

3）安装prom-adapter

需要修改资源文件，默认资源文件制定的是从官网下载镜像启动容器，我们需要修改为自己的192.168.1.100私有镜像仓库的路径。

```shell
[root@master prometheus]# vim prom-adapter/prometheus-adapter-deployment.yaml
28         image: 192.168.1.100:5000/k8s-prometheus-adapter-amd64:v0.5.0
#提示：上面这些镜像的链接路径如果不知道，可以使用docker images查看。
[root@master prometheus]# kubectl apply -f prom-adapter/
```

4）安装metrics-state

需要修改资源文件，默认资源文件制定的是从官网下载镜像启动容器，我们需要修改为自己的192.168.1.100私有镜像仓库的路径。

```shell
[root@master prometheus]# vim metrics-state/kube-state-metrics-deployment.yaml
24            image: 192.168.1.100:5000/kube-rbac-proxy:v0.4.1
41            image: 192.168.1.100:5000/kube-rbac-proxy:v0.4.1
58            image: 192.168.1.100:5000/kube-state-metrics:v1.9.2
#提示：上面这些镜像的链接路径如果不知道，可以使用docker images查看。
[root@master prometheus]# kubectl apply -f metrics-state/
```

5）安装node-exporter

需要修改资源文件，默认资源文件制定的是从官网下载镜像启动容器，我们需要修改为自己的192.168.1.100私有镜像仓库的路径。

```shell
[root@master prometheus]# vim node-exporter/node-exporter-daemonset.yaml
27            image: 192.168.1.100:5000/node-exporter:v1.0.0
57            image: 192.168.1.100:5000/kube-rbac-proxy:v0.4.1
#提示：上面这些镜像的链接路径如果不知道，可以使用docker images查看。
[root@master prometheus]# kubectl apply -f node-exporter/
```

6）安装alertmanager

需要修改资源文件，默认资源文件制定的是从官网下载镜像启动容器，我们需要修改为自己的192.168.1.100私有镜像仓库的路径。

```shell
[root@master prometheus]# vim alertmanager/alertmanager-alertmanager.yaml
09     baseImage: 192.168.1.100:5000/alertmanager
18     version: v0.18.0
#提示：上面这些镜像的链接路径如果不知道，可以使用docker images查看。
[root@master prometheus]# kubectl apply -f alertmanager/
```

7）安装grafana

需要修改资源文件，默认资源文件制定的是从官网下载镜像启动容器，我们需要修改为自己的192.168.1.100私有镜像仓库的路径。

```shell
[root@master prometheus]# vim grafana/grafana-deployment.yaml
19    - image: 192.168.1.100:5000/grafana:6.4.3
#提示：上面这些镜像的链接路径如果不知道，可以使用docker images查看。
[root@master prometheus]# kubectl apply -f grafana/
```



# 3. 发布服务pometheus（二）

## 3.1 问题

本案例延续前面的案例3，继续部署pometheus，具体要求如下：

## 3.2 步骤

**步骤三：对外发布grafana服务（在master主机操作）**

相关资源文件共享在云盘第四阶段kubernetes/v1.17.6/prometheus/ grafana/grafana-service.yaml。

下面使用使用nodePort发布服务将容器的3000端口映射到真机节点的30000端口。

```shell
[root@master prometheus]# vim grafana/grafana-service.yaml
... ...
spec:
  type: NodePort
  ports:
  - name: http
    port: 3000
    nodePort: 30000
    targetPort: http
... ...
[root@master prometheus]# kubectl  apply  -f  grafana/grafana-service.yaml
```

使用浏览器访问任意节点的30002端口，即可访问到Web网页，效果如图-4所示。

![img](https://img-blog.csdnimg.cn/img_convert/bafd9cd31bc8d818f7b42145683ee4df.png)

图-4



# 4. 配置grafana

## 4.1 问题

本案例要求配置grafana，具体要求如下。

1. 配置数据源
2. 展示监控页面

## 4.2 步骤

实现此案例需要按照如下步骤进行。

**步骤一：配置grafana（在任意主机操作）**

1）登录

登录的默认用户和密码：admin/admin

第一次登录需要修改密码，效果如图-5所示。

![img](https://img-blog.csdnimg.cn/img_convert/906ef6fed6459a18fb71192fbbd506a3.png)

图-5

2）修改数据源地址

我们添加的数据为prometheus

数据源就是 Prometheus service 的地址

可以填写prometheus的Service内部的DNS名称

http://prometheus-k8s.monitoring.svc.cluster.local:9090

如何查看到这个DNS的域名呢？可以执行如下的命令即可。

```shell
[root@master ~]# kubectl -n monitoring get service
NAME               TYPE             CLUSTER-IP       EXTERNAL-IP    PORT(S)
grafana          NodePort       10.254.169.248        <none>         3000:30002/TCP
prometheus-k8s  NodePort       10.254.44.72    <none>              9090:30001/TCP
... ...
# 找到这里的prometheus-k8s名称后
# 在它的后面附加一个固定的monitoring.svc.cluster.local:9090
# 连接在一起就是：http://prometheus-k8s.monitoring.svc.cluster.local:9090
```

点击如图-6和图-7所示的按钮，修改数据源。

添加数据源Prometheus，名字随意，URL需要填写Prometheus内部的DNS名称，

默认端口号 9090。

![img](https://img-blog.csdnimg.cn/img_convert/a2e095d9cd4a1f2d2b5608e448921cc9.png)

图-6

![img](https://img-blog.csdnimg.cn/img_convert/2df52cfdff35dd5c27ae06098e5f0993.png)

图-7

3）导入模板

导入模板，需要正确配置后点击保存和测试后开始添加仪表盘

点开import，输入模板ID，效果如图-8所示。

![img](https://img-blog.csdnimg.cn/img_convert/69ecb2fdd8ff0c12b11fe3330513b01b.png)

图-8

常用的模块为315，如图-9所示。

![img](https://img-blog.csdnimg.cn/img_convert/d8f992662f272253af1800a8ba930b0c.png)

图-9

数据源就是刚刚定义的 Prometheus，如图-10所示。

![img](https://img-blog.csdnimg.cn/img_convert/33396cb1c9e586e6b143872c13a350bb.png)

图-10

最后查看监控效果，如图-11和图-12所示。



图-11



![img](https://img-blog.csdnimg.cn/img_convert/4348e84fbbfcbe882ad1bd24ed9f60a0.png)

图-12



# 5. HPA集群

## 5.1 问题

本案例利用监控指标实现HPA集群，具体要求如下。

1. 完成一个弹性集群

## 5.2 步骤

实现此案例需要按照如下步骤进行。

**步骤一：部署一个弹性集群（在master主机操作）**

1）查看、学习资源文件

```shell
[root@master ~]# vim myhpa.yaml 
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myweb
spec:
  selector:
    matchLabels:
      app: apache
  replicas: 1
  template:
    metadata:
      labels:
        app: apache
    spec:
      containers:
      - name: apache
        image: 192.168.1.100:5000/myos:httpd
        ports:
        - containerPort: 80
        resources:
          requests:
            cpu: 200m
      restartPolicy: Always
---
apiVersion: v1
kind: Service
metadata:
  name: web-service
spec:
  ports:
  - protocol: TCP
    port: 80
    targetPort: 80
  selector:
    app: apache
  type: ClusterIP
---
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: my-app
  annotations:
    kubernetes.io/ingress.class: "nginx"
spec:
  backend:
    serviceName: web-service
    servicePort: 80
---
apiVersion: autoscaling/v1
kind: HorizontalPodAutoscaler
metadata:
  name: myweb
spec:
  minReplicas: 1
  maxReplicas: 3
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myweb
  targetCPUUtilizationPercentage: 50
[root@master ~]# kubectl apply -f hpa-example.yaml
[root@master ~]# kubectl get hpa
NAME    REFERENCE          TARGETS   MINPODS   MAXPODS   REPLICAS   AGE
myweb   Deployment/myweb   0%/50%    1         3         1          15m
```

**步骤二：压力测试**

想办法对前面创建的容器进行压力测试，消耗容器CPU资源！！！

**步骤三：查看动态扩容效果**

```shell
[root@master ~]# kubectl get hpa 
NAME    REFERENCE          TARGETS    MINPODS   MAXPODS   REPLICAS   AGE
myweb  Deployment/myweb   287%/50%   1         3         3          16m
[root@master ~]# kubectl  get pod
NAME                     READY   STATUS    RESTARTS   AGE
myweb-7f89fc7b66-kzhj5   1/1     Running   0          16m
myweb-7f89fc7b66-nh4kn   1/1     Running   0          21s
myweb-7f89fc7b66-q2jnf   1/1     Running   0          21s
#当容器CPU占用过高时，集群可以自动扩容
-----------------------------------------------------------------------------
[root@master ~]# kubectl get hpa 
NAME    REFERENCE          TARGETS   MINPODS   MAXPODS   REPLICAS   AGE
myweb   Deployment/myweb   1%/50%    1         3         3          20m
[root@master ~]# kubectl  get pod
NAME                     READY   STATUS    RESTARTS   AGE
myweb-7f89fc7b66-kzhj5   1/1     Running   0          22m
# 当容器CPU占用率恢复正常时，容器可以自动缩减
```
> 如有侵权，请联系作者删除
