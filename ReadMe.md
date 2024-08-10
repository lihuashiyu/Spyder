## <center>实用的爬虫程序

<br>

### `1.` 结构目录

```shell
    Spider
    ├── JingDong                                                     # 爬取 JingDong 数据
    │       ├── crawler                                              # 爬虫主程序
    │       │       ├── __init__.py                                   
    │       │       ├── items.py                                     
    │       │       ├── middlewares.py                                
    │       │       ├── pipelines.py                                  
    │       │       ├── settings.py                                   
    │       │       └── spiders                                       
    │       ├── ReadMe.md                                             
    │       └── scrapy.cfg                                            
    │
    ├── LICENSE                                                      # GPL v3 协议
    │
    ├── ReadMe.md                                                    # 项目说明
    │
    └── V2Ray                                                        # 爬取互联网节点
            └── TelegramNode.py                                      # 从 TG 爬取节点
```

<br>

### `2.` 项目说明：
    
    本项目可能存在版权风险，禁止一切商用行为，仅供个人学习、使用