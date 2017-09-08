# 数据分析

ELK 是一个用于日志分析的开源的完整的技术栈. 由三部分组成:

* Elasticsearch: Search and analyze data in real time.

* Logstash: Collect, enrich, and transport data.

* Kibana: Explore and visualize your data.

## Logstash

[Logstash](https://download.elastic.co/logstash/logstash/logstash-2.3.4.tar.gz) 负责收集, 整理, 传输日志, [文档](https://www.elastic.co/guide/en/logstash/current/index.html).

    wget https://download.elastic.co/logstash/logstash/logstash-2.3.4.tar.gz
    tar -xf logstash-2.3.4.tar.gz

日志类型:

* 系统日志: 软硬件资源, 性能, 安全日志
* 应用日志: 业务逻辑日志

## FileBeat

[FileBeat](https://github.com/elastic/beats/tree/master/filebeat)


Getting Started with Beats and the Elastic Stackedit

Looking for an "ELK tutorial" that shows how to set up the Elastic stack for Beats? You’ve come to the right place. The topics in this section describe how to install and configure the Elastic stack for Beats.

A regular Beats setup consists of:

* One or more Beats. You install the Beats on your servers to capture operational data.
* Elasticsearch for storage and indexing. See Installing Elasticsearch.
* Logstash (optional) for inserting data into Elasticsearch. See Installing Logstash.
* Kibana for the UI. See Installing Kibana.
* Kibana dashboards for visualizing the data. See Loading the Beats Dashboards.

See the Elastic Support Matrix for information about supported operating systems and product compatibility.

### 安装

    curl -L -O https://download.elastic.co/beats/filebeat/filebeat-1.2.3-x86_64.rpm
    #curl -L -O http://god.91juice.com:8081/download/elk/filebeat-1.2.3-x86_64.rpm
    sudo rpm -vi filebeat-1.2.3-x86_64.rpm
    sudo systemctl enable filebeat.service
    sudo systemctl start filebeat.service
    sudo systemctl status filebeat.service

`/etc/filebeat/filebeat.yml` 配置如下:

    filebeat:
      prospectors:
        -
          paths:
            - /var/log/*.log
            - /juice/agame/deploy/bin/*/log/*
            - /juice/agame/deploy/bin/*/log/events/*
          encoding: utf-8
          input_type: log
      registry_file: /var/lib/filebeat/registry
    output:
      elasticsearch:
        hosts: ["sdk.91juice.com:9200", "test.91juice.com:9200"]
    shipper:
    logging:
      files:
        rotateeverybytes: 10485760 # = 10MB

## Elasticsearch

Elasticsearch 索引的对象是 JSON 文档, 下面是 Elasticsearch 中的一些概念跟关系型数据库的相关对照:

    Relational DB -> Databases -> Tables -> Rows -> Columns
    Elasticsearch -> Indices   -> Types  -> Documents -> Fields 

### 安装

[Elasticsearch](https://www.elastic.co/downloads/elasticsearch) 的运行, 依赖 java. Elasticsearch 集群的作用主要是提高稳定性, 节点生产环境搭建脚本示例:

    #!/bin/sh
    yum install -y java | java -version
    curl -L -O https://download.elastic.co/elasticsearch/release/org/elasticsearch/distribution/rpm/elasticsearch/2.3.4/elasticsearch-2.3.4.rpm
    #curl -L -O http://god.91juice.com:8081/download/elk/elasticsearch-2.3.4.rpm
    curl -L -O http://god.91juice.com:8081/download/elk/elasticsearch.yml.tmpl
    rpm -vi elasticsearch-2.3.4.rpm
    sed -i "s/^node\.name.*$/node.name: ${HOSTNAME}/" elasticsearch.yml.tmpl
    mkdir -p /juice/elk/data | mkdir -p /juice/elk/log
    chown -R elasticsearch:elasticsearch /juice/elk
    mv -f elasticsearch.yml.tmpl /etc/elasticsearch/elasticsearch.yml
    chmod 750 /etc/elasticsearch/elasticsearch.yml
    chown root:elasticsearch /etc/elasticsearch/elasticsearch.yml
    systemctl daemon-reload
    systemctl enable elasticsearch.service
    systemctl restart elasticsearch.service
    systemctl status elasticsearch.service

`/etc/elasticsearch/elasticsearch.yml` 配置如下:

    cluster.name: juice
    node.name: ${HOSTNAME}
    node.rack: r1
    path.data: /juice/elk/data
    path.logs: /juice/elk/logs
    network.host: 0.0.0.0
    network.publish_host: 0.0.0.0
    discovery.zen.ping.unicast.hosts: ["sdk.91juice.com"]

## Kibana

    curl -L -O https://download.elastic.co/kibana/kibana/kibana-4.5.3-1.x86_64.rpm
    sudo rpm -vi kibana-4.5.3-1.x86_64.rpm
    sudo systemctl start kibana.service
    sudo systemctl status kibana.service

## Marvel

Marvel 是 Elasticsearch/Kibana 的管理和监控工具:

    sudo /usr/share/elasticsearch/bin/plugin install license
    sudo /usr/share/elasticsearch/bin/plugin install marvel-agent
    sudo /opt/kibana/bin/kibana plugin --install elasticsearch/marvel/latest

## Sense

Sense 是一个交互式控制台, 使用户方便的通过浏览器直接与 Elasticsearch 进行交互:

    sudo /opt/kibana/bin/kibana plugin --install elastic/sense

    GET filebeat-2016.07.20/_search
    {
      "query": {
        "bool": {
          "must": [
            { "match": { "source": "_data/log/events" } },
            { "match": {
                "message": {
                  "query": "120011469035500062 600301",
                  "operator": "and"
                }
            }
          ]
        }
      },
      "highlight": {
        "fields" : {
          "message" : {}
        }
      }
    }


## 应用

ELK  生产环境的拓扑结构如下:

        Raw Log +--> FileBeat +--+
                                 |
        Raw Log +--> FileBeat +--+
                                 +--> Elasticsearch +--> Kibana
        Raw Log +--> FileBeat +--+
                                 |
        Raw Log +--> FileBeat +--+

* Raw Log: 各节点服务器上的原始日志
* FileBeat: 将原始日志上发到 Elasticsearch
* Elasticsearch: 对日志文件进行索引, 提供查询
* Kibana: 向用户提供统一界面

## 模式

* 付费测试前免费, 从付费测试开始, 按月付费
* 专线专服

## 特性

* 极简的 API
* 无 SDK 
* 宕机分析(需接入 SDK 库)

## 压力

* 需承受较大压力
