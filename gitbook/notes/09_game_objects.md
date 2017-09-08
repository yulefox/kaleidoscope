# 数据与业务的设计理念

----

## 更新日志

### 2017-07-01

* `[MOD]` 成长维度及战力计算

### 2017-02-16

* `[MOD]` 任务定义
* `[MOD]` 属性定义

### 2017-01-22

* `[MOD]` 属性定义

### 2017-01-12

* `[ADD]` 对象类型枚举
* `[ADD]` 各对象类型定义/更新

### 2016-12-10

* `[ADD]` 数据对象, 用户, 角色, 变量, 容器等

----

## 数据对象(object)

### 基础实现

两种:

* 继承自 `elf::Object`, 带封装: `GUser`, `GApp`.

* 直接使用 `protobuf`, 无额外封装.

### 对象的创建

`elf::Object` 对象在对 `m_pb` 赋非空值时调用 `OnInit` 接口, 完成对象创建及索引. 为了应对多重索引(如同一事件对象可能被多个用户持有), 为 `protobuf` 对象添加引用计数, `IndexProto` 会完成多重引用的自增计数, `UnindexProto` 会完成多重引用的自减计数, 需要**用户**保证对多重引用计数的正确使用.

### 对象类型枚举

```protobuf
    enum ObjectType
    {
        option allow_alias                          = true;
        OBJECT_NONE                                 = 0;        // 无
        OBJECT_SERVER                               = 1;        // 服务器
        OBJECT_SYSTEM                               = 2;        // 系统(系统变量等)
        OBJECT_SYSTEM_TEMP                          = 3;        // 系统临时变量
        OBJECT_APP_INDEX                            = 10;       // 当前应用 ID(单一节点)
        OBJECT_APP_TYPE                             = 11;       // 当前应用类型(单一节点)
        OBJECT_PEER_USERS                           = 98;       // 消息接收方可能是
        OBJECT_PEER_ITSELF                          = 99;       // 消息接收方是网络连接自身
        OBJECT_SERVER_GOD                           = 100;      // 中心服务器
        OBJECT_SERVER_DATA                          = 101;      // 数据服务器
        OBJECT_SERVER_GAME                          = 102;      // 游戏服务器
        OBJECT_SERVER_GATE                          = 103;      // 网关服务器
        OBJECT_SERVER_BATTLE                        = 104;      // 战斗服务器
        OBJECT_SERVER_CHAT                          = 105;      // 聊天服务器
        OBJECT_CODE                                 = 200;      // 结果码

        OBJECT_SCENE                                = 301;      // 场景
        OBJECT_GUILD                                = 302;      // 公会
        OBJECT_TEAM                                 = 303;      // 队伍

        OBJECT_USER                                 = 1001;     // 用户
        OBJECT_ROLE                                 = 1002;     // 角色
        OBJECT_ITEM                                 = 1003;     // 道具
        OBJECT_VARIABLE                             = 1004;     // 变量
        OBJECT_EVENT                                = 1005;     // 事件
        OBJECT_QUEST                                = 1006;     // 任务
        OBJECT_COST                                 = 1007;     // 消耗
        OBJECT_ATTR                                 = 1008;     // 属性
        OBJECT_RANK                                 = 1017;     // 排名
        OBJECT_MAIL                                 = 1018;     // 邮件
        OBJECT_CONFIG                               = 1101;     // 配置
        CONTAINER_USER                              = 2001;     // 用户
        CONTAINER_ROLE                              = 2002;     // 角色
        CONTAINER_ITEM                              = 2003;     // 道具
        CONTAINER_VARIABLE                          = 2004;     // 变量
        CONTAINER_EVENT                             = 2005;     // 事件
        CONTAINER_QUEST                             = 2006;     // 任务
        CONTAINER_COST                              = 2007;     // 消耗
        CONTAINER_ATTR                              = 2008;     // 属性
        CONTAINER_CONFIG                            = 2101;     // 配置
        CONTAINER_SHADOW_BEGIN                      = 3003;     // 影子容器
        CONTAINER_SHADOW_ITEM                       = 3003;     // 影子道具
        CONTAINER_SHADOW_VARIABLE                   = 3004;     // 影子变量
        CONTAINER_SHADOW_EVENT                      = 3005;     // 影子事件
        CONTAINER_SHADOW_QUEST                      = 3006;     // 影子任务
        CONTAINER_SHADOW_COST                       = 3007;     // 影子消耗
        CONTAINER_SHADOW_ATTR                       = 3008;     // 影子属性
        CONTAINER_SHADOW_END                        = 3008;     // 影子容器
        OBJECT_PEER                                 = 9999;     // 网络连接
        OBJECT_APP                                  = 10000;    // 5-6 位为应用编号
        OBJECT_ID                                   = 2000000000; // 64 位供对象 ID 使用
    }
```

## 逻辑对象

将游戏中的数据对象(`protobuf`) 与业务逻辑剥离. 数据对象直接使用 `protobuf`, 不做任何额外封装, 利用 `protobuf` 提供的接口实现**添加**, **删除**, **修改属性**等操作. 相关业务逻辑通过外部接口实现. 数据对象类型有:

* 用户(`User`)

* 角色(`Role`)

* 道具(`Item`)

* 变量(`Variable`)

* 事件(`Event`)

* 任务(`Quest`)

* 消耗(`Cost`)

* 属性(`Attr`)

### 用户(`User`)

每个用户 `user` 对应一个玩家账号, 用以承载该账号的公用游戏数据.

```protobuf
    message User
    {
        int64 id = 1;                       // ID
        int64 pid = 2;                      // 父 ID
        bytes ext = 3;                      // 扩展数据

        string alias = 4;                   // 别名
        bytes account = 5;                  // 用户账号
        bytes name = 6;                     // 用户名
        int32 status = 7;                   // 用户状态
        int32 server = 8;                   // 区服
        bytes channel = 10;                 // 渠道
        string addr = 11;                   // IP 地址
        string device = 13;                 // 设备号
        string device_type = 14;            // 设备类型
        int32 createtime = 15;              // 创建时间
        int32 stamp = 16;                   // 上次存盘时间

        repeated Attr attr = 20;            // 属性表
        repeated Role role = 21;            // 角色列表
        repeated Item item = 22;            // 道具列表
        repeated Variable variable = 23;    // 变量列表
    }
```

### 角色(`Role`)

存储单个角色的游戏数据.

```protobuf
    message Role {
        int64 id = 1;                       // ID
        int64 pid = 2;                      // 父 ID
        bytes ext = 3;                      // 扩展数据

        string alias = 5;                   // 别名
        int32 cls = 6;                      // 职业
        bytes name = 7;                     // 角色名
        int32 status = 10;                  // 当前状态
        int32 createtime = 13;              // 创建时间
        int32 stamp = 14;                   // 上次存盘时间

        repeated Attr attr = 20;            // 属性表
        repeated Item item = 22;            // 道具列表
        repeated Variable variable = 23;    // 变量列表
    }
```

### 道具(`Item`)

```protobuf
    message Item
    {
        int64 id = 1;                       // ID
        int32 idx = 2;                      // 道具配置id: 对应道具表
        int64 pid = 3;                      // 父 ID

        int32 num = 4;                      // 数量
        int32 delta = 5;                    // 变化量(+/-)
        int32 status = 6;                   // 当前状态
        int32 cls = 7;                      // 装备职业
        int32 field = 8;                    // 装备栏位, 0: 未装备
        int32 createtime = 10;              // 创建时间
        int32 stamp = 11;                   // 更新时间戳
        bytes ext = 19;                     // 扩展数据

        repeated Attr attr = 20;            // 成长维度
        repeated Cost cost = 21;            // 成长消耗
        repeated Variable variable = 23;    // 变量列表
    }
```

### 变量(`Variable`)

变量可以当做计数器使用, 也可以记录一个功能模块的所有数据.

```cpp
    // ================== 客户端变量 [         1 -  100000000)
    // ================== 配置变量   [ 100000000 - 1000000000)
    // ================== 服务器变量 [1000000000 - 2000000000)
```

```protobuf
    message Variable
    {
        int64 id = 1;                       // ID
        int64 pid = 2;                      // 父 ID
        int32 idx = 3;                      // 类型
        int32 val_32 = 4;                   // 32 位数值
        int64 val_64 = 5;                   // 64 位数值
        bytes val = 6;                      // 字符串值
        int32 status = 7;                   // 当前状态
        int32 createtime = 13;              // 创建时间
        int32 stamp = 14;                   // 上次存盘时间
    }
```

### 事件(`Event`)

```protobuf
    message Event
    {
        int64 id = 1;                       // ID (key)
        int64 pid = 2;                      // 父 ID
        int64 uid = 3;                      // 用户 ID
        int32 idx = 4;                      // 事件类型
        int32 oper = 5;                     // 操作事件源
        int32 host = 6;                     // 事件主体
        int32 arg_a = 8;                    // 32 位整型参数 1
        int32 arg_b = 9;                    // 32 位整型参数 2
        int64 arg_64 = 11;                  // 64 位整型参数
        string arg_str = 12;                // 字符串参数
        int32 status = 13;                  // 状态
        int64 role_a = 14;
        int64 role_b = 15;
        RoleTip role_tip_a = 16;
        RoleTip role_tip_b = 17;

        int32 createtime = 18;              // 创建时间
        int32 stamp = 19;                   // 更新时间

        repeated Variable variable = 23;    // 变量列表
    }
```

## 任务(`Quest`)

```protobuf
    message Quest
    {
        int64 id = 1;                       // ID
        int64 pid = 2;                      // 父 ID
        int32 idx = 3;                      // 任务编号
        int32 prog_s = 5;                   // 任务进度
        int32 prog_c = 6;                   // 领奖进度
        int32 status = 7;                   // 任务状态
        int32 createtime = 13;              // 创建时间
        int32 stamp = 14;                   // 上次存盘时间
    }
```

不再支持自动完成的任务, 可通过系统变量实现.

## 消耗(`Cost`)

```protobuf
    message CostArgs
    {
        int32 num = 1;                      // 消耗数量
        int32 total = 2;                    // 消耗总需求数量
        int32 remain = 3;                   // 消耗剩余数量
        bool passed = 4;                    // 消耗验证是否通过
        map<int64, int32> item = 9;         // 道具/数量
    }

    message Cost
    {
        int64 id = 1;                       // ID
        int64 pid = 2;                      // 父 ID
        int32 idx = 3;                      // 道具
        int32 num = 4;                      // 道具数量
        int32 status = 8;                   // 状态
        int32 createtime = 10;              // 创建时间
        int32 stamp = 11;                   // 变更时间
        map<int64, CostArgs> solo = 20;     // 单次消耗记录(按逻辑事件划分)
    }
```

```c++
// --------- Cost --------- 
///
/// Check cost Item by ID.
/// @param[in] evt Event type.
/// @param[in] eid Event ID.
/// @param[in] pid Parent ID.
/// @param[in] iid Item ID.
/// @return Result code.
///
int CheckCost(int evt, elf::oid_t eid, elf::oid_t pid, elf::oid_t iid);

///
/// Check cost Item by idx.
/// @param[in] evt Event type.
/// @param[in] eid Event ID.
/// @param[in] pid Parent ID.
/// @param[in] idx Item index.
/// @param[in] num Item num.
/// @return Result code.
///
int CheckCost(int evt, elf::oid_t eid, elf::oid_t pid, int idx, int num);

///                                                                       
/// Deduct costs with event.                                              
/// @param[in] evt Event type.                                            
/// @param[in] eid Event ID.                                              
/// @param[in] tag Client tag.                                            
/// @param[in] pid Parent ID.                                             
/// @param[in] iid Item ID(marking costs).                                
/// @return Result code.                                                  
///                                                                       
int DeductCosts(int evt, elf::oid_t eid, int tag, elf::oid_t pid, elf::oid_t iid = 0); 

///                                                                       
/// Rollback costs with event.                                            
/// @param[in] evt Event type.                                            
/// @param[in] eid Event ID.
/// @param[in] tag Client tag.                                            
/// @param[in] pid Parent ID.
/// @return Result code.
///
int RollbackCosts(int evt, elf::oid_t eid, int tag, elf::oid_t pid);      
```

> 不可堆叠的道具消耗, 只能由客户端指定道具 ID, 不能由服务器根据编号自动扣除
> 可堆叠的道具消耗, 只能由服务器根据编号自动扣除

- 检查消耗 `CheckCost`
- 逻辑成功, 扣除消耗: `RemoveCosts`
- 逻辑失败, 回滚消耗: `RollbackCosts`

可能存在多条业务逻辑共用消耗(如金币等)的情况, 甚至存在消耗挂起的情况. 为应对这些事件, 采用以下实现:

- `Cost` 容器挂在 `UserID` 下
- 每个业务逻辑有自己的 `CostArgs`, 记录消耗的详细信息

### TODO

- 将消耗与事件关联

## 属性(`Attr`)

```protobuf
    message AttrItem
    {    
        int32 type = 1;                     // 屬性项类型
        int32 val = 2;                      // 属性项值
    }    

    message Attr {
        int64 id = 1;                       // ID    
        int64 pid = 2;                      // 父 ID 
        int32 type = 3;                     // 属性类型
        int32 idx = 4;                      // 编号  
        int32 lvl = 5;                      // 等级          
        int32 exp = 6;                      // 经验          
        int32 combat = 7;                   // 战斗力        
        int32 status = 8;                   // 状态          
        int32 dep = 9;                      // 依赖成长维度  
        int32 createtime = 10;              // 创建时间
        int32 stamp = 11;                   // 变更时间
        bytes item_s = 19;                  // 属性集        
        repeated AttrItem item = 20;        // 属性集        
        int32 pre_combat = 21;              // 战力前值      
        bool dirty = 22;                    // 是否持有脏数据
    }    
```

`Attr.item` 的 `type` 使用 `AttrType` 定义的 `ATTR_SOLO_COMBAT_BEGIN - ATTR_SOLO_COMBAT_END` 区间.

战力成长相关维度使用 `AttrType` 定义的 `ATTR_COMBAT_BEGIN - ATTR_COMBAT_END` 区间, 服务器不关心具体类型.

### 属性枚举

```protobuf
    enum AttrType
    {
        ATTR_SOLO_COMBAT_BEGIN                      = 0;     // 单项战力属性
        ATTR_HP                                     = 1;     // 生命值 health point
        ATTR_ATK                                    = 2;     // 攻击 attack
        ATTR_DEF                                    = 3;     // 防御 defense
        ATTR_ATKDEV                                 = 4;     // 神圣攻击 atkdev
        ATTR_DODGE                                  = 5;     // 闪避 dodge
        ATTR_CRIR                                   = 6;     // 暴击 critical striking rate
        ATTR_CRIV                                   = 7;     // 暴击伤害 critical striking value
        ATTR_DES                                    = 8;     // 破甲 destroy
        ATTR_DAMADDR                                = 9;     // 伤害加深倍率
        ATTR_DAMRESIST                              = 10;    // 伤害减少倍率
        ATTR_SOLO_COMBAT_END                        = 11;    // 单项战力属性
        ATTR_TOTAL                                  = 90;    // 汇总属性/战力
        ATTR_USER                                   = 91;    // 用户
        ATTR_ROLE                                   = 92;    // 角色
        ATTR_ITEM                                   = 93;    // 装备
        ATTR_DIMENSION_BEGIN                        = 100;   // 成长维度
        ATTR_UPGRADE_LEVEL                          = 200;   // 等级
        ATTR_UPGRADE_STAR                           = 201;   // 星级
        ATTR_UPGRADE_RANK                           = 202;   // 品阶
        ATTR_UPGRADE_QUALITY                        = 203;   // 品质
        ATTR_DIMENSION_END                          = 9999;  // 成长维度
        ATTR_EXTRA                                  = 10000; // 客户端自定义属性
    }
```

### 特殊成长

除与战力计算相关的基础属性及成长外, 另有与服务器关联比较松散的特殊成长维度, 自 `AttrType.ATTR_EXTRA(10000)` 开始由客户端使用, 对服务器相对透明. 其随机属性对应编号记录在 `Attr` 对象属性集中的 `AttrType.ATTR_CUSTOM(0)` 项.

以神器为例:

```sh
    [USER] EVENT_ITEM_ADD (item, num)
    |--> [ITEM] EVENT_ITEM_INIT (subclass, quality)
        |--> [ITEM] EVENT_ATTR_LEVEL_SET (type, level)
        |--> [ITEM] EVENT_ATTR_EXTRA_INIT (probability, type)
```

- 神器主属性(固定)初始化操作 `EVENT_ATTR_LEVEL_SET`:

```lua
    /Game.Run("EVENT_ATTR_LEVEL_SET", 10000, 1);
```

主属性的成长规则与常规成长维度一致.

- 神器附加属性(随机)初始化操作 `EVENT_ATTR_EXTRA_INIT`:

```lua
    /Game.Run("EVENT_ATTR_EXTRA_INIT", 10000, 10001);
    /Game.Run("EVENT_ATTR_EXTRA_INIT", 5000, 10002);
```

附加属性的成长不使用等级成长方式(等级固定为 `1`), 仅使用经验成长(成长经验值为基于配置的随机数).

详细信息参见[事件相关文档](/notes/10_game_events.html).

## 容器(`container`)

一般情况下, 数据对象都是另一个对象的附属, 数据对象间的从属关系用容器表示:

               +---> variable
        user --+---> role
               +---> item
               +---> event
               +---> quest
               +---> mail

       scene --+---> user

       guild --+---> user
               +---> variable

        team --+--> user
               +---> variable

        role --+---> item
               +---> variable

容器的成员是对象 ID(`elf::oid_t`, 而非对象指针). 如果需要获取对象, 可以根据对象的唯一 ID 查找到 `protobuf` 对象.

为了简化容器操作, 我们可以将容器固化为三层的树状结构:

                      对象 ID
                    /   |    \
              类型 A   类型 B   类型 C
                 /      |       \
          对象 ID...  对象 ID...  对象 ID...

第一层为作为容器的对象 ID, 一般而言, 以 `elf::oid_t` 类型的对象 ID(全局唯一)作为容器 ID.

还有一些容器, 不是上述通用对象, 或者没有分配 `elf::oid_t` 类型的 ID, 他们使用 `int32_t` 类型的 ID:

* `0`: root 容器

* 应用(`App`)编号: 如, `100011`

注意: 需要保证上述容器 ID 的唯一性.

第二层为成员对象类型:

```protobuf
    OBJECT_NONE = 0;                        // 无
    OBJECT_USER = 1;                        // 用户
    OBJECT_ROLE = 2;                        // 角色
    OBJECT_ITEM = 3;                        // 道具
    OBJECT_VARIABLE = 4;                    // 变量
    OBJECT_EVENT = 5;                       // 事件
    OBJECT_QUEST = 6;                       // 任务
    OBJECT_MAIL = 8;                        // 邮件
    OBJECT_GUILD = 9;                       // 公会
    OBJECT_PEER = 1001;                     // 网络连接
    OBJECT_SERVER = 2001;                   // 服务器
    OBJECT_RESULT_CODE = 2002;              // 结果码
```

第三层为成员对象 ID, 成员对象 ID 与容器对象 ID 是互为**全集**的.

### 容器操作

```cpp
    ///
    /// Find children by container object ID and type in `s_containers`.
    /// @param[in] cid Container ID.
    /// @param[in] type Container type.
    /// @return Pointer to container if found, or NULL.
    ///
    static elf::id_set *GetChildren(elf::oid_t cid, int type);

    ///
    /// Remove children from `s_containers`.
    /// @param[in] cid Container ID.
    /// @param[in] type Container type, clear all if type is 0.
    ///
    static void DelChildren(elf::oid_t cid, int type = 0);

    ///
    /// Find the last/only child object ID by container object ID and type in `s_containers`.
    /// @param[in] cid Container ID.
    /// @param[in] type Container type.
    /// @return Last/Only element object ID.
    ///
    static elf::oid_t GetLastChild(elf::oid_t cid, int type);

    ///
    /// Set the only child object ID into `s_containers`.
    /// @param[in] cid Container ID.
    /// @param[in] type Container type.
    /// @param[in] oid Object ID.
    ///
    static void SetChild(elf::oid_t cid, int type, elf::oid_t oid);

    ///
    /// Insert child object ID into `s_containers`.
    /// @param[in] cid Container ID.
    /// @param[in] type Container type.
    /// @param[in] oid Object ID.
    ///
    static void AddChild(elf::oid_t cid, int type, elf::oid_t oid);

    ///
    /// Remove child object ID from `s_containers`.
    /// @param[in] cid Container ID.
    /// @param[in] type Container type.
    /// @param[in] oid Object ID.
    ///
    static void DelChild(elf::oid_t cid, int type, elf::oid_t oid);
```

## 网络连接容器

网络消息最终是通过 `OBJECT_PEER` 类型的网络连接(具有唯一 ID)发送的. 网络连接使用对象容器进行管理, 能够拥有 `OBJECT_PEER` 子节点的对象:

* 应用(`App`, `OBJECT_APP`)

* 用户(`User`, `OBJECT_USER`)

## TODO

* App 纳入 AddPB

* 发送邮件以 ID 为准

* 排行榜通过 Variable 实现

----


