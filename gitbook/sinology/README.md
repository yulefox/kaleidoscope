## CLI

通过 CLI 整合子命令, 将 Lamp 打造成一个完整生态.

- `dashboard` 后台仪表盘

- `spanner` 扳手: 发送命令

- `log` 各种日志


## 流程

- 生产者发布消息

常见的生产者应用场景: 用户通过浏览器从前端投递消息(Node.js).

```sh
curl -l -H "Content-type: application/json" -X POST -d '{"event":"EVENT_ITEM_ADD","arg_a":501001,"arg_b":10000,"arg_64":$long_id,"arg_str":""}' http://yulefox.com:4151/pub?topic=gm
```

消息经 `nsqd` 发布, 等待消费者处理.

- 消费者处理消息 

  - NSQ 客户端接收并处理消息, 转发给游戏服务进行逻辑处理.
  - 生产者等待处理结果, 需要借助 `channel` 实现.



