# Lamp API 文档

## 接口调用方式

通过 HTTP 协议访问接口, 接口的所有参数均使用 `utf-8` 编码, 返回数据均为 `json` 格式(含错误信息).

### 公共输入参数

* `app_id`: 产品应用的唯一标识(string, e.g. `agame`)
* `time_stamp`: 请求的标准时间戳(秒)
* `nonce`: 随机字符串
* `sign`: HTTP 请求的签名值, 参考 [签名算法](#签名算法)

### 公共输出参数

* `code`: 返回码. 0: 正确, 1: 错误. 有其他正常返回的输出参数时, 可省略.
* `msg`: `code` 非 0, 对应错误提示

文档中的示例 API, 在无异常情况和特殊说明时, 一律返回:

    {
        "code":0
    }

### 请求格式

    /sdk.91juice.com/app_id/v1/api?key_a=val_a&key_b=val_b&time_stamp=time_stamp&sign=sign_string

暂时只支持第一种, 不验证签名, 后续示例 URI 省略前缀 `/sdk.91juice.com/app_id/v1`.

## 常用术语

* `app_id`: 产品应用的唯一标识(string, e.g. `agame`)

* `time_stamp`: 请求的标准时间戳(秒)

* `sign`: HTTP 请求的签名值

* `platform`: 平台类型(string, e.g. `100`), 对应游戏区服允许登录的平台类型, 根据运营策略划分
  * `0`: 通用
  * `100`: 苹果测试
  * `200`: 安卓
  * `300`: 应用宝
  * `400`: 苹果官方

* `channel`: 发行渠道(string, e.g. `xiaomi`), 对应各发行渠道应用商店或接入 SDK 的代号
  * `xiaomi`: 小米
  * `360`: 奇虎 360
  * `1sdk`: 易接 SDK

* `server_type`: 服务器类型(string, e.g. `game`), 对应不同的服务端应用
  * `god`: 中心服务器
  * `data`: 数据库服务器, 服务器 ID 后缀为 `00`
  * `game`: 游戏逻辑服务器, 服务器 ID 后缀为 `01`
  * `gate`: 网关服务器, 服务器 ID 后缀为 `31`

* `server_group`: 服务器组 ID(string, e.g. `1001`), 同一应用下保证唯一

* `server_id`: 服务器 ID(string, e.g. `100131`), 由服务器组 ID 和服务器类型数字后缀拼接而成

----
## 运维

为运维人员提供主机, 区服管理功能.

### 添加/修改主机信息

    POST /operate/host

#### 输入参数:

* `host_id`: 主机 ID(string, e.g. `10000`)
* `brief`: 描述(string, e.g. `test`)
* `lan_ip`: 局域网 IP(string, e.g. `10.100.100.100`)
* `wan_ip`: 局域网 IP(string, e.g. `200.200.200.200`)

#### 输出参数:

* 无

#### 示例:

    POST /operate/host?host_id=10000&brief=test&lan_ip=10.100.100.1000&wan_ip=200.200.200.200

### 添加/修改区服信息

    POST /operate/server

#### 输入参数:

* `server_id`: 服务器 ID(string, e.g. `100101`)
* `name`: 服务器名称(string, e.g. `测试1服`)
* `type`: 服务器类型(string, e.g. `game`)
* `host_id`: 主机 ID(string, e.g. `10000`)
* `port`: 端口(int, e.g. `10101`)
* `platform`: 平台类型(string, e.g. `100`)
* `version`: 版本号(string, e.g. `1.0.0`)

#### 输出参数:

* 无

#### 示例:

    POST /operate/server?server_id=100101&name=测试1服&server_type=game&host_id=10000&port=10101&platform=100&version=1.0.0

### 添加/修改版本信息

    POST /operate/version

#### 输入参数:

* `version`: 版本(string, e.g. `1.0.0`)
* `branch`: 分支(string, e.g. `test`)
* `lan_ip`: 局域网 IP(string, e.g. `10.100.100.100`)
* `wan_ip`: 局域网 IP(string, e.g. `200.200.200.200`)

#### 输出参数:

* 无

#### 示例:

    POST /operate/host?host_id=10000&brief=test&lan_ip=10.100.100.100&wan_ip=200.200.200.200

### 添加/修改主机信息

    POST /operate/host

#### 输入参数:

* `host_id`: 主机 ID(string, e.g. `10000`)
* `brief`: 描述(string, e.g. `test`)
* `lan_ip`: 局域网 IP(string, e.g. `10.100.100.100`)
* `wan_ip`: 局域网 IP(string, e.g. `200.200.200.200`)

#### 输出参数:

* 无

#### 示例:

    POST /operate/host?host_id=10000&brief=test&lan_ip=10.100.100.1000&wan_ip=200.200.200.200

## 区服

### 获取主机列表

根据提供的参数查询并返回主机列表, 无参数时返回所有主机列表(仅供沙盒测试使用).

    GET /hosts

#### 输入参数:

* `host_id`: [可选] 主机 ID(string, e.g. `10000`)
* `brief`: [可选] 描述(string, e.g. `test`)
* `lan_ip`: [可选] 局域网 IP(string, e.g. `10.100.100.100`)
* `wan_ip`: [可选] 广域网 IP(string, e.g. `200.200.200.200`)

#### 输出参数:

* `hosts`: 主机列表
  * `id`: 主机 ID(string, e.g. `10000`)
  * `brief`: 描述(string, e.g. `test`)
  * `lan_ip`: 局域网 IP(string, e.g. `10.100.100.100`)
  * `wan_ip`: 广域网 IP(string, e.g. `200.200.200.200`)

#### 示例:

##### 获取指定主机信息:

    GET /hosts?id=10000

返回:

    {
        "host":[
        {
            "id":"10000",
            "brief":"test",
            "lan_ip":"10.100.100.100",
            "wan_ip":"200.200.200.200"
        }
        ]
    }

### 获取区服列表

根据提供的参数查询并返回服务器列表, 无参数时返回所有服务器列表(仅供沙盒测试使用).

    GET /servers

#### 输入参数:

* `server_id`: [可选] 服务器 ID(string, e.g. `100101`)
* `name`: [可选] 服务器名称(string, e.g. `测试1服`)
* `type`: [可选] 服务器类型(string, e.g. `game`)
* `host_id`: [可选] 主机 ID(string, e.g. `10000`)
* `port`: [可选] 端口(int, e.g. `10101`)
* `platform`: [可选] 平台类型(string, e.g. `100`)
* `version`: [可选] 版本号(string, e.g. `1.0.0`)

#### 输出参数:

* `servers`: 服务器列表
  * `id`: 服务器 ID(string, e.g. `100101`)
  * `name`: 服务器名称(string, e.g. `测试1服`)
  * `type`: 服务器类型(string, e.g. `game`)
  * `ip`: 广域网 IP(string, e.g. `200.200.200.200`)
  * `port`: 端口(int, e.g. `10101`)
  * `platform`: 平台类型(string, e.g. `100`)
  * `ver`: 版本号(string, e.g. `1.0.0`)
* `last_servers`: 最近登录服务器列表
  * `id`: 服务器 ID(string, e.g. `100101`)

#### 示例:

##### 给定平台和版本, 获取区服网关列表:

    GET /apps?type=gate&platform=100&verion=1.0.0

返回:

    {
        "app": [
        {
            "id":"100131",
            "name":"测试1服",
            "type":"gate",
            "ip":"200.200.200.200",
            "port":10101,
            "platform":"100",
            "ver":"1.0.0"
        },
        {
            "id":"100231",
            "name":"测试2服",
            "type":"gate",
            "ip":"200.200.200.200",
            "port":10201,
            "platform":"100",
            "ver":"1.0.0"
        }
        ]
        "last_servers": [
        "100101"
        ]
    }

## 查询

### 充值明细查询

根据提供的参数查询并返回充值明细.

    GET /detail/orders

#### 输入参数:

* `date_a`: 起始日期(string, e.g. `2016-01-01`), 默认为当前日期
* `date_b`: 截至日期(string, e.g. `2016-02-01`), 默认为当前日期
* `role_id`: [可选] 角色唯一 ID(string, e.g. `100100000000000001`)
* `platform`: [可选] 平台类型(string, e.g. `100`), 默认为所有平台
* `server_id`: [可选] 服务器 ID(string, e.g. `100101`), 默认为所有区服
* `channel`: [可选] 渠道(string, e.g. `baidu`), 默认为所有渠道

#### 输出参数:

* `orders`: 充值明细
  * `id`: 流水号(string, e.g. `10001`)
  * `cid`: 订单号(string, e.g. `100100000000000001`)
  * `user`: 账号(string, e.g. `zq.test`)
  * `rid`: 角色 ID(string, e.g. `100100000000000001`)
  * `lvl`: 等级(int, e.g. `10`)
  * `vip`: VIP(int, e.g. `1`)
  * `totaltime`: 累计在线时长(int, e.g. `10000`)
  * `price`: 充值金额(int, e.g. `100`)
  * `idx`: 充值项(int, e.g. `1`)
  * `num`: 充值份额(int, e.g. `1`)
  * `code`: 充值结果(int, e.g. `0`)
  * `server`: 服务器 ID(string, e.g. `100101`)
  * `req_time_s`: 请求时间(string, e.g. `2016-08-01 10:00:00`)
  * `res_time_s`: 响应时间(string, e.g. `2016-08-01 10:00:00`)

#### 示例:

    GET /detail/orders?server_id=100101&date_a=2016-09-01&date_b=2016-10-01

返回:

    {
        "orders": [
        {
            "id":"100100000000000001",
            "user":"zq.test",
            "name":"test",
            "server":"100101",
            "sid":"10001",
            "cls":"101",
            "lvl":10,
            "vip":1
        }
        ]
    }

## 用户

### 获取角色列表

根据提供的参数查询并返回角色列表, 无参数时返回所有角色列表(仅供沙盒测试使用).

    GET /roles

#### 输入参数:

* `role`: [可选] 角色唯一 ID, 角色短 ID, 角色名称, 账号名称
* `role_id`: [可选] 角色唯一 ID(string, e.g. `100100000000000001`)
* `user`: [可选] 账号(string, e.g. `zq.test`)
* `name`: [可选] 角色名称(string, e.g. `test`)
* `server_id`: [可选] 服务器 ID(string, e.g. `100101`)
* `short_id`: [可选] 角色短 ID(string, e.g. `10001`)
* `cls`: [可选] 职业(string, e.g. `101`)
* `lvl`: [可选] 等级(int, e.g. `10`)
* `vip`: [可选] VIP 等级(int, e.g. `1`)

#### 输出参数:

* `roles`: 角色列表
  * `id`: 角色唯一 ID(string, e.g. `100100000000000001`)
  * `user`: 账号(string, e.g. `zq.test`)
  * `name`: 角色名称(string, e.g. `test`)
  * `server_id`: 服务器 ID(string, e.g. `100101`)
  * `sid`: 短 ID(string, e.g. `10001`)
  * `cls`: 职业(string, e.g. `101`)
  * `lvl`: 等级(int, e.g. `10`)
  * `vip`: VIP 等级(int, e.g. `1`)
  * `combat`: 战斗力(int, e.g. `100000`)
  * `guild_id`: 公会 ID(string, e.g. `1001`)
  * `totaltime`: 累计在线时间(秒)(int, e.g. `10000`)
  * `createtime_s`: 创建时间(string, e.g. `2016-08-01 10:00:00`)
  * `entertime_s`: 上线时间(string, e.g. `2016-08-01 10:00:00`)
  * `leavetime_s`: 下线时间(string, e.g. `2016-08-01 10:00:00`), 为空时, 表示当前在线
  * `money_cur_a`: 当前持有游戏币(int, e.g. `10000`)
  * `money_cur_b`: 当前持有充值币(int, e.g. `10000`)
  * `money_cost_a`: 累计消耗游戏币(int, e.g. `10000`)
  * `money_cost_b`: 累计消耗充值币(int, e.g. `10000`)
  * `money_total_a`: 累计获取游戏币(int, e.g. `10000`)
  * `money_total_b`: 累计获取充值币(int, e.g. `10000`)
  * `money_charged`: 累计充值额度(int, e.g. `10000`)

#### 示例:

##### 根据区服和角色短 ID, 查询角色信息:

    GET /roles?server_id=100101&short_id=10001

返回:

    {
        "role": [
        {
            "id":"100100000000000001",
            "user":"zq.test",
            "name":"test",
            "server":"100101",
            "sid":"10001",
            "cls":"101",
            "lvl":10,
            "vip":1
        }
        ]
    }

##### 查询指定区服的角色列表:

    GET /roles?server_id=100101

### 获取角色道具列表

根据提供的参数查询并返回角色道具列表.

    GET /items

查询计数器:

    GET /counters

查询事件:

    GET /events

查询任务:

    GET /quests

查询关卡:

    GET /levels

#### 输入参数:

* `server_id`: 服务器 ID(string, e.g. `100101`)
* `role_id`: [可选] 角色唯一 ID(string, e.g. `100100000000000001`)
* `item_id`: [可选] 道具唯一 ID(string, e.g. `100101000000010001`)
* `role_name`: [可选] 角色名称(string, e.g. `test`)

#### 输出参数:

* `items`: 道具列表
  * `id`: 道具 ID(string, e.g. `100101000000010001`)
  * `idx`: 道具索引编号(int, e.g. `501001`)
  * `role`: 角色 ID(string, e.g. `100100000000000001`)
  * `stack`: 堆叠数量(int, e.g. `1000`)
  * `lvl`: 等级(int, e.g. `10`)
  * `star`: 星级(int, e.g. `10`)
  * `quality`: 品质(int, e.g. `10`)
  * `field`: 栏位(int, e.g. `10`), `0` 表示未装备
  * `stamp_s`: 道具变更时间(string, e.g. `2016-08-01 10:00:00`)

#### 示例:

根据角色 ID 查询:

    GET /items?server_id=100101&role_id=100100000000000001

根据道具 ID 查询:

    GET /items?server_id=100101&item_id=100101000000010001

根据角色名称查询:

    GET /items?server_id=100101&role_name=test

返回:

    {
        "item": [
        {
            "id":"100101000000010001",
            "idx":501001,
            "role":"100100000000000001",
            "stack":1000,
            "lvl":10,
            "star":10,
            "quality":10,
            "field":10,
            "stamp_s":"2016-08-01 10:00:00"
        }
        ]
    }

### 查询玩家操作日志

根据提供的参数查询并返回角色道具列表.

    GET /logs

#### 输入参数:

* `server_id`: 服务器 ID(string, e.g. `100101`)
* `role_id`: [可选] 角色唯一 ID(string, e.g. `100100000000000001`)
* `event`: [可选] 事件类型(int, e.g. `200101`), 参考 [事件类型](#事件类型)
* `stamp_a`: [可选] 起始时间(string, e.g. `2016-08-01 10:00:00`)
* `stamp_b`: [可选] 截止时间(string, e.g. `2016-08-01 10:00:00`)

#### 输出参数:

* `logs`: 日志列表
  * `id`: 事件 ID(string, e.g. `100101000000010001`)
  * `role_a`: 角色 A ID(string, e.g. `100100000000000001`)
  * `role_b`: 角色 B ID(string, e.g. `100100000000000001`)
  * `event`: 事件类型(int, e.g. `200101`), 参考 [事件类型](#事件类型)
  * `type`: 子类型(int, e.g. `1000`)
  * `idx`: 索引(int, e.g. `1000`)
  * `num`: 数量(int, e.g. `1000`)
  * `delta`: 变化量(int, e.g. `1000`)
  * `status`: 状态(int, e.g. `1000`)
  * `arg_64`: 64 位参数(int64, e.g. `1000`)
  * `arg_str`: 字符串参数(int64, e.g. `test`)
  * `arg_a`: 32 位参数 A(int64, e.g. `1000`)
  * `arg_b`: 32 位参数 B(int64, e.g. `1000`)
  * `stamp_s`: 道具变更时间(string, e.g. `2016-08-01 10:00:00`)

#### 示例:

根据角色 ID 查询:

    GET /items?server_id=100101&role_id=100100000000000001

根据道具 ID 查询:

    GET /items?server_id=100101&item_id=100101000000010001

根据角色名称查询:

    GET /items?server_id=100101&role_name=test

返回:

    {
        "item": [
        {
            "id":"100101000000010001",
            "idx":501001,
            "role":"100100000000000001",
            "stack":1000,
            "lvl":10,
            "star":10,
            "quality":10,
            "field":10,
            "stamp_s":"2016-08-01 10:00:00"
        }
        ]
    }

## GM 指令

### 发送邮件

    POST /gm/add_mail

#### 输入参数:

* `oid`: 操作者 ID(string, e.g. `gm_001`)
* `from_name`: [可选] 发送者(string, e.g. `系统`)
* `to_name`: [可选] 接收者(string, e.g. `测试`)
* `type`: 邮件类型(int, e.g. `10001`), 参考 [邮件类型](#邮件类型)
* `title`: 标题(string, e.g. `test`)
* `data`: 内容(string, e.g. `test`)
* `lvl`: [可选] 等级限制(int, e.g. `10`), 非 0 时, 大于等于该等级的玩家可以收到该邮件
* `vip`: [可选] VIP 等级限制(int, e.g. `1`), 非 0 时, VIP 大于等于该等级的玩家可以收到该邮件
* `expired`: [可选] 有效时间(秒), 缺省值 `0`: 永久有效
* `idx_a`: [可选] 附件道具 A(int, e.g. `501001`)
* `num_a`: [可选] 附件道具 A 数量(int, e.g. `1000`)
* `idx_b`: [可选] 附件道具 B(int, e.g. `501001`)
* `num_b`: [可选] 附件道具 B 数量(int, e.g. `1000`)
* `group_idx`: [可选] 附件道具组(int, e.g. `501001`)
* `group_num`: [可选] 附件道具组数量(int, e.g. `1`)
* `server_id`: [可选] 服务器 ID(string, e.g. `100101`), 缺省值 `0`: 广播到所有区服

#### 示例:

注意: 如需定时/循环发布, 需外部逻辑实现. 不指定 `server_id` 时, 将广播到所有区服, 如需指定多个区服, 可发送多个 HTTP 请求实现.

    POST /gm/add_mail?oid=gm_001&type=10001&title=test&data=hello,world

### 触发事件

大多数 GM 指令均通过事件方式触发.

    POST /gm/trigger_event

#### 输入参数:

* `oid`: 操作者 ID(string, e.g. `gm_001`)
* `event`: 事件类型(int, e.g. `200101`), 参考 [事件类型](#事件类型)
* `arg_a`: [可选] 整型参数 A(int, e.g. `501001`)
* `arg_b`: [可选] 整型参数 B(int, e.g. `1000`)
* `str_a`: [可选] 字符串参数 A(string, e.g. `hello`)
* `str_b`: [可选] 字符串参数 B(string, e.g. `world`)
* `server_id`: [可选] 服务器 ID(string, e.g. `100101`), 缺省值 `0`: 广播到所有区服

#### 示例:

##### 添加黑白名单(900002):

* `event`: `900002`
* `arg_a`: 黑白名单权限, 通过位运算进行权限组合
  * `0x0001`: 特权账号(1)
  * `0x0002`: 调试登录(2)
  * `0x0010`: 开放登录(16)
  * `0x1000`: 封停账号(4096)
  * `0x2000`: 禁言账号(8192)
* `arg_b`: 有效时间(秒), 缺省值 `0`: 永久有效
* `str_a`: 渠道(出于安全考虑, 不对外开放使用)
* `str_b`: 账号
* `server_id`: 不设置. 为了方便操作, 黑白名单对所有区服有效

注意: 黑白名单的作用对象为 **账号** 而非 **角色**.

    POST /gm/trigger_event?oid=gm_001&event=900002&arg_a=17&str_b=zq.test

##### 添加道具(200101):

* `event`: `200101`
* `arg_a`: 道具 ID
* `arg_b`: 道具数量
* `str_b`: 角色名称
* `server_id`: 角色所在区服 ID

示例:

    POST /gm/trigger_event?oid=gm_001&event=200101&arg_a=501001&arg_b=10000&str_b=测试&server_id=100101

##### 修改计数器(600103):

* `event`: `600103`
* `arg_a`: 计数器 ID
* `arg_b`: 数值
* `str_b`: 角色名称
* `server_id`: 角色所在区服 ID

示例:

    POST /gm/trigger_event?oid=gm_001&event=600103&arg_a=10000&arg_b=1&str_b=测试&server_id=100101

##### 添加任务(210101):

* `event`: `210101`
* `arg_a`: 任务 ID
* `str_b`: 角色名称
* `server_id`: 角色所在区服 ID

示例:

    POST /gm/trigger_event?oid=gm_001&event=210101&arg_a=100001&str_b=测试&server_id=100101

##### 设置任务状态(200103):

* `event`: `210103`
* `arg_a`: 任务 ID
* `arg_b`: 任务状态
  * `2`: 已接(任务已接, 尚未完成)
  * `3`: 成功(任务成功, 尚未领取奖励)
  * `5`: 完成(任务完成, 且已领取奖励)
* `str_b`: 角色名称
* `server_id`: 角色所在区服 ID

示例:

    POST /gm/trigger_event?oid=gm_001&event=200103&arg_a=100001&arg_b=3&str_b=测试&server_id=100101

##### 重新加载角色(900101):

* `event`: `900101`
* `str_b`: 角色名称
* `server_id`: 角色所在区服 ID

示例:

    POST /gm/trigger_event?oid=gm_001&event=900101&str_b=测试&server_id=100101

##### 恢复角色(900202):

* `event`: `900202`
* `str_b`: 角色名称
* `server_id`: 角色所在区服 ID

示例:

    POST /gm/trigger_event?oid=gm_001&event=900202&str_b=测试&server_id=100101

##### 清除通天塔数据(900010):

* `event`: `900010`
* `str_b`: 角色名称
* `server_id`: 角色所在区服 ID

示例:

    POST /gm/trigger_event?oid=gm_001&event=900010&str_b=测试&server_id=100101

##### 发布跑马灯:

* `event`: `900003`
* `str_a`: 跑马灯内容

在游戏内以跑马灯形式发布公告.

注意: 如需定时/循环发布, 需外部逻辑实现. 不指定 `server_id` 时, 将广播到所有区服, 如需指定多个区服, 可发送多个 HTTP 请求实现.

    POST /gm/trigger_event?oid=gm_001&event=900003&str_a=hello,world

### 留存数据

    POST /stat/retention

#### 输入参数:

* `date_a`: 起始日期(string, e.g. `2016-01-01`), 默认为当前日期
* `date_b`: 截至日期(string, e.g. `2016-02-01`), 默认为当前日期
* `platform`: [可选] 平台类型(string, e.g. `100`), 默认为所有平台
* `server_id`: [可选] 服务器 ID(string, e.g. `100101`), 默认为所有区服
* `channel`: [可选] 渠道(string, e.g. `baidu`), 默认为所有渠道

#### 输出参数:

* 无

#### 示例:

    POST /stat/retention?platform=100&server_id=100101&version=1.0.0

----

----

## 参考

### 事件类型

针对角色:

* `900002`: 添加黑白名单
* `103001`: 发送邮件
* `200101`: 添加道具
* `600103`: 修改计数器
* `210101`: 添加任务
* `210103`: 设置任务状态
* `900101`: 重新加载角色
* `900202`: 恢复角色
* `900010`: 清除通天塔数据

针对区服:

* `900003`: 发布跑马灯

### 签名算法

对请求的 URI 路径进行 URL 编码(记为 `uri_a`), 将除 `sign` 外的所有参数按 key 进行字典升序排列(记为 `uri_b`). 将 HTTP 请求方式(method: `GET`/`POST`)以及 `uri_a`, `uri_b` 用 `&` 拼接构成源串, 用 `app_key` 对源串散列(HMAC-SHA1)后经 Base64 编码得到签名值
