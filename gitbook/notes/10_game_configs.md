# 配置

**部分配置的细节在实现过程中可能会有调整!**

----

## 更新日志

### 2017-07-17

* `[ADD]` 变量配置

### 2017-07-14

* `[MOD]` 成长维度属性计算

### 2017-06-28

* `[MOD]` 道具成长消耗新增按成长维度/等级所需材料
* `[MOD]` 道具转换新增按成长维度/等级分解材料

### 2017-06-10

* `[MOD]` 商城配置

### 2017-05-16

* `[ADD]` 抽奖, 道具组添加后续触发事件

### 2017-01-12

* `[ADD]` 事件, 道具, 道具组, 场景, 任务, 属性配置说明
* `[ADD]` 道具, 场景, 任务编号均使用 6 位整数表示

----

## 事件基础(`cfg_event_base`)

```protobuf
    message EventBase {
        message Item {
            string brief = 1;               // 描述
            int32 evt = 2;                  // 前置事件类型
            int32 arg_a = 4;                // 前置事件参数 A
            int32 arg_b = 5;                // 前置事件参数 B
            int32 post_evt = 40;            // 触发事件类型
            int32 post_arg_a = 42;          // 触发事件参数 A
            int32 post_arg_b = 43;          // 触发事件参数 B
            string post_arg_str = 44;       // 触发事件字符串参数
        }
        repeated Item item = 1;
    }
```

### 索引

* `evt`
* `arg_a`
* `arg_b`

#### 前置事件(`evt`)

前置事件类型由一个 8 位整数表示.

### 说明

当前置事件发生时, 触发后置事件, 同一前置事件可以触发多个后置事件.

前置事件参数 `arg_a`, `arg_b` 配置为 `-1` 表示该参数可为任意值. 后置事件参数 `post_arg_a`, `post_arg_b` 配置为 `-1` 表示应用前置事件参数 `arg_a`, `arg_b` 触发后置事件.

事件的[相关介绍](10_game_events.html).

## 事件定时器(`cfg_event_timer`)

```protobuf
message EventTimer {                                                    
    message Item {                                                      
        int32 idx = 1;                  // ID                          
        string brief = 2;               // 描述                        
        bool available = 3;             // 是否生效                    
        int32 variable = 4;             // 相对系统变量: `VariableType`
        int32 type = 5;                 // 类型, 0: 仅服务器使用; 1: 服务器和用户均使用
        string spec = 9;                // 定时器时间配置              
        int32 life = 10;                // 生命周期(单位: 分钟)        
        int32 post_evt = 11;            // 触发事件类型                
        int32 post_arg_a = 12;          // 触发事件参数 A              
        int32 post_arg_b = 13;          // 触发事件参数 B              
        string post_arg_str = 14;       // 触发事件字符串参数          
        int32 term_evt = 15;            // 结束事件类型                
        int32 term_arg_a = 16;          // 结束事件参数 A              
        int32 term_arg_b = 17;          // 结束事件参数 B              
        string term_arg_str = 18;       // 结束事件字符串参数          
        string ext_arg = 56;            // 扩展参数                    
    }                                                                   
                                                                        
    repeated Item item = 1;                                             
}                                                                       
```

### 索引

- `idx`

### 核心实现

- 计算上一次触发时间戳
- 系统每分钟, 检查每一配置的变量值, 该触发未触发的触发, 该关闭未关闭的关闭
- 玩家上线时, 根据玩家上一次触发时间, 计算下线期间需要补记的触发次数并执行

定时器的时间配置方式参考 [cron](https://github.com/robfig/cron/blob/master/doc.go)

## 道具基础(`cfg_item_base`)

```protobuf
    message ItemBase {
        message Item {
            int32 idx = 1;                  // 道具编号
            string name = 2;                // 名称
            string icon = 3;                // 图标
            string model = 4;               // 模型
            int32 type = 5;                 // 类型
            int32 subclass = 6;             // 子类
            int32 cls = 7;                  // 职业
            string brief = 9;               // 描述
            string detail = 10;             // 获取途径
            int32 lvl = 15;                 // 使用等级
            int32 rank = 16;                // 品阶
            int32 quality = 17;             // 品质
            int32 max_limit = 21;           // 最大拥有上限
            int32 max_recover = 22;         // 自动回复上限
            int32 max_stack = 23;           // 堆叠上限
            int32 buy_price = 31;           // 购买价格(消耗不足时可购买)
            int32 sell_price = 32;          // 出售价格
            string ext_arg = 56;            // 客户端扩展参数
        }
        repeated Item item = 1;
    }
```

### 索引

* `idx`

#### 道具编号(`idx`)

道具编号由一个 6 位整数表示.

### 说明

## 道具转换(`cfg_item_transform`)

```protobuf
    message ItemTransform {
        message Item {
            int32 id = 1;                   // ID
            string brief = 2;               // 描述
            int32 type = 3;                 // 转换类型
            int32 src_subclass = 5;         // 源道具子类型
            int32 src_attr = 6;             // 源道具成长维度类型
            int32 src_lvl = 7;              // 源道具成长维度等级
            int32 src_num = 8;              // 源道具数量
            int32 src_idx_a = 11;           // 源道具类型1
            int32 src_num_a = 12;           // 源道具数量1
            int32 src_idx_b = 13;           // 源道具类型2
            int32 src_num_b = 14;           // 源道具数量2
            int32 src_idx_c = 15;           // 源道具类型3
            int32 src_num_c = 16;           // 源道具数量3
            int32 src_idx_d = 17;           // 源道具类型4
            int32 src_num_d = 18;           // 源道具数量4
            int32 src_idx_e = 19;           // 源道具类型5
            int32 src_num_e = 20;           // 源道具数量5
            int32 dst_rate_a = 21;          // 目标道具概率1       
            int32 dst_idx_a = 22;           // 目标道具类型1       
            int32 dst_num_a1 = 23;          // 目标道具数量1(MIN)  
            int32 dst_num_a2 = 24;          // 目标道具数量1(MAX)  
            int32 dst_rate_b = 25;          // 目标道具概率2       
            int32 dst_idx_b = 26;           // 目标道具类型2       
            int32 dst_num_b1 = 27;          // 目标道具数量2(MIN)  
            int32 dst_num_b2 = 28;          // 目标道具数量2(MAX)  
            int32 dst_rate_c = 29;          // 目标道具概率3       
            int32 dst_idx_c = 30;           // 目标道具类型3       
            int32 dst_num_c1 = 31;          // 目标道具数量3(MIN)  
            int32 dst_num_c2 = 32;          // 目标道具数量3(MAX)  
            int32 dst_rate_d = 34;          // 目标道具概率4       
            int32 dst_idx_d = 33;           // 目标道具类型4       
            int32 dst_num_d1 = 35;          // 目标道具数量4(MIN)  
            int32 dst_num_d2 = 36;          // 目标道具数量4(MAX)  
            int32 dst_rate_e = 37;          // 目标道具概率5       
            int32 dst_idx_e = 38;           // 目标道具类型5       
            int32 dst_num_e1 = 39;          // 目标道具数量5(MIN)  
            int32 dst_num_e2 = 40;          // 目标道具数量5(MAX)  
            string ext_arg = 56;            // 客户端扩展参数
        }
        repeated Item item = 1;
    }
```

### 索引

* `id`

#### ID(`id`)

与配置行一一对应.

### 说明

道具转换: 实现道具到道具多对多的转换逻辑, 最多支持 5 转 5.

装备分解, 带成长维度及等级限制的材料分解, 发消息时除需要指定道具转换配置行 ID 外, 还需要带上分解道具 ID 列表.

## 道具商城(`cfg_item_mall`)

```protobuf
message ItemMall {
    message Item {
        int32 id = 1;                   // 配置编号
        int32 mall = 2;                 // 商城类型
        int32 cate = 3;                 // 子组 ID(0: 固定商品)
        int32 num = 4;                  // 数量(0: 商品未上架或已下架)
        int32 weight = 5;               // 权重(0: 无法随机到)
        string name = 10;               // 名称
        int32 dst_idx = 11;             // 目标道具索引
        int32 dst_num = 12;             // 目标道具数量
        int32 src_idx = 13;             // 源道具索引
        int32 src_num = 14;             // 源道具数量(原价)
        int32 discount = 15;            // 显示折扣
        int32 status = 16;              // 状态(客户端定义并使用: 新品/推荐等)
        int32 var_idx = 17;             // 购买数量变量
        int32 var_num = 18;             // 购买数量上限值
        int32 limit_var_a_idx = 21;     // 限制条件变量
        int32 limit_var_a_num = 22;     // 限制条件变量上限值
        int32 limit_var_b_idx = 23;     // 限制条件变量
        int32 limit_var_b_num = 24;     // 限制条件变量上限值
        string ext_arg = 56;            // 客户端扩展参数
    }
    repeated Item item = 1;
}
```

### 索引

* `id`

#### ID(`id`)

与配置行一一对应.

### 说明

## 道具组(`cfg_item_group`)

```protobuf
    message ItemGroup {
        message Item {
            int32 evt = 1;                  // 前置事件类型
            int32 arg_a = 2;                // 前置事件参数 A
            int32 arg_b = 3;                // 前置事件参数 B
            string brief = 4;               // 描述
            int32 cate = 5;                 // 子组 ID(同一子组概率互斥, 不同子组概率独立)
            int32 cls = 6;                  // 职业
            int32 rate = 10;                // 概率
            int32 item_idx = 11;            // 道具编号
            int32 item_num_min = 12;        // 道具最小数量
            int32 item_num_max = 13;        // 道具最大数量(为 0 时, 采用 item_num_min)
            int32 var_idx_a = 21;           // 道具变量 A
            int32 var_val_a = 22;           // 道具变量值 A
            int32 var_idx_b = 23;           // 道具变量 B
            int32 var_val_b = 24;           // 道具变量值 B
            int32 hit_variable = 30;        // 道具获取变量 ID
            int32 hit_threshold = 31;       // 道具获取变量阈值(低于此阈值不可获取)
            int32 hit_rate_inc = 32;        // 超过阈值后每次概率增加值(`10000`, 直接获取, 且变量清 `0`)
            int32 post_evt = 40;            // 触发事件类型
            int32 post_arg_a = 42;          // 触发事件参数 A
            int32 post_arg_b = 43;          // 触发事件参数 B
            string post_arg_str = 44;       // 触发事件字符串参数
        }
        repeated Item item = 1;
    }
```

### 索引

* `event`
* `arg_a`
* `arg_b`

### 说明

道具组获取通过 `事件 + 参数 A + 参数 B` 的方式实现.

一个道具组(和事件对应)由若干个(1-N)道具子组(`cate`)构成, 每个道具子组最多获得一种道具, 道具子组间的道具获取相互独立.

道具子组内的道具获取根据概率(`rate`, 万分比)进行排他计算, 同一道具子组的概率之和不大于 `10000`.

道具获取计算流程如下:

1. 根据事件过滤出满足条件的所有配置行.

2. 通过概率计算出所命中的道具子组的配置行(当同一道具子组的概率之和小于 `10000` 时, 可能无法命中), 未命中时, 转 2, 计算下一子组, 当所有子组计算完毕, 转 8.

3. 未配置道具获取变量(`hit_variable`)时, 直接获得道具, 转 6.

4. 道具获取变量(`hit_variable`)小于阈值(`hit_threshold`, 为 `0` 代表无阈值), 不获得道具, 变量 `hit_variable += 1`, 转 2.

4. 道具获取概率增加值(`hit_rate_inc`, 为 `10000`, 直接获取)满足 `rand(1, 10000) <= (hit_variable - hit_threshold + 1) * hit_rate_inc`, 获得道具, `hit_variable` 清 `0`, 转 5. 否则不获得道具, 变量 `hit_variable += 1`, 转 2.

5. 道具数量为 `rand(item_num_min, item_num_max)`.

6. 未配置道具变量 `var_idx_a` 及 `var_idx_b`, 该子组道具添加完毕, 转 2.

7. 为道具设置变量 `var_idx_a`, `var_idx_b`, **注意**: 道具的数量只能为 `1`, 且该道具不可堆叠, 该子组道具添加完毕, 转 2.

8. 触发事件 `post_evt(arg_a, arg_b)`.

9. 结束.

### 示例

#### 关卡 `100101` 的首次三星通关奖励

* 关卡结束: `EVENT_SCENE_END,100101,-1,...`
* 通关: `EVENT_SCENE_PASS,100101,-1,...`
* 首次通关: `EVENT_SCENE_PASS_1,100101,-1...`
* 每日首次通关: `EVENT_SCENE_PASS_0,100101,-1...`
* 三星通关: `EVENT_SCENE_PASS,100101,3,...`
* 首次三星: `EVENT_SCENE_PASS_1,100101,3,...`
* 每日首次三星: `EVENT_SCENE_PASS_0,100101,3,...`

#### 任务 `100001` 的完成奖励

* 任务完成: `EVENT_QEUST_STATUS_SET,100001,QUEST_STATUS_SUCCESS,...`
* 任务进度: `EVENT_QEUST_PROGRESS_SET,200001,1,...`

## 场景基础(`cfg_scene_base`)

```protobuf
    message SceneBase {
        message Item {
            int32 idx = 1;                  // 场景编号
            string name = 2;                // 场景名称
            string brief = 3;               // 描述
            int32 lvl = 4;                  // 等级限制
            int32 type = 5;                 // 场景类型(大厅, 战斗, 竞技场)
            int32 cate = 6;                 // 场景子类型(普通/精英/魔王...)
            int32 sn = 7;                   // 场景序号
            string model = 8;               // 模型
            string mode = 9;                // 难度模式
            int32 pre = 10;                 // 前置关卡
            int32 min_eff = 11;             // 最小战力
            int32 recomm_eff = 12;          // 推荐战力
            string icon = 13;               // 场景图标
            string boss = 14;               // BOSS 图标
            int32 chapter = 15;             // 关卡所属章节
            int32 cost_enter_idx_a = 20;    // 进入时消耗
            int32 cost_enter_num_a = 21;    // 进入时消耗
            int32 cost_enter_idx_b = 22;    // 进入时消耗
            int32 cost_enter_num_b = 23;    // 进入时消耗
            int32 cost_leave_idx_a = 24;    // 离开时消耗
            int32 cost_leave_num_a = 25;    // 离开时消耗
            int32 cost_leave_idx_b = 26;    // 离开时消耗
            int32 cost_leave_num_b = 27;    // 离开时消耗
            int32 cond_type_1 = 30;         // 1 星条件
            int32 cond_arg_1 = 31;          // 1 星参数
            int32 cond_type_2 = 32;         // 2 星条件
            int32 cond_arg_2 = 33;          // 2 星参数
            int32 cond_type_3 = 34;         // 3 星条件
            int32 cond_arg_3 = 35;          // 3 星参数
            string cond_script = 36;        // 通关判定脚本
            string music = 40;              // 起始音乐
            string music_boss = 41;         // boss音乐
            string ext_arg = 56;            // 客户端扩展参数
        }
        repeated Item item = 1;
    }
```

### 索引

* `idx`

#### 场景编号(`idx`)

场景编号由一个 6 位整数表示.

### 说明

关卡奖励配置在 `cfg_item_group` 中.

## 场景属性(`cfg_scene_attr`)

```protobuf
    message SceneAttr {                                                       
        message Item {                                                        
            int32 cate = 1;                 // 关卡子类型                     
            string brief = 2;               // 描述                           
            int32 type = 4;                 // 变量类型                       
            int32 cd_occasion = 5;          // 计算 CD 的时机                 
            int32 cd_time = 6;              // CD 时间                        
            int32 ticket_occasion = 9;      // 扣减门票的时机                 
            int32 variable = 10;            // 关联的系统变量(0 则永久开放, 开关)
            int32 camp_max = 11;            // 最大阵营/队伍数                
            int32 role_max = 12;            // 队伍内最大人数
            int32 reward_type = 20;         // 0=正常奖励，1=翻牌奖励         
            int32 auto_vip = 22;            // 扫荡vip限制
            int32 auto_cost_idx = 23;       // 扫荡消耗类型                   
            int32 auto_cost_num = 24;       // 扫荡消耗数量                   
        }   
        repeated Item item = 1;
    }   
```

### 索引

* `cate`

## 任务基础(`cfg_quest_base`)

```protobuf
    message QuestBase {
        message Item {
            int32 idx = 1;                  // 任务编号
            int32 parent = 2;               // 父任务编号
            string name = 3;                // 任务名称
            int32 lvl = 4;                  // 等级限制
            int32 variable_sys = 5;         // 关联系统变量(开关)
            int32 variable_user = 6;        // 关联玩家变量(开关)
            string brief = 10;              // 描述
            int32 type = 11;                // 任务类型
            int32 progress = 12;            // 任务进度
            string ext_arg = 56;            // 客户端扩展参数
        }
        repeated Item item = 1;
    }
```

### 索引

* `idx`

#### 任务编号(`idx`)

任务编号由一个 6 位整数表示.

### 说明

任务奖励配置在 `cfg_item_group` 中.

不再支持自动完成的任务, 可通过系统变量实现.

## 属性组(`cfg_attr_group`)

```protobuf
    message AttrGroup {                                                                         
        message Item {                                                                          
            string brief = 1;               // 描述                                             
            int32 type = 2;                 // 类型                                             
            int32 idx = 3;                  // 编号                                             
            int32 lvl = 4;                  // 等级                                             
            int32 dep = 5;                  // 依赖成长维度                                     
            int32 rand_type = 6;            // 随机抽取类型(0: 所有, 1: 不放回选取, 2: 放回选取)
            int32 rand_num = 7;             // 随机抽取数量                                     
            int32 attr = 9;                 // 属性类型                                         
            int32 weight = 10;              // 属性权重(0: 无法随机到)                          
            int32 rate = 11;                // 概率                                             
            int32 attr_val_min = 12;        // 属性最小值                                       
            int32 attr_val_max = 13;        // 属性最大值(为 0 时, 采用 attr_val_min)           
            string ext_arg = 56;            // 客户端扩展参数                                   
        }                                                                                       
        repeated Item item = 1;                                                                 
    }                                                                                           
```

### 索引

* `type`
* `idx`
* `lvl`

#### 属性索引(`idx`)

用户的属性索引为 `OBJECT_USER(1001)`, 角色的属性索引为角色职业编号, 道具的属性索引为道具编号或索引(`ItemMap` 多个道具使用同一索引).

### 说明

## 维度成长(`cfg_upgrade_base`)

```protobuf
    message UpgradeBase {
        message Item {                                             
            int32 id = 1;                   // ID                  
            int32 idx = 2;                  // 编号                
            string brief = 3;               // 描述                
            int32 type = 4;                 // 类型                
            int32 lvl = 5;                  // 等级                
            int32 role_lvl = 6;             // 强化所需角色等级    
            bool mark_cost = 7;             // 是否记录累积消耗    
            int32 pattern = 8;              // 消耗路线            
            int32 cost_fix_idx_a = 11;      // 必选消耗类型1       
            int32 cost_fix_num_a = 12;      // 必选消耗数量1       
            int32 cost_fix_idx_b = 13;      // 必选消耗类型2       
            int32 cost_fix_num_b = 14;      // 必选消耗数量2       
            int32 cost_fix_idx_c = 15;      // 必选消耗类型3       
            int32 cost_fix_num_c = 16;      // 必选消耗数量3       
            int32 cost_fix_subclass = 17;   // 必选消耗道具子类型       
            int32 cost_fix_attr = 18;       // 必选消耗道具成长维度类型 
            int32 cost_fix_lvl = 19;        // 必选消耗道具成长维度等级 
            int32 cost_fix_num = 20;        // 必选消耗道具数量         
            int32 cost_opt_idx = 25;        // 可选消耗类型        
            int32 cost_opt_num = 26;        // 可选消耗数量        
            int32 rate = 30;                // 成功概率            
            int32 inc_exp = 31;             // 增加经验值          
            int32 downgrade = 32;           // 强化失败降低等级    
            int32 exp = 33;                 // 升级经验            
            bool reset_exp = 34;            // 升级后经验是否清 0  
            int32 promoted_delta = 40;      // 道具进阶后索引增加值
            string script = 54;             // 触发脚本            
            string ext_arg = 56;            // 客户端扩展参数      
        }                                                          
        repeated Item item = 1;
    }
```

### 索引

* `id`
* `idx + type + lvl`

#### 任务编号(`idx`)

任务编号由一个 6 位整数表示.

### 说明

用户/角色/道具的成长消耗配置在 `cfg_upgrade_base` 中. 支持线性插值, 限制如下:

- 配置行在数据表中的顺序由第一列的 `id` 决定.
- 同一成长维度/同一消耗路线的配置行**必须连续正增长**.
- 需要进行插值计算的项(如等级为 `16`), 其插值的上一项(如等级为 `10`)及下一项(如等级为 `20`)必须存在, 且消耗道具编号一致.

## 道具索引(`cfg_item_map`)

```protobuf
    message ItemMap {
        message Item {
            int32 idx = 1;                  // 道具编号
            string brief = 3;               // 描述
            int32 type = 5;                 // 属性类型
            int32 cost_idx = 7;             // 消耗索引编号
            int32 attr_idx = 8;             // 属性索引编号
            string ext_arg = 56;            // 客户端扩展参数
        }
        repeated Item item = 1;
    }
```

### 索引

* `idx`
* `type`

#### 道具编号(`idx`)

道具编号由一个 6 位整数表示, 对应一个可成长的装备/技能等.

#### 属性类型(`type`)

成长维度, 以 `AttrType` 标识, 为 `0` 表示该道具所有成长维度适用该映射.

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

### 说明

当多个道具的成长消耗或属性配置相同时, 可通过道具映射获取对应索引编号.

## 变量基础(`cfg_variable_base`)

```protobuf
    message VariableBase {
        message Item {
            int32 idx = 1;                  // 变量类型
            string brief = 2;               // 描述
            int32 val = 4;                  // 数值
            int32 var_idx = 7;              // 关联变量类型
            int32 var_val = 8;              // 关联变量数值
            string ext_arg = 56;            // 客户端扩展参数
        }
        repeated Item item = 1;
    }
```

### 说明

- `var_idx`: 关联变量类型
  - `0`: 作为常量使用(等同<疾风剑魂>的 `cfg_counter_base`)
  - `-1`: 作为增量配置(等同<疾风剑魂>的 `cfg_counter_inc`)
  - `>0`: 取值随关联变量不同而不同(扩展<疾风剑魂>的 `cfg_counter_vip` 及 `cfg_counter_guild`, 且不限关联变量类型)
- `var_val`: 关联变量数值, **分段取值, 非插值**
  - `0`: 作为常量使用(等同<疾风剑魂>的 `cfg_counter_base`)

