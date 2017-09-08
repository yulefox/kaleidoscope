# FAQ

----

## 更新日志

### 2017-01-12

* `[ADD]` 道具获取, 战斗属性

----

## 道具

#### Q: 获取道具的方式有哪些?

#### A: 任意事件均可触发道具获取, 获取道具最终通过两个事件完成:

    EVENT_ITEM_ADD              // 添加单个道具, 道具必须存在于 `cfg_item_base`
    EVENT_ITEM_GROUP_ADD        // 添加一组道具, 道具组必须存在于 `cfg_item_group`

关卡结束, 任务完成等常见事件的奖励道具获取直接配置到 `cfg_item_group`.

#### Q: 玩家战斗属性如何计算?

#### A: 玩家的战斗属性的组织结构如下:

    ATTR_USER --+----- ATTR_UPGRADE_LEVEL(user)
                |----- ATTR_ROLE --+----- ATTR_UPGRADE_LEVEL(role)
                |                  |----- ATTR_ITEM_ARMED --+----- ATTR_ITEM --+----- VARIABLE_SEGMENT_ITEM_ARMED(role)
                |                                           |                  |----- ATTR_UPGRADE_LEVEL(item)
                |                                           |                  |----- ATTR_UPGRADE_STAR(item)
                |                                           |                  |----- ATTR_UPGRADE_RANK(item)
                |                                           |                  |----- ATTR_UPGRADE_QUALITY(item)
                |                                           |                  ...
                |                                           |                  |----- ATTR_UPGRADE_EXTRA(item)
                |                                           |
                |                                           |----- ATTR_ITEM(role) ...
                |                                           ...
                |                                           |----- ATTR_ITEM(role) ...
                |
                |----- ATTR_ITEM_ARMED --+----- ATTR_ITEM --+----- VARIABLE_SEGMENT_ITEM_ARMED(user)
                                         |                  |----- ATTR_UPGRADE_LEVEL(item)
                                         |                  |----- ATTR_UPGRADE_STAR(item)
                                         |                  |----- ATTR_UPGRADE_RANK(item)
                                         |                  |----- ATTR_UPGRADE_QUALITY(item)
                                         |                  ...
                                         |                  |----- ATTR_UPGRADE_EXTRA(item)
                                         |
                                         |----- ATTR_ITEM(user) ...
                                         ...
                                         |----- ATTR_ITEM(user) ...

* 在装备穿卸(`EVENT_ITEM_ARM`, `EVENT_ITEM_UNARM`, `EVENT_ITEM_ADD_ARM`), 角色/装备属性等级变化(`EVENT_ATTR_LEVEL_SET`, `EVENT_ATTR_LEVEL_INC`, `EVENT_ATTR_LEVEL_DEC`), 重新计算玩家属性(`ATTR_USER`).

* 为避免重复计算, 可根据属性是否变化(根据时间戳判断)决定是否重新计算.

* 手动触发属性计算(`EVENT_ATTR_CALC`).

#### Q: 玩家的装备如何更换?

#### A:

#### Q: 

#### A:

## 场景

## 任务

## 随机数

```
```
