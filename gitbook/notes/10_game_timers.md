# 定时器

----

## 更新日志

### 2017-03-03

* `[ADD]` 定时器实现方案设计

----

## 简述

定时器是依赖于系统时间触发相应事件的逻辑机制.

以触发时间分类:

* 绝对时间触发: 按系统时间触发

* 相对时间触发: 相对某个时间戳(`variable.stamp`)的偏移时间

以执行逻辑分类:

* 以服务器为主体触发:

* 以玩家为主体触发:

* 两者皆触发:

### 定时器类型

    enum TimerType {
        TIMER_NONE                                  = 0;        // 无
        TIMER_ABSOLUTE_SERVER                       = 1;        // 针对服务器
        TIMER_ABSOLUTE_PLAYER                       = 2;        // 针对玩家
        TIMER_ABSOLUTE_BOTH                         = 3;        // 针对服务器及玩家
        TIMER_RELATIVE_SERVER                       = 4;        // 相对服务器
        TIMER_RELATIVE_PLAYER                       = 5;        // 相对玩家
    }

### 生命周期

### 配置

    message EventTimer {
        message Item {
            int32 idx = 1;                  // 定时器 ID
            string brief = 2;               // 描述
            int32 type = 3;                 // 定时器类型: `TimerType`
            int32 variable = 4;             // 关联的系统/玩家变量: `VariableType`
            string cron_expr = 6;           // cron 配置
            int32 life = 15;                // 生命周期(单位: 分钟)
            int32 evt_s = 17;               // 开始事件类型
            int32 evt_s_arg_a = 18;         // 开始事件参数
            int32 evt_s_arg_b = 19;         // 开始事件参数对应的数值(如道具数量, 变量数值)
            int32 evt_e = 21;               // 结束事件类型
            int32 evt_e_arg_a = 22;         // 结束事件参数
            int32 evt_e_arg_b = 23;         // 结束事件参数对应的数值(如道具数量, 变量数值)
            string ext_arg = 56;            // 客户端扩展参数
        }

        repeated Item item = 1;
    }


