## 流程

- 事件源发布事件消息

```sh
curl -l -H "Content-type: application/json" -X POST -d '{"event":"EVENT_ITEM_ADD","arg_a":501001,"arg_b":10000,"arg_64":$long_id,"arg_str":""}' http://yulefox.com:4151/pub?topic=gm
```
- NSQ 集群广播消息

- NSQ 客户端接收并处理消息, 转发给游戏服务进行逻辑处理