# 设计思路

## 特点

* 基于 HTTP 协议进行应用间的通信

* 耦合度低

* 使用签名, 安全性高

## 功能

* 服务器区服管理

  - 查询: 从数据库中查询服务器区服信息 

  - 操作: 修改/添加/删除服务器区服信息

## 依赖

* [labstack/echo](https://github.com/labstack/echo)
* [go-sql-driver/mysql](https://github.com/go-sql-driver/mysql)

echo 实现路由解析, mysql 实现数据库, 


----

测试驱动

游戏服务器区服信息集中管理.

MD5 验证更新结果.

----
## 功能

### 添加主机

### 获取服务器列表

### 生成服务器配置

xml

/config/:server_id

### 日志

ELK 是一个用于日志分析的开源的完整的技术栈. 由三部分组成:

* Elasticsearch: Search and analyze data in real time.

* Logstash: Collect, enrich, and transport data.

* Kibana: Explore and visualize your data.

#### Logstash

[Logstash](https://download.elastic.co/logstash/logstash/logstash-2.3.4.tar.gz) 负责收集, 整理, 传输日志, [文档](https://www.elastic.co/guide/en/logstash/current/index.html).

    wget https://download.elastic.co/logstash/logstash/logstash-2.3.4.tar.gz
    tar -xf logstash-2.3.4.tar.gz

日志类型:

* 系统日志: 软硬件资源, 性能, 安全日志
* 应用日志: 业务逻辑日志

[Filebeat](https://github.com/elastic/beats/tree/master/filebeat)


Getting Started with Beats and the Elastic Stackedit

Looking for an "ELK tutorial" that shows how to set up the Elastic stack for Beats? You’ve come to the right place. The topics in this section describe how to install and configure the Elastic stack for Beats.

A regular Beats setup consists of:

* One or more Beats. You install the Beats on your servers to capture operational data.
* Elasticsearch for storage and indexing. See Installing Elasticsearch.
* Logstash (optional) for inserting data into Elasticsearch. See Installing Logstash.
* Kibana for the UI. See Installing Kibana.
* Kibana dashboards for visualizing the data. See Loading the Beats Dashboards.

See the Elastic Support Matrix for information about supported operating systems and product compatibility.

