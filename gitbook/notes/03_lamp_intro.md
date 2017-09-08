# 管理模板

[gentelella](https://github.com/puikinsh/gentelella) 是 GitHub 上关注度最高的一个管理模板。

我用 Laravel 实现了一版。

## 初始化项目

    composer create-project laravel/laravel gentelellamp --prefer-dist "5.1.*"

## 基本配置

* [数据库](http://laravel-china.org/docs/5.1/database#configuration)
* [缓存](http://laravel-china.org/docs/5.1/cache#configuration)
* [会话](http://laravel-china.org/docs/5.1/session#configuration)

## 依赖项

Node 依赖项存在于 `package.json` 文件中：

* [gulp](http://gulpjs.com)
* [elixir](http://laravel-china.org/docs/5.1/elixir)
* [bootstrap](http://www.bootcss.com)
* [gentelella](https://github.com/puikinsh/gentelella)

注意：

如果使用 elixir 的 `browserify` 遇到异常，参照该 [issue](https://github.com/laravel/elixir/issues/354)。

PHP 依赖项存在于 `composer.json` 文件中：

* [graham-campbell/markdown](https://github.com/GrahamCampbell/Laravel-Markdown)

## 导入 gentelella

将 gentelella 导入项目中，目录结构如下：

    |---- public/
    |   |---- build/
    |   |---- css/
    |   |---- js/
    |   |---- vendors/
    |       |---- bootstrap/
    |       |---- Chart.js/
    |       |---- datatables.net/
    |       |---- Flot/
    |       |---- font-awesome/
    |       |---- gentelella/
    |       |---- iCheck/
    |---- resources
        |---- assets/
        |---- lang/
        |---- views/
            |---- errors/
            |---- layouts/
            |   |---- blank.blade.php
            |   |---- footer.blade.php
            |   |---- header.blade.php
            |   |---- master.blade.php
            |---- vendor/
                |---- gentelella/
                    |---- calendar.blade.php
                    |---- form.blade.php
                    |---- icons.blade.php
                    |---- index.blade.php

## 改（作）造（死）

借助 Laravel 的 [blade 模板](http://laravel-china.org/docs/5.1/blade)，将重复的 html 代码抽离到 `layouts` 中。 

## 导航

[entrust]()

## 脚本

将 shell 与 Larabel 提供的 envoy、schedule 结合，实现一些特定功能。

## 发布

[扩展包](http://laravel-china.org/docs/5.1/packages)

----

## 业务

### 日志

rsync

日志流水动态显示

### 统计

`http://localhost/api/api_name`

### 后台

开放查询与签名验证

### 日历

日历事件：

* 开服
* 合服
* 维护

    mysql -ujuice -pJuice@2015 agame_god -e 'INSERT INTO `dat_command` (`cmd`, `server`) VALUES (\'res_code = Game.TriggerEvent(102528, 2032, 1, '', '')\', 20101);'
