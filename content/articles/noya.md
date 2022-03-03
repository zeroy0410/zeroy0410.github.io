---
title: "基于go-cqhttp的机器人NoyaBot"
date: 2022-03-03T10:04:25+08:00
draft: false
categories: ["WEB"]
url: "articles/noya"
---

#### 前言

2月14情人节过于孤独，于是萌生了写个qqbot玩的想法。

#### 概述

**项目地址：**[zeroy0410/NoyaBot (github.com)](https://github.com/zeroy0410/NoyaBot)

配置完[go-cqhttp](https://docs.go-cqhttp.org/)的基本信息之后，就可以用它的api来操纵bot的账号进行各种操作，同时go-cqhttp会转发接收到的信息到指定端口。只需要在本地搭建一个服务器对收到的信息进行一定规则的回复即可。

我使用了Python-Flask作为项目的框架。

**机器人功能（截止2022/3/3）**

- 闲聊
- - 回答指定的问题
  - 设定回答问题的概率
- 数学计算
- - 计算能用一行字符串表示的Sympy库格式的数据
- 一言
- 翻译

```bash
/teach A|B #当输入为A时以B来回答
/let talk_enable (True or False) #是否在群内开启闲聊
/let talk_probability 一个浮点数 #闲聊时接话的概率
/ask A #问话就会回答（无视上面两条指令的限制）
/calc sympy库格式的一条算式 #不要尝试计算复杂度过高的式子，计算时间过长会阻塞进程
/hito 参数# 一言参数参考https://hitokoto.cn/
/trans 内容|from|to #如trans Hello World!|en|zh 英译中
```

#### 注意事项

数学计算功能使用了eval函数让python能够解析输入的代码，我过滤掉了大部分常用的注入语句，但仍有被注入的风险。

