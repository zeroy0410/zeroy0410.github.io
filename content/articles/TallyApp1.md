---
title: "Flask学习1 TallyApp beta 0.9"
url: ["articles/TallyApp1"]
date: 2022-02-01T19:35:39+08:00
draft: false
categories: ["Python-Flask"]
---

#### 功能描述

1. 支持注册和登录
2. 支持简单的分类记账
3. 支持以饼图的形式展现各个分类占总体收支的数目
4. 支持增删改数据
5. 支持以一定的xlsx格式导入导出数据

#### 基本结构

![](/Z-Tally.svg)

[Demo](http://114.55.111.14:8080/)
[项目地址](https://github.com/zeroy0410/TallyApp)

#### 技术路线

后端：[python-Flask](https://www.youtube.com/watch?v=MwZwr5Tvyxo&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH&ab_channel=CoreySchafer)

前端：[BootStrap](https://getbootstrap.com/docs/5.1/getting-started/introduction/)

#### 踩过的坑

1. 程序开始时数据库需要已经初始化完毕`db.create_all()`
2. 使用get方法传参会出未知问题，故全部改为使用url传参
3. 浮点误差会让数据很奇怪，注意保留两位小数
4. 不同的数据类型（pandas与string）可能会让数据显示异常（空数据显示为'None'）

#### Docker应用部署细节

Flask本身不带服务器，使用gunicorn来使得web应用能够在服务器上被访问。

使用阿里云作为Docker Hub。

```bash
#注册完阿里云的镜像服务之后
#登录
docker login --username={{your username}} registry.cn-hangzhou.aliyuncs.com/
#命名并上传本地docker镜像
docker tag tallyapp registry.cn-hangzhou.aliyuncs.com/tally_app/tallyapp:{{version}}
docker push tallyapp registry.cn-hangzhou.aliyuncs.com/tally_app/tallyapp:{{version}}
#拉取镜像
docker pull tallyapp registry.cn-hangzhou.aliyuncs.com/tally_app/tallyapp:{{version}}
```

将本地数据库挂载到Docker容器中，并运行容器。

```bash
docker run -d -p 8080:8080 -v /database:/soft/TallyApp/database {{images_id}}
```
