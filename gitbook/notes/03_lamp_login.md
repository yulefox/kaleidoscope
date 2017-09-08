# 登录

----

## 更新日志

### 2016-11-17

* `[ADD]` 登录流程

----

## 登录

### `lamp SDK`

`lamp SDK` 负责处理所有独立于游戏服务的通用逻辑:

* 账户验证
* 充值
* 用户信息记录及统计, 分析
* 客户端事件记录及统计, 分析

### 登录验证

用户登录验证(`lamp SDK`)服务独立于游戏服务(`Game Servers`).

### 登录流程

            client      +           gate           +           game           +       data
                        |                          |                          |
                        |                          |                          |
                        | * login authentication   |                          |
                        | * bind user              |                          |
    +-----------+       | * set game server        |                          |
    | Login.Req +------->                          |                          |
    +-----------+       |   forward Login.Req      |                          | * load user info
                        +-------------------------->                          |
                        |                          |   forward Login.Req      |
                        |                          +-------------------------->
                        |                          |                          |
                        |                          |                          |
                        |                          | * update user info       |
                        |                          |                          |
                        | * update user info       <--------------------------+
                        |                          |                          |
                        <--------------------------+                          |
    +-----------+       |                          |                          |
    | Login.Res <-------+                          |                          |
    +-----------+       |                          |                          |
                        |                          |                          |
                        |                          |                          |
                        +                          +                          +

* 游戏客户端(`client`)经第三方或 `lamp SDK` 获取账户信息并提交 `lamp SDK` 验证, 除第三方验证必须的 `toker` 等账户信息外, 还须提供设备信息等. 

* `lamp SDK` 经第三方验证通过后, 将用户信息封装(`json`, 供游戏服务使用)后返回给游戏客户端.

* 游戏客户端将 `lamp SDK` 返回的用户信息(不可更改)提交到网关服务器(`gate`), 并指定游戏区服(`Login.Req:server`), 登录游戏(`Login.Req`).

* 网关服务器(`gate`)根据用户信息校验用户数据的合法性, 校验通过后, 通知游戏服务器(`game`).

* 游戏服务器(`game`)经数据服务器(`data`)加载游戏数据, 经网关服务器回传给客户端, 完成登录流程.

### 断开连接



### 断线重连

断线重连与正常登录流程基本相同, 唯一区别在于:

* `Login.Req` 不指定游戏区服, 网关服务器根据用户上次选择游戏服务器完成登录流程.

* 网关服务器(`gate`)无法获取上次选择游戏服务器时, 返回对应错误码, 客户端指定游戏区服重新登录.

### 挤掉其他终端

* 网关服务器(`gate`)检测到用户(`GUser`)已在其他终端 A(`Peer A`)登录时, 将解除已登录终端与用户的绑定, 并重新绑定用户到新终端 B(`Peer B`).

* 网关服务器(`gate`)收到终端 A(`Peer A`)的新请求时, 将拒绝新请求并通知其被挤掉的对应错误码.

* 终端A(`Peer A`)对应客户端应主动断开连接, 或发起断线重连的请求.

* 网关服务器(`gate`)会定时关闭超时未绑定用户的连接.

### 退出流程

* 客户端(`client`)可在游戏中主动退出: 发送 `Logout.Req` 或直接断开网络连接.

* 网关服务器(`gate`)收到 `Logout.Req` 请求时, 将解除客户端(`client`)对应终端(`Peer`)与用户的绑定.

* 网关服务器(`gate`)收到 `Fini.Req`(网络连接断开时触发) 请求时, 亦将解除客户端(`client`)对应终端(`Peer`)与用户的绑定.

## 绑定/通信

用户登录成功后绑定映射(`peer`, `server`, `uid`):

    elf::Object::SetChild(uid,      entity::OBJECT_SERVER,      server);
    elf::Object::AddChild(server,   entity::OBJECT_USER,        uid);

    elf::Object::SetChild(uid,      entity::OBJECT_PEER,        peer);
    elf::Object::SetChild(peer,     entity::OBJECT_USER,        uid);
    elf::Object::SetChild(peer,     entity::OBJECT_CODE,        entity::RC_OK);

用户连接断开或逻辑断开(被踢下线)解绑映射:

    elf::Object::SetChild(uid,      entity::OBJECT_SERVER,      0);
    elf::Object::DelChild(server,   entity::OBJECT_USER,        uid);

    elf::Object::SetChild(uid,      entity::OBJECT_PEER,        elf::OID_NIL);
    elf::Object::SetChild(peer,     entity::OBJECT_USER,        elf::OID_NIL);
    elf::Object::SetChild(peer,     entity::OBJECT_CODE,        rc);

映射关系查找:

    elf::oid_t peer     = elf::Object::GetLastChild(uid,        entity::OBJECT_PEER);
    elf::oid_t uid      = elf::Object::GetLastChild(peer,       entity::OBJECT_USER);
    int server          = elf::Object::GetLastChild(uid,        entity::OBJECT_SERVER);
    int rc              = elf::Object::GetLastChild(peer,       entity::OBJECT_CODE);
    elf::id_set *users  = elf::Object::GetChildren(server,      entity::OBJECT_USER);

为了逻辑上的简化, 在所有服务器上, 用户均以 `user.id` 进行索引.

## 用户下线

用户