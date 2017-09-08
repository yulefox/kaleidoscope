# 事件

----

## 更新日志

### 2017-05-24

* `[ADD]` `EVENT_USER_NAME` 设置用户昵称: 重名校验, 改名消耗(暂定 200 钻石)
* `[ADD]` `EVENT_BATTLE_MATCH` (跨服)匹配

### 2017-05-16

* `[ADD]` `EVENT_ITEM_GACHA` 抽奖

### 2017-02-24

* `[ADD]` 道具转换, 道具成长

### 2017-02-16

* `[ADD]` 成长维度: 更新成长维度等级/经验, 成长维度计算
* `[MOD]` 任务: 更新任务服务器/客户端进度
* `[ADD]` 道具: 添加道具时设置初始等级, 装备/卸下/添加并装备道具时计算玩家成长维度

### 2017-01-10

* `[ADD]` 事件机制介绍, 事件枚举, 脚本示例(配置, 脚本, 道具, 道具组, 任务, 关卡, 用户)

----

## 机制介绍

* 业务请求: `SetEvent`
* 数据读取: `GetAny`
* 数据写入: `SetAny`
* 容器更新: `UpdateContainer`

事件来源从广义上讲有两种:

* 网络通信(来自其他服务器或客户端请求)
* 服务器自身逻辑触发

事件触发时, 执行对应事件逻辑, 然后加入前置事件列表. 当前逻辑帧结束时, 从 `EventBase` 表中读取后置事件列表, 依次执行列表中所有事件. 网络通信触发的事件, 其后置事件可在当前逻辑帧结束前处理.

需要注意的是: 事件的后置事件调整为**栈式调用**. 即, 同一个网络通信事件及其后置事件按**深度优先**触发, 这一点限制可能会导致某些**不确定性**.

## 事件定义

```protobuf
    message Event
    {
        int64 id = 1;                       // ID (key)
        int64 pid = 2;                      // 父 ID
        int64 uid = 3;                      // 用户 ID
        int32 idx = 4;                      // 事件类型
        int32 oper = 5;                     // 操作事件源
        int32 arg_a = 8;                    // 32 位整型参数 A
        int32 arg_b = 9;                    // 32 位整型参数 B
        int64 arg_64 = 11;                  // 64 位整型参数
        string arg_str = 12;                // 字符串参数
        int32 status = 13;                  // 状态

        int32 createtime = 18;              // 创建时间
        int32 stamp = 19;                   // 更新时间

        repeated Variable variable = 23;    // 变量列表
    }
```

## 事件枚举

事件枚举由一个 8 位整数表示.

`OPER_XXX` 段对应事件的操作源, 由服务器根据事件的请求者确定.

```protobuf
    // ------------- OPER ---------------------------------
    OPER_BEGIN                                  = 10000000; // 逻辑操作源
    OPER_COMMAND_CLIENT                         = 10000001; // 客户端执行 GM 指令
    OPER_COMMAND_SYSTEM                         = 10000002; // 系统执行 GM 指令(外部)
    OPER_REQUEST_CLIENT                         = 10000003; // 客户端请求
    OPER_SYSTEM_ROUTING                         = 10000009; // 系统事务
    OPER_SYSTEM_RECOVER                         = 10000010; // 系统定时恢复
    OPER_SYSTEM_QUEST                           = 10000011; // 任务奖励
    OPER_SYSTEM_LEVEL                           = 10000012; // 关卡奖励
    OPER_END                                    = 10009999; // 逻辑操作源

    // ------------- CONFIG ----------------------------------
    EVENT_CONFIG_GET                            = 10010100; // 客户端获取配置
    EVENT_CONFIG_LOAD                           = 10010101; // 服务器获取配置
    EVENT_CONFIG_RELOAD                         = 10010102; // 服务器重读配置

    // ------------- SERVER ----------------------------------
    EVENT_SERVER_STARTUP                        = 10010201; // 服务器启动
    EVENT_SERVER_LOOP                           = 10010202; // 服务器循环

    // ------------- CONTAINER ----------------------------------
    EVENT_CONTAINER_ADD                         = 10010301; // 容器元素插入 +
    EVENT_CONTAINER_DEL                         = 10010302; // 容器元素移除 -

    // ------------- LUA ----------------------------------
    EVENT_LUA_LOAD_ALL                          = 10010400; // 加载 Lua 脚本
    EVENT_LUA_FUNC                              = 10010401; // 运行 Lua 接口

    // ------------- USER ----------------------------------
    EVENT_USER_CREATE                           = 10010601; // 创建用户 +
    EVENT_USER_DELETE                           = 10010602; // 删除用户 -
    EVENT_USER_LOGIN                            = 10010603; // 用户上线 +
    EVENT_USER_LOGOUT                           = 10010604; // 用户下线 -
    EVENT_USER_SAVE                             = 10010611; // 用户数据存盘
    EVENT_USER_REMOVE                           = 10010612; // 移除内存用户

    // ------------- ROLE ----------------------------------
    EVENT_ROLE_CREATE                           = 10020101; // 创建角色 +
    EVENT_ROLE_DELETE                           = 10020102; // 删除角色 -

    // ------------- VARIABLE ----------------------------------
    EVENT_VARIABLE_SET                          = 10030000; // 设置变量
    EVENT_VARIABLE_INC                          = 10030001; // 增加变量 +
    EVENT_VARIABLE_DEC                          = 10030002; // 减少变量 -
    EVENT_VARIABLE_SAVE_SYSTEM                  = 10030101; // 保存系统变量

    // ------------- ITEM ----------------------------------
    EVENT_ITEM_ADD                              = 10040001; // 添加道具 +
    EVENT_ITEM_DEL                              = 10040002; // 删除道具 -
    EVENT_ITEM_GROUP_ADD                        = 10040011; // 添加道具组 +
    EVENT_ITEM_ARM                              = 10040101; // 装备道具 +
    EVENT_ITEM_UNARM                            = 10040102; // 卸下道具 -

    EVENT_ITEM_RECOVER                          = 10040200; // 道具回复
    EVENT_ITEM_USE                              = 10040201; // 使用道具
    EVENT_ITEM_SELL                             = 10040202; // 出售道具

    EVENT_ITEM_UPGRADE_LEVEL_SET                = 10041100; // 道具成长-等级设置
    EVENT_ITEM_UPGRADE_LEVEL_UP                 = 10041101; // 道具成长-等级增加 +
    EVENT_ITEM_UPGRADE_LEVEL_DOWN               = 10041102; // 道具成长-等级降低 -
    EVENT_ITEM_UPGRADE_STAR_SET                 = 10041200; // 道具成长-星级设置
    EVENT_ITEM_UPGRADE_STAR_UP                  = 10041201; // 道具成长-星级增加 +
    EVENT_ITEM_UPGRADE_STAR_DOWN                = 10041202; // 道具成长-星级降低 -
    EVENT_ITEM_UPGRADE_RANK_SET                 = 10041300; // 道具成长-品阶设置
    EVENT_ITEM_UPGRADE_RANK_UP                  = 10041301; // 道具成长-品阶增加 +
    EVENT_ITEM_UPGRADE_RANK_DOWN                = 10041302; // 道具成长-品阶降低 -
    EVENT_ITEM_UPGRADE_QUALITY_SET              = 10041400; // 道具成长-品质设置
    EVENT_ITEM_UPGRADE_QUALITY_UP               = 10041401; // 道具成长-品质增加 +
    EVENT_ITEM_UPGRADE_QUALITY_DOWN             = 10041402; // 道具成长-品质降低 -
```

## 逻辑请求

客户端的绝大多数逻辑请求均通过 `SetEvent.Req` 发送, `Event` 对象参数的说明如下:

* `idx`: 事件类型 `EVENT_XXX_YYY`, 对应具体事件, 如添加道具/设置变量/场景进入/道具购买/道具升级等
* `oper`: 操作事件源, 无需填写, 由服务器填充. 表示事件源是客户端请求/系统推送/GM指令等
* `pid`: 事件的父 ID, 服务器在收到 `SetEvent.Req` 请求时, 如果对应用户拥有已出战角色, `pid` 为出战角色 ID. `TriggerEvent` 处理过程中, `pid` 可能被指定为道具 ID 等
* `uid`: 用户 ID, 对应 `SetEvent.Req` 发送的客户端用户 ID
* `arg_a`: 变量类型/道具/任务/场景等编号
* `arg_b`: 32位数值/道具数量/任务状态/任务进度等
* `pid`: 64位数值, 事件操作对象(角色, 道具等)
* `arg_64`: 64位数值, `pid` 之外, 还有其他对象, (如为某角色装备某道具)
* `arg_str`: 字符串值

## 脚本示例

通过 GM 后台执行的脚本指令接口及参数如下:

```cpp
    /// 
    /// Trigger event by GM command.
    /// @param[in] evt_s Event type.
    /// @param[in] arg_a 32-bit argument A.
    /// @param[in] arg_b 32-bit argument B.
    /// @param[in] pid String ID for User, Role, Item, etc.
    /// @param[in] arg_64 64-bit argument.
    /// @param[in] arg_str String argument.
    /// @return Result code.
    ///
    int Exec(const std::string &evt_s, int arg_a = 0, int arg_b = 0,
            const std::string &pid = "", const std::string &arg_64 = "",
            const std::string &arg_str = "");
```

通过客户端执行的脚本指令接口及参数如下:

```cpp
    /// 
    /// Trigger event by client command.
    /// @param[in] evt_s Event type.
    /// @param[in] arg_a 32-bit argument A.
    /// @param[in] arg_b 32-bit argument B.
    /// @param[in] pid String ID for User, Role, Item, etc.
    /// @param[in] arg_64 64-bit argument.
    /// @param[in] arg_str String argument.
    /// @return Result code.
    /// 
    int Run(const std::string &evt_s, int arg_a = 0, int arg_b = 0,
            const std::string &pid = "", const std::string &arg_64 = "",
            const std::string &arg_str = "");
```

### 服务器重读配置

```lua
    /Game.Run("EVENT_CONFIG_RELOAD");
```

### 服务器加载配置

```lua
    /Game.Run("EVENT_CONFIG_LOAD");
```

### 客户端获取配置

```lua
    /Game.Run("EVENT_CONFIG_GET");
```

### 服务器重读所有 Lua 脚本(热更新)

```lua
    /Game.Run("EVENT_LUA_LOAD_ALL");
```

### 服务器运行 Lua 函数

```lua
    /Game.Run("EVENT_LUA_FUNC", arg_a, arg_b, "pid", "arg_64", "lua_func");
```

* `arg_a`: 32 位整型参数 A
* `arg_b`: 32 位整形参数 B
* `pid`: 64 位整型参数, 字符串形式
* `arg_64`: 64 位整型参数, 字符串形式
* `lua_func`: Lua 函数名称, 其参数为 `arg_a, arg_b, pid, arg_64`

### 从逻辑服加载数据

```lua
    /Game.Run("EVENT_ANY_GET", arg_a, 0, "pid", "arg_64");
```

* `arg_a`: 数据类型
* `pid`: 数据对象的父节点 ID
* `arg_64`: 单个数据对象的 ID, 留空则取父节点下指定类型所有数据, 字符串形式

### 从数据服加载数据

```lua
    /Game.Run("EVENT_ANY_LOAD", arg_a, 0, "pid", "arg_64");
```

* `arg_a`: 数据类型
* `pid`: 数据对象的父节点 ID
* `arg_64`: 单个数据对象的 ID, 留空则取父节点下指定类型所有数据, 字符串形式

### 成长维度计算

```lua
    /Game.Run("EVENT_ATTR_CALC", ATTR_UPGRADE_LEVEL, 10, "");
```

### 成长维度更新

```lua
    /Game.Run("EVENT_ATTR_CALC", ATTR_UPGRADE_LEVEL, 10, "");
    /Game.Run("EVENT_ATTR_LEVEL_SET", ATTR_UPGRADE_LEVEL, 10, "");
    /Game.Run("EVENT_ATTR_LEVEL_INC", ATTR_UPGRADE_LEVEL, 10, "");
    /Game.Run("EVENT_ATTR_LEVEL_DEC", ATTR_UPGRADE_STAR, 10, "", "ITEM_ID");
    /Game.Run("EVENT_ATTR_EXP_SET", ATTR_UPGRADE_LEVEL, 10000, "");
    /Game.Run("EVENT_ATTR_EXP_INC", ATTR_UPGRADE_LEVEL, 100, "");
    /Game.Run("EVENT_ATTR_EXP_DEC", ATTR_UPGRADE_STAR, 100, "", "ITEM_ID");
```

* `arg_a`: 成长维度类型
* `arg_b`: 设置/增加/减少的等级/经验值
* `pid`: 用户/道具/角色 ID, 默认为用户 ID

### 成长维度属性项修改

```lua
    /Game.Run("EVENT_ATTR_ITEM_SET", ATTR_UPGRADE_LEVEL, 10, "");
```

* `arg_a`: 成长维度类型
* `arg_b`: 属性项类型
* `arg_64`: 属性项值
* `pid`: 用户/道具/角色 ID, 默认为用户 ID

成长维度类型:

```protobuf
    enum AttrType
    {
        ATTR_UPGRADE_LEVEL                          = 200;   // 等级
        ATTR_UPGRADE_STAR                           = 201;   // 星级
        ATTR_UPGRADE_RANK                           = 202;   // 品阶
        ATTR_UPGRADE_QUALITY                        = 203;   // 品质
        ATTR_UPGRADE_EXTRA                          = 300;   // 异界
    }
```

### 添加道具

添加道具, 道具必须存在于 `config::ItemBase`.

```lua
    /Game.Run("EVENT_ITEM_ADD", 501001, 100);
```

* `arg_a`: 道具编号
* `arg_b`: 道具数量

### 添加道具(带恢复上限)

添加道具, 道具必须存在于 `config::ItemBase`.

```lua
    /Game.Run("EVENT_ITEM_RECOVER", 502002, 1);
```

* `arg_a`: 道具编号
* `arg_b`: 道具数量

### 删除道具

```lua
    /Game.Run("EVENT_ITEM_DEL", 201000, 100);
    /Game.Run("EVENT_ITEM_DEL", 0, 100, "", "ITEM_ID");
```

* `arg_a`: 道具编号
* `arg_b`: 道具数量
* `arg_64`: 道具 ID

### 装备道具

装备道具, 通过设置变量实现.

```lua
    /Game.Run("EVENT_ITEM_ARM", 101001, 1, "", "ITEM_ID");
```

* `arg_a`: 道具栏位
* `arg_b`: 道具编号
* `pid`: 角色 ID, 默认为用户 ID
* `arg_64`: 道具 ID

### 卸下道具

装备道具, 通过设置变量实现.

```lua
    /Game.Run("EVENT_ITEM_UNARM", 1);
```

* `arg_a`: 道具栏位

### 添加并装备一件道具

通过添加道具实现.

```lua
    /Game.Run("EVENT_ITEM_ADD_ARM", 101001, 1);
```

* `arg_a`: 道具编号
* `arg_b`: 道具栏位

### 使用道具

```lua
    /Game.Run("EVENT_ITEM_USE", 201000, 100);
```

* `arg_a`: 道具编号
* `arg_b`: 道具数量

### 购买道具(`ItemBase`)

```lua
    /Game.Run("EVENT_ITEM_BUY_BASE", 10, 1);
```

* `arg_a`: 道具编号, 关联道具表 `config::ItemBase`
* `arg_b`: 购买数量

购买道具以 `ItemBase` 表配置的 `buy_price` 作价格, 付出 `ITEM_YUANBAO`.

### 购买道具(商城)

```lua
    /Game.Run("EVENT_ITEM_BUY", 10, 1);
```

* `arg_a`: 配置编号, 关联道具商城表 `config::ItemMall`
* `arg_b`: 购买数量

#### 商城售卖列表

- 售卖列表按配置编号增序排列
- 同一商城类型, 同一子组连续配置
- 数量 `num == 0`, 商品未上架或已下架
- 子组 `cate == 0`, 固定售卖, 始终显示 
- 权重 `weight == 0`, 无法随机到
- 同一商城的同一子组为一个道具池, `num` 表示该道具池抽取所占孔数
- 同一商城的各个道具池使用同一个种子变量(允许用户调整该变量)进行不放回抽取

#### 道具池随机算法

```
seed_type := VARIABLE_SEGMENT_MALL_SEED + mall_type(<1000)
seed := USER.Variable32(seed_type) | SYSTEM.Variable32(seed_type)
item_list_n := PickItemList(seed, pool_n, num_n)
```

#### 道具折扣价格计算公式

```
total := num * price * discount / 100
```

#### 道具购买次数变量

```
var_idx: VARIABLE_SECTOR_MALL_ITEM + offset(<1000000)
```

该变量累加的是购买次数(非目标道具数量). 购买后, 玩家变量值大于配置值, 不可购买

#### 道具购买限制变量

```
limit_var_a_idx
limit_var_b_idx
```

玩家变量值小于配置值, 不可购买

### 出售道具

```lua
    /Game.Run("EVENT_ITEM_SELL", 201000, 100);
```

* `arg_a`: 道具编号
* `arg_b`: 道具数量

出售道具以 `ItemBase` 表配置的 `sell_price` 作价格, 获得 `ITEM_GOLD`.

### 道具转换

```lua
    /Game.Run("EVENT_ITEM_TRANSFORM", 1000, 0, "", "", "ITEM_ID_LIST");
```

* `arg_a`: 配置编号
* `arg_str`: 道具 ID 列表(`EventArgs` 序列化)

装备分解, 带成长维度及等级限制的材料分解, 发消息时除需要指定道具转换配置行 ID 外, 还需要带上分解道具 ID 列表.

### 道具成长

```lua
    /Game.Run("EVENT_ITEM_UPGRADE", 1000, 1, "ITEM_ID", "", "ITEM_ID_LIST");
```

* `arg_a`: 配置编号
* `arg_b`: 是否消耗可选道具
* `pid`: 成长道具 ID
* `arg_str`: 消耗道具 ID 列表(`EventArgs`)

当道具成长方式为积累经验升级时, 道具增加经验值(配置为 `-1`)为当前拥有的所有经验道具, 触发**更新成长维度经验**(`EVENT_ATTR_EXP_INC`)事件.

装备成长, 带成长维度及等级限制的消耗, 发消息时除需要指定装备成长配置行 ID 外, 还需要带上消耗道具 ID 列表.

### 道具继承

```lua
    /Game.Run("EVENT_ITEM_INHERIT", 0, 0, "DST_ID", "SRC_ID");
```

* `pid`: 继承后目标道具 ID
* `arg_64`: 继承前源道具 ID

该事件仅供脚本测试或作为后续事件调用, 禁止由玩家直接触发.

目标道具继承源道具的指定范围成长维度(`ATTR_INHERIT + 2000`).

### 抽奖

```lua
    /Game.Run("EVENT_ITEM_GACHA", 10, 1);
```

* `arg_a`: 抽奖类型 `GachaType`
* `arg_b`: 抽奖次数

关联变量 `VARIABLE_SEGMENT_GACHA(1950001000) + GACHA_TYPE(< 1000)`.

- 判断关联变量当前概率, `>= 10000`, 触发事件 `EVENT_ITEM_GACHA_SPECIAL`, 否则触发事件 `EVENT_ITEM_GACHA_NORMAL`
- `config::ItemGroup` 配置事件:
  - `EVENT_ITEM_GACHA_NORMAL,  GACHA_TYPE, -1`
  - `EVENT_ITEM_GACHA_SPECIAL, GACHA_TYPE, -1`

### 添加道具组

添加一组道具, 道具组必须存在于 `config::ItemGroup`.

注意: 一次只能添加道具组 X1, 如果希望获得多个同一道具组, 推荐修改道具组配置, 或触发多次事件. 详情参考[道具组配置](10_game_configs.html#道具组cfgitemgroup).

```lua
    /Game.Run("EVENT_ITEM_GROUP_ADD", 10100111, 100101);
```

* `arg_a`: 事件类型
* `arg_b`: 道具组编号

### 设置任务状态

```lua
    /Game.Run("EVENT_QUEST_STATUS_SET",201000,2);
```

* `arg_a`: 任务编号
* `arg_b`: 任务状态

### 更新服务器任务进度

```lua
    /Game.Run("EVENT_QUEST_PROG_S_SET",201000,2);
    /Game.Run("EVENT_QUEST_PROG_S_INC",201000,2);
```

* `arg_a`: 任务编号
* `arg_b`: 服务器任务进度

不再支持自动完成的任务, 可通过系统变量实现.

### 设置客户端任务进度

触发领奖.

```lua
    /Game.Run("EVENT_QUEST_PROG_C_SET",201000,2);
```

* `arg_a`: 任务编号
* `arg_b`: 客户端任务进度

注意: 设置客户端任务进度(`prog_c`)须满足:

* 任务未被删除
* 不得小于等于当前客户端进度(`prog_c`)
* 不得大于当前服务器进度(`prog_s`)

### 创建角色

```lua
    /Game.Run("EVENT_ROLE_CREATE", 104, 0, "", "褚遂良");
```

* `arg_a`: 职业
* `arg_str`: 角色名称

### 创建角色品质不同, 触发该事件

```lua
    /Game.Run("EVENT_ROLE_CREATE_RANK", 1);
```

* `arg_a`: 角色品质

### 删除角色

设置角色状态.

```lua
    /Game.Run("EVENT_ROLE_DELETE", 0, 0, "", ROLE_ID);
```

* `arg_64`: 角色 ID

### 选择当前角色

装备道具, 通过设置变量实现.

```lua
    /Game.Run("EVENT_ROLE_SELECT", 0, 0, ROLE_ID);
```

* `pid`: 角色 ID

设置成功后, 通过 `DoLoadAny`(`GetAny`) 加载角色数据.

### 角色成长

与**道具成长**实现相同.

```lua
    /Game.Run("EVENT_ITEM_UPGRADE", 1000, 1, ROLE_ID, "", ARG_STR);
```

* `arg_a`: 配置编号
* `arg_b`: 是否消耗可选道具
* `pid`: 成长角色 ID
* `arg_str`: 道具 ID 列表(`EventArgs`)

当道具成长方式为积累经验升级时, 道具增加经验值(配置为 `-1`)为当前拥有的所有经验道具, 触发**更新成长维度经验**(`EVENT_ATTR_EXP_INC`)事件.

### 进入场景

```lua
    /Game.Run("EVENT_SCENE_ENTER",201000,1);
```

* `arg_a`: 场景编号
* `arg_b`: 场景分线(默认由服务器根据指定规则分配)

### 退出场景

```lua
    /Game.Run("EVENT_SCENE_LEAVE");
```

### 关卡结束

```lua
    /Game.Run("EVENT_SCENE_END",3,60);
```

* `arg_a`: 关卡星级(`0`: 失败, `1-3`: 胜利)
* `arg_b`: 所用时长

### 修改玩家昵称

```lua
    /Game.Run("EVENT_USER_NAME", 0, 0, "", "", NAME);
```

* `arg_str`: 昵称

玩家昵称同时存储在变量 `VARIABLE_USER_NAME` 中.

### 保存玩家数据

```lua
    /Game.Run("EVENT_USER_SAVE");
```

### 玩家下线

```lua
    /Game.Run("EVENT_USER_LOGOUT");
```

### 玩家移除

```lua
    /Game.Run("EVENT_USER_REMOVE");
```

### 设置变量/系统变量

```lua
    /Game.Run("EVENT_VARIABLE_SET", 10030000, 2, "pid", "arg_64", arg_str);
    /Game.Run("EVENT_VARIABLE_SYS_SET", 10030000, 2, OBJECT_SYSTEM, "arg_64", arg_str);
```

### 设置变量/系统变量为时间戳

```lua
    /Game.Run("EVENT_VARIABLE_STAMP", 10030000, 0, "pid", "arg_64", arg_str);
    /Game.Run("EVENT_VARIABLE_SYS_STAMP", 10030000, 0, OBJECT_SYSTEM, "arg_64", arg_str);
```

* `arg_a`: 变量类型
* `arg_b`: 时间戳, `0` 使用当前系统时间
* `arg_64`: 变量的 64 位数值, 字符串形式
* `arg_str`: 变量的字符串值

### 增加变量/系统变量

```lua
    /Game.Run("EVENT_VARIABLE_INC", 10030000, 2);
    /Game.Run("EVENT_VARIABLE_SYS_INC", 10030000, 2, OBJECT_SYSTEM);
```

* `arg_a`: 变量类型
* `arg_b`: 变量的 32 位数值
* 未支持增加 64 位数值

### 减少变量/系统变量

```lua
    /Game.Run("EVENT_VARIABLE_DEC", 10030000, 2);
    /Game.Run("EVENT_VARIABLE_SYS_DEC", 10030000, 2, OBJECT_SYSTEM);
```

* `arg_a`: 变量类型
* `arg_b`: 变量的 32 位数值
* 未支持减少 64 位数值

### 购买变量

```lua
    /Game.Run("EVENT_VARIABLE_BUY", 1799501001);
```

### 保存所有系统变量

```lua
    /Game.Run("EVENT_VARIABLE_SAVE_SYSTEM");
```

### 计算成长维度

```lua
    /Game.Run("EVENT_ATTR_CALC", 200, 101);
```

成长维度类型:

```protobuf
    ATTR_TOTAL                                  = 90;    // 汇总属性/战力
    ATTR_USER                                   = 91;    // 用户         
    ATTR_ROLE                                   = 92;    // 角色         
    ATTR_ITEM                                   = 93;    // 装备         
    ATTR_COMBAT_BEGIN                           = 100;   // 战力相关成长维度
    ATTR_UPGRADE_LEVEL                          = 200;   // 等级         
    ATTR_UPGRADE_STAR                           = 201;   // 星级         
    ATTR_UPGRADE_RANK                           = 202;   // 品阶         
    ATTR_UPGRADE_QUALITY                        = 203;   // 品质         
    ATTR_COMBAT_END                             = 9999;  // 战力相关成长维度
    ATTR_EXTRA                                  = 10000; // 特殊成长起始(其后由客户端定义使用)
```

* `arg_a`: 成长维度类型
* `arg_b`: 成长维度索引编号, 角色按职业(3 位整数)索引, 道具按 `config::ItemMap` 映射(6 位整数)或道具编号(6 位整数)索引.
* `pid`: 用户/角色/道具 ID, 默认为用户 ID

### 更新成长维度等级

```lua
    /Game.Run("EVENT_ATTR_LEVEL_SET", 200, 10);
    /Game.Run("EVENT_ATTR_LEVEL_INC", 200, 1);
    /Game.Run("EVENT_ATTR_LEVEL_DEC", 200, 1);
```

* `arg_a`: 成长维度类型
* `arg_b`: 成长维度索引编号, 角色按职业(3 位整数)索引, 道具按 `config::ItemMap` 映射(6 位整数)或道具编号(6 位整数)索引.
* `pid`: 用户/角色/道具 ID, 默认为用户 ID

成长维度等级更新成功后, 触发 `EVENT_ATTR_CALC`, 重新计算玩家成长维度(无论对应成长维度是否影响玩家成长维度, 待优化).

### 更新成长维度经验

```lua
    /Game.Run("EVENT_ATTR_EXP_SET", 200, 10000);
    /Game.Run("EVENT_ATTR_EXP_INC", 200, 100);
    /Game.Run("EVENT_ATTR_EXP_DEC", 200, 100);
```

* `arg_a`: 成长维度类型
* `arg_b`: 成长维度索引编号, 角色按职业(3 位整数)索引, 道具按 `config::ItemMap` 映射(6 位整数)或道具编号(6 位整数)索引.
* `pid`: 用户/角色/道具 ID, 默认为用户 ID

成长维度经验值增加后, 判断是否触发更新成长维度等级. 如果**没有其他消耗**, 则**一直升级至无法升级为止**, 反之, **最多升级一次**.

### 成长维度的刷新与确认

```lua
    /Game.Run("EVENT_ATTR_REFRESH", 1000, 1, "ITEM_ID");
    /Game.Run("EVENT_ATTR_CONFIRM", 1000, 0, "ITEM_ID");
```

* `arg_a`: 成长维度类型
* `arg_b`: 刷新后等级(不同等级对应属性区间不同)
* `pid`: 道具 ID

#### 成长维度的刷新

客户端消息实现采用 `EVENT_ITEM_UPGRADE`. 当成长维度配置为等级不提升(`rate = 0 && inc_exp = 0`) 时, 即触发后续事件 `EVENT_ATTR_REFRESH`.

`cfg_upgrade_base` 的 `downgrade` 配置为刷新后等级.

该事件仅供脚本测试或作为后续事件调用, 禁止由玩家直接触发.

#### 成长维度的确认

刷新后的属性临时存放在成长维度 `ATTR_TEMP` 中, 玩家确认后, 以 `ATTR_TEMP` 覆盖原成长维度.

在服务器明确收到客户端 `EVENT_ATTR_CONFIRM` 事件或 `ATTR_TEMP` 被改写前, 即使掉线后, 玩家依然可以确认.

### 创建容器

```lua
    /Game.Run("EVENT_CONTAINER_CREATE", [type], 0, "", 0, [name]);
```

* `arg_a`: 容器类型
  - `OBJECT_TEAM`
  - `OBJECT_GUILD`
* `arg_str`: 容器名称

### 加入容器

```lua
    /Game.Run("EVENT_CONTAINER_ADD", [type], 0, [cid], 0, "");
```

* `arg_a`: 容器类型
  - `OBJECT_TEAM`
  - `OBJECT_GUILD`
* `arg_64`: 容器ID(VARIABLE_SEGMENT_CONTAINER + type)

### 退出容器

```lua
    /Game.Run("EVENT_CONTAINER_DEL", [type], 0, [cid], 0, "");
```

* `arg_a`: 容器类型
  - `OBJECT_TEAM`
  - `OBJECT_GUILD`
* `arg_64`: 容器ID(VARIABLE_SEGMENT_CONTAINER + type)

### 删除容器

```lua
    /Game.Run("EVENT_CONTAINER_DESTROY", [type], 0, [cid], 0, "");
```

* `arg_a`: 容器类型
  - `OBJECT_TEAM`
  - `OBJECT_GUILD`
* `arg_64`: 容器ID(VARIABLE_SEGMENT_CONTAINER + type)

### 获取容器列表

    /Game.Run("EVENT_CONTAINER_LIST", CONTAINER_TYPE);

* `arg_a`: 容器类型

### 获取容器成员列表

    /Game.Run("EVENT_CONTAINER_MEMBERS", CONTAINER_TYPE, CONTAINER_ID);

* `arg_a`: 容器类型
* `arg_64`: 容器 ID(可选, 服务器根据类型获取)

### 扩展成长维度初始化

```lua
    /Game.Run("EVENT_ATTR_EXTRA_INIT", 5000, 10001);
```

* `arg_a`: 扩展成长维度获得概率(万分比)
* `arg_b`: 扩展成长维度类型
* `pid`: 用户/角色/道具 ID, 默认为用户 ID

### 开始/取消匹配

```lua
    /Game.Run("EVENT_BATTLE_MATCH", 21, 1);
    /Game.Run("EVENT_BATTLE_MATCH", 21, 0);
```

* `arg_a`: 场景子类型.
* `arg_b`: 匹配标识, `1`: 开始匹配, `0`: 取消匹配
* `pid`: 单人匹配时默认为用户 ID, 预组队匹配时为队伍 ID.

### 无条件执行定时器

```lua
    /Game.Run("EVENT_TIMER_EXECUTE_UNCOND", 0, 0);
    /Game.Run("EVENT_TIMER_EXECUTE_UNCOND", 0, TIME_STAMP);
    /Game.Run("EVENT_TIMER_EXECUTE_UNCOND", 101, 0);
    /Game.Run("EVENT_TIMER_EXECUTE_UNCOND", 10001, 0);
    /Game.Run("EVENT_TIMER_EXECUTE_UNCOND", 10001, TIME_STAMP);
```

* `arg_a`: 配置编号, `0`: 所有配置
* `arg_b`: 时间戳, `0`: 取当前时间

无论定时器是否生效, 触发条件是否满足, 均执行定时器触发事件, 并设置定时器活动标记为 `true`.

### 无条件关闭定时器

```lua
    /Game.Run("EVENT_TIMER_TERMINATE_UNCOND", 0, 0);
    /Game.Run("EVENT_TIMER_TERMINATE_UNCOND", 0, TIME_STAMP);
    /Game.Run("EVENT_TIMER_TERMINATE_UNCOND", 10001, 0);
    /Game.Run("EVENT_TIMER_TERMINATE_UNCOND", 10001, TIME_STAMP);
```

* `arg_a`: 配置编号, `0`: 所有配置
* `arg_b`: 时间戳, `0`: 取当前时间

无论定时器是否生效, 关闭条件是否满足, 均执行定时器关闭事件, 并设置定时器活动标记为 `false`.

### 有条件执行定时器

```lua
    /Game.Run("EVENT_TIMER_EXECUTE_COND", 0, 0);
    /Game.Run("EVENT_TIMER_EXECUTE_COND", 0, TIME_STAMP);
    /Game.Run("EVENT_TIMER_EXECUTE_COND", 10001, 0);
    /Game.Run("EVENT_TIMER_EXECUTE_COND", 10001, TIME_STAMP);
```

* `arg_a`: 配置编号, `0`: 所有配置
* `arg_b`: 时间戳, `0`: 取当前时间

仅当定时器生效, 触发条件满足, 且定时器活动标记为 `false` 时, 执行定时器触发事件, 并设置定时器活动标记为 `true`.

### 有条件关闭定时器

```lua
    /Game.Run("EVENT_TIMER_TERMINATE_COND", 0, 0);
    /Game.Run("EVENT_TIMER_TERMINATE_COND", 0, TIME_STAMP);
    /Game.Run("EVENT_TIMER_TERMINATE_COND", 10001, 0);
    /Game.Run("EVENT_TIMER_TERMINATE_COND", 10001, TIME_STAMP);
```

* `arg_a`: 配置编号, `0`: 所有配置
* `arg_b`: 时间戳, `0`: 取当前时间

仅当定时器生效, 关闭条件满足, 且定时器活动标记为 `true` 时, 执行定时器关闭事件, 并设置定时器活动标记为 `false`.

### 玩家定时器

```lua
    /Game.Run("EVENT_TIMER_RESTORE", 0, 0, "pid");
    /Game.Run("EVENT_TIMER_RESTORE", 10001, TIME_SATAMP, "pid");
```

* `arg_a`: 配置编号, `0`: 所有配置
* `arg_b`: 玩家上一次下线时间戳, `0`: 取玩家数据, 非 `0`: 调试数据
* `pid`: 64 位整型参数, 字符串形式, 当前用户可留空

根据玩家下线时间计算定时器是否触发及触发次数.


### 聊天

```lua
    /Game.Run("EVENT_CHAT", [channel], [type], "", [target_id], [body]);
```

* `arg_a`: 聊天频道
  - `CHAT_CHANNEL_PERSONAL`
  - `CHAT_CHANNEL_WORLD`
* `arg_b`: 聊天内容类型(文本/语音/其余客户端自定义类型)
* `arg_64`: 私聊目标玩家ID
* `arg_str`: 聊天内容


### 创建容器

```lua
    /Game.Run("EVENT_CONTAINER_CREATE", [type], 0, "", 0, [name]);
```

* `arg_a`: 容器类型
  - `OBJECT_TEAM`
  - `OBJECT_GUILD`
* `arg_str`: 容器名称

### 加入容器

```lua
    /Game.Run("EVENT_CONTAINER_ADD", [type], 0, [cid], 0, "");
```

* `arg_a`: 容器类型
  - `OBJECT_TEAM`
  - `OBJECT_GUILD`
* `arg_64`: 容器ID(VARIABLE_SEGMENT_CONTAINER + type)

### 退出容器

```lua
    /Game.Run("EVENT_CONTAINER_DEL", [type], 0, [cid], 0, "");
```

* `arg_a`: 容器类型
  - `OBJECT_TEAM`
  - `OBJECT_GUILD`
* `arg_64`: 容器ID(VARIABLE_SEGMENT_CONTAINER + type)

### 删除容器

```lua
    /Game.Run("EVENT_CONTAINER_DESTROY", [type], 0, [cid], 0, "");
```

* `arg_a`: 容器类型
  - `OBJECT_TEAM`
  - `OBJECT_GUILD`
* `arg_64`: 容器ID(VARIABLE_SEGMENT_CONTAINER + type)

### 添加好友

```lua
    /Game.Run("EVENT_BUDDY_ADD", 0, 0, "", "[dst_id]");
```

* `arg_64`: 对方ID

### 删除好友

```lua
    /Game.Run("EVENT_BUDDY_DEL", 0, 0, "", "[dst_id]");
```

* `arg_64`: 好友ID

### 接收添加好友邀请

```lua
    /Game.Run("EVENT_BUDDY_ACCEPT", 0, 0, "", "[dst_id]");
```

* `arg_64`: 邀请者ID

### 拒绝添加好友邀请

```lua
    /Game.Run("EVENT_BUDDY_REFUSE", 0, 0, "", "[dst_id]");
```

* `arg_64`: 邀请者ID

### 添加好友黑名单

```lua
    /Game.Run("EVENT_BUDDY_BLOCK", 0, 0, "", "[dst_id]");
```

* `arg_64`: 对方ID


### 拉取好友列表

```lua
    /Game.Run("EVENT_BUDDY_LIST", 0, 0, "", "");
```

服务器通过GetAny.Res{}回复好友信息


### 更新排行榜

```lua
    /Game.Run("EVENT_RANK_SET", rank, score, "", "");
```
* `rank`: 排行榜类型
* `score`: 参与排名数值

### 刷新排行榜

```lua
    /Game.Run("EVENT_RANK_REFRESH", rank, solo, "", "reverse");
```
* `rank`: 排行榜类型
* `solo`: 是否单服排行榜，大于0时单服排行，否则全服
* `reverse`:  大于0时按从大到小排序，否则从小到大排序

### 刷新排行榜（发奖）

```lua
    /Game.Run("EVENT_RANK_SEAL", rank, solo, "", "reverse");
```
* `rank`: 排行榜类型
* `solo`: 是否单服排行榜，大于0时单服排行，否则全服
* `reverse`:  大于0时按从大到小排序，否则从小到大排序

### 更新排行榜（客户端通过http请求）

```lua
    https://api.91juice.com/v1/rank/set?uid=uid&server=server&type=rankType&score=score
    https://api.91juice.com/v1/rank/set?type=1002&score=1024&server=20701&uid=100010000000043106
```
* `uid`: 玩家ID
* `server`: 服务器ID
* `type`: 排行榜类型
* `score`:  排行数值


### 获取排行榜（客户端通过http请求）

```lua
    https://api.91juice.com/v1/rank?type=rankType&top=topSize&reverse=ifReverse
```
* `type`: 排行榜类型
* `top`:  排行榜数量
* `reverse`:  大于0时按从大到小排序，否则从小到大排序

### 获取玩家排行榜（客户端通过http请求）

```lua
    https://api.91juice.com/v1/rank/user?uid=uid&server=server&reverse=reverse&solo=solo&type=type
    https://api.91juice.com/v1/rank/user?uid=100010000000000736&server=20701&reverse=1&solo=1&type=0
```
* `uid`: 玩家ID
* `server`:  玩家所在服务器ID
* `solo`:  单服/全服排行标识，1为单服，否则全服
* `reverse`:  为1时按从大到小排序，否则从小到大排序
* `type`:  排行榜类型，为0返回当前玩家所有类型排行榜信息

### 排行榜http请求返回数据类型(JSON)

```lua
    msg.SetEvent_Res{}, 其中每项排名信息放在variable列表中，variable各字段含义如下
```
pid: 玩家ID，  idx:排行榜类型，  val_32  排名, val_64: 排名值,
* `pid`: 玩家ID
* `idx`: 排行榜类型
* `val_32`: 排名(rank)
* `val_64`: 排名值(val)
* `Val`:  玩家所在服务器ID,字符串形式


### 获取玩家简要信息

```lua
    https://api.91juice.com/v1/user/brief?id=idList&server=server
    https://api.91juice.com/v1/user/brief?id=100010000000043863&server=20701
```
* `idList`: 玩家ID列表，多个id用`,`分割
* `server`:  区服ID

