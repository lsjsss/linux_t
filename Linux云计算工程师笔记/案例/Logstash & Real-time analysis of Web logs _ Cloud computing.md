@[TOC]( Logstash & Real-time analysis of Web logs | Cloud computing )

---

# 1. 安装Logstash

## 1.1 问题

本案例要求：

- 创建虚拟机并安装 logstash
- 最低配置： 2cpu，2G内存，10G硬盘
- 虚拟机IP： 192.168.1.47 logstash

## 1.2 步骤

实现此案例需要按照如下步骤进行。

**步骤一：安装logstash**

1）配置主机名，ip和yum源，配置/etc/hosts

```shell
[root@logstash ~]# vim /etc/hosts
192.168.1.41    es-0001
192.168.1.42    es-0002
192.168.1.43    es-0003
192.168.1.44    es-0004
192.168.1.45    es-0005
192.168.1.46    kibana
192.168.1.47    logstash
```

2）安装java-1.8.0-openjdk和logstash

```shell
[root@logstash ~]# yum -y install java-1.8.0-openjdk logstash
[root@logstash ~]# java -version
openjdk version "1.8.0_161"
OpenJDK Runtime Environment (build 1.8.0_161-b14)
OpenJDK 64-Bit Server VM (build 25.161-b14, mixed mode)
[root@logstash ~]# ln -s /etc/logstash /usr/share/logstash/config 
[root@logstash ~]# vim /etc/logstash/conf.d/my.conf
input { 
  stdin {}
}
filter{ }
output{ 
  stdout{}
}
[root@logstash ~]# /usr/share/logstash/bin/logstash
```



# 2. 编写logstash配置文件

## 2.1 问题

本案例要求：

- 编写 logstash 配置文件
- 标准输入采用 json 编码格式
- 标准输出采用 rubydebug 编码格式
- 启动 logstash 验证

## 2.2 步骤

实现此案例需要按照如下步骤进行。

**步骤一：codec类插件**

1）codec类插件

```shell
[root@logstash ~]# vim /etc/logstash/conf.d/my.conf
input { 
  stdin { codec => "json" }
}
filter{ }
output{ 
  stdout{ codec => "rubydebug" }
}
[root@logstash ~]# /usr/share/logstash/bin/logstash
Settings: Default pipeline workers: 2
Pipeline main started
a
{
       "message" => "a",
           "tags" => [
          [0] "_jsonparsefailure"
],
      "@version" => "1",
    "@timestamp" => "2020-05-23T12:34:51.250Z",
          "host" => "logstash"
}
```



# 3. Logstash input插件

## 3.1 问题

本案例要求：

- 编写 logstash 配置文件
- 从文件中读取数据，并在屏幕显示
- 启动 logstash 验证

## 3.2 步骤

实现此案例需要按照如下步骤进行。

**步骤一：file模块插件**

1）file模块插件

```shell
[root@logstash ~]# vim /etc/logstash/conf.d/my.conf
input { 
  file {
    path => ["/tmp/c.log"]
    type => "test"
    start_position => "beginning"
    sincedb_path => "/var/lib/logstash/sincedb"
  }
}
filter{ }
output{ 
  stdout{ codec => "rubydebug" }
}
[root@logstash ~]# rm -rf /var/lib/logstash/plugins/inputs/file/.sincedb_*
[root@logstash ~]# touch /tmp/a.log /tmp/b.log
[root@logstash ~]# /usr/share/logstash/bin/logstash
```

另开一个终端：写入数据

```shell
[root@logstash ~]#  echo a1 >> /tmp/a.log 
[root@logstash ~]#  echo b1 >> /var/tmp/b.log
```

之前终端查看：

```shell
[root@logstash ~]# /usr/share/logstash/bin/logstash
Settings: Default pipeline workers: 2
Pipeline main started
{
       "message" => "a1",
      "@version" => "1",
    "@timestamp" => "2019-03-12T03:40:24.111Z",
          "path" => "/tmp/a.log",
          "host" => "logstash",
          "type" => "testlog"
}
{
       "message" => "b1",
      "@version" => "1",
    "@timestamp" => "2019-03-12T03:40:49.167Z",
          "path" => "/tmp/b.log",
          "host" => "logstash",
          "type" => "testlog"
}
```



# 4. Web日志解析实验

## 4.1 问题

本案例要求：

- Web日志解析实验
- 复制一条 web 日志添加到文件中
- 使用 grok 匹配出日志的各个字段含义转化成 json 格式

## 4.2 步骤

实现此案例需要按照如下步骤进行。

**步骤一：filter grok模块插件**

grok插件：

解析各种非结构化的日志数据插件

grok使用正则表达式把飞结构化的数据结构化

在分组匹配，正则表达式需要根据具体数据结构编写

虽然编写困难，但适用性极广

解析Apache的日志，之前已经安装过的可以不用安装

浏览器访问网页，在/var/log/httpd/access_log有日志出现

```shell
[root@es-0005 ~]# cat /var/log/httpd/access_log
192.168.1.254 - - [12/Mar/2019:11:51:31 +0800] "GET /favicon.ico HTTP/1.1" 404 209 "-" "Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0"
[root@logstash ~]#  vim /etc/logstash/logstash.conf
input{
    file {
      path           => [ "/tmp/a.log", "/tmp/b.log" ]
      sincedb_path   => "/var/lib/logstash/sincedb"
      start_position => "beginning"
      type           => "testlog"
   }
}
filter{
    grok{
       match => [ "message",  "(?<key>reg)" ]
    }
}
output{
    stdout{ codec => "rubydebug" }
}
```

复制/var/log/httpd/access_log的日志到logstash下的/tmp/c.log

```shell
[root@logstash ~]# echo '192.168.1.252 - - [29/Jul/2020:14:06:57 +0800] "GET /info.html HTTP/1.1" 200 119 "-" "curl/7.29.0"' >/tmp/c.log
[root@logstash ~]# vim /etc/logstash/conf.d/my.conf
input { 
  file {
    path => ["/tmp/c.log"]
    type => "test"
    start_position => "beginning"
    sincedb_path => "/dev/null"
  }
}
filter{ 
  grok {
    match => { "message" => "%{HTTPD_COMBINEDLOG}" }
  }
}
output{ 
  stdout{ codec => "rubydebug" }
}
[root@logstash ~]# /usr/share/logstash/bin/logstash
```

查找正则宏路径

```shell
[root@logstash ~]# cd 
/usr/share/logstash/vendor/bundle/jruby/2.5.0/gems/logstash-patterns-core-4.1.2/patterns
[root@logstash ~]# cat httpd  //查找COMBINEDAPACHELOG
COMBINEDAPACHELOG %{COMMONAPACHELOG} %{QS:referrer} %{QS:agent}
[root@logstash ~]#  vim /etc/logstash/logstash.conf
...
filter{
   grok{
        match => ["message", "%{ HTTPD_COMBINEDLOG }"]
  }
}
...
```

解析出的结果

```shell
 [root@logstash ~]#  /opt/logstash/bin/logstash -f  /etc/logstash/logstash.conf  
Settings: Default pipeline workers: 2
Pipeline main started
{
        "message" => "192.168.1.254 - - [15/Sep/2018:18:25:46 +0800] \"GET /noindex/css/open-sans.css HTTP/1.1\" 200 5081 \"http://192.168.1.65/\" \"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0\"",
       "@version" => "1",
     "@timestamp" => "2018-09-15T10:55:57.743Z",
           "path" => "/tmp/a.log",
ZZ           "host" => "logstash",
           "type" => "testlog",
       "clientip" => "192.168.1.254",
          "ident" => "-",
           "auth" => "-",
      "timestamp" => "15/Sep/2019:18:25:46 +0800",
           "verb" => "GET",
        "request" => "/noindex/css/open-sans.css",
    "httpversion" => "1.1",
       "response" => "200",
          "bytes" => "5081",
       "referrer" => "\"http://192.168.1.65/\"",
          "agent" => "\"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0\""
}
...
```



# 5. 部署beats与filebeat

## 5.1 问题

本案例要求：

- 打通ELK全流程
- 在 logstash 上安装配置 beats 插件
- web 服务器上安装 filebeat
- 使用 filebeat 收集 web 日志，并发送给 logstash
- 将日志转化为json格式存入elasticsearch

## 5.2 步骤

实现此案例需要按照如下步骤进行。

**步骤一：filter grok模块插件**

```shell
[root@logstash ~]# vim /etc/logstash/conf.d/my.conf
input { 
  stdin { codec => "json" }
  file{
    path => ["/tmp/c.log"]
    type => "test"
    start_position => "beginning"
    sincedb_path => "/var/lib/logstash/sincedb"
  }
  beats {
    port => 5044
  }
} 
filter{ 
  grok {
    match => { "message" => "%{HTTPD_COMBINEDLOG}" }
  }
} 
output{ 
  stdout{ codec => "rubydebug" }
  elasticsearch {
    hosts => ["es-0004:9200", "es-0005:9200"]
    index => "weblog-%{+YYYY.MM.dd}"
  }
}
[root@logstash ~]# /usr/share/logstash/bin/logstash
```

2）在之前安装了Apache的主机上面安装filebeat

```shell
[root@web ~]# yum install -y filebeat
[root@web ~]# vim /etc/filebeat/filebeat.yml
24:  enabled: true
28:  - /var/log/httpd/access_log
45:    fields: 
46:       my_type: apache
148, 150 注释掉
161: output.logstash:
163:   hosts: ["192.168.1.47:5044"]
180, 181, 182 注释掉
[root@web ~]# grep -Pv "^\s*(#|$)" /etc/filebeat/filebeat.yml
[root@web ~]# systemctl enable --now filebeat
```



# Exercise

## 1 什么是kibana

数据可视化平台工具

## 2 Logstash插件有哪些

codec类插件、file插件、tcp和udp插件、syslog插件、filter grok插件



> 如有侵权，请联系作者删除
