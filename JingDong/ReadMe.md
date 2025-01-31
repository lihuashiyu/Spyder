### `1.` 安装  `Python`，支持 `Python 3.8+`


### `2.` 安装  `Python`  相关第三方库，命令如下：

```shell
    pip install requests
    pip install pymysql
    pip install scrapy
    pip install bs4
```


### `3.` 使用连接工具，连接  `Mysql`  创建数据库和表：

```mysql
    -- 创建数据库
    -- drop database if exists test;
    -- create database if not exists test default charset = "utf8mb4";
    -- use test;
    
    -- 商品描述和评价数据
    drop table if exists ods_jingdong_product;
    create table if not exists ods_jingdong_product
    (
        sku_id                 varchar(16)    primary key  comment '商品 ID',
        store                  varchar(32)                 comment '店铺名称',
        product_price          varchar(8)                  comment '商品价格',
        guide_price            varchar(8)                  comment '商品指导价',
        original_price         varchar(8)                  comment '商品原价',
        brand                  varchar(32)                 comment '品牌',
        description            varchar(2048)               comment '商品详细参数介绍',
        url                    varchar(128)                comment '商品详情页链接',
        comment_count          varchar(64)                 comment '全部评价数量',
        favorable_rate         varchar(6)                  comment '好评度',
        comment_target         varchar(2048)               comment '评价标签',
        show_picture_count     varchar(6)                  comment '晒图数量',
        show_video_count       varchar(6)                  comment '视频晒单数量',
        add_comment_count      varchar(6)                  comment '追评数量',
        better_comment_count   varchar(6)                  comment '好评数量',
        general_comment_count  varchar(6)                  comment '中评数量',
        bed_comment_count      varchar(6)                  comment '差评数量'
    ) engine = InnoDB default charset = "utf8mb4" comment '商品描述和评价数据';
```

```mysql
    -- 用户对商品的评论数据
    drop table if exists ods_jingdong_comment;
    create table if not exists ods_jingdong_comment
    (
        id                  int(16)        primary key  auto_increment,
        sku_id              varchar(16)                 comment '商品 ID',
        user_id             varchar(16)                 comment '用户 ID',
        user_guid           varchar(32)                 comment '用户 GUID',
        user_name           varchar(8)                  comment '用户名字',
        user_head_url       varchar(256)                comment '用户头像 url',
        user_level          varchar(4)                  comment '用户等级',
        score               varchar(2)                  comment '对商品评分',
        buy_time            varchar(24)                 comment '购买时间',
        comment_time        varchar(24)                 comment '留言时间',
        item_description    varchar(128)                comment '商品描述',
        content             varchar(2048)               comment '评论内容',
        imagine_count       varchar(2)                  comment '图片数量',
        imagine_info        varchar(1024)               comment '图片信息',
        video_count         varchar(2)                  comment '视频数量',
        video_info          varchar(1024)               comment '视频信息',
        like_count          varchar(4)                  comment '评论点赞数',
        reply_count         varchar(4)                  comment '评论回复数',
        add_comment_content varchar(2048)               comment '追评内容'
    ) engine = InnoDB auto_increment = 1 default charset = "utf8mb4" comment '用户对商品的评论数据';
```

```mysql
    select * from ods_jingdong_product;
    select * from ods_jingdong_comment;
    select count(*) from ods_jingdong_comment;
```


### `4.` 修改配置文件：
主要配置文件在 `settings.py`中：

```yaml
138-139 行:
    # 查询的页码
    MAX_PAGE = 50
```

```yaml
140-163 行:
    # 登录后用户 cookie
    USER_COOKIE = { *** }
    将对应的信息修改为自己的京东数据
```

```yaml
178-185 行:
    # Mysql 配置
    MYSQL_HOST = '127.0.0.1'
    MYSQL_PORT = 3306
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = '111111'
    MYSQL_DB_NAME = 'test'
    MYSQL_CONNECT_CHARSET = 'utf8'
```


### `5.` 运行爬虫：
```bash
# 首先切换到项目路径下：    
    cd Spider/crawler/spiders/
     
# 然后： 
    scrapy crawl JingDong
```
