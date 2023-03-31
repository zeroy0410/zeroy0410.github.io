# 数据库基础|JDBC入门|Druid连接池的简单配置


### 数据库基础

#### 增

**新建数据库**

```mysql
CREATE DATABASE {{name}}
```

**新建数据表**

```mysql
CREATE TABLE {{name}}(
{{列名}} {{数据类型}} {{约束}},
.....
);

EXAMPLE:
CREATE TABLE Users(
id int primary key,
name varchar(30) NOT NULL,
birthday date,
score int NOT NULL
);
```

**添加外键约束**

建表时添加

```mysql
CONSTRAINT {{键名}} FOREIGN KEY({{当前表列名}}) REFERENCES {{别的表(别的表列名)}}
```

建表后添加

```mysql
alter table {{表名}} add CONSTRAINT {{键名}} FOREIGN KEY({{当前表列名}}) REFERENCES {{别的表(别的表列名)}}
```



**插入元素**

```mysql
EXAMPLE:
向一张名为users的数据表中插入元素：
INSERT INTO users(id,name,birthday,score) VALUES
(1,'zeroy','2003-4-10',100) ,
(2,'admin','2003-4-10',99) 
```

#### 查

```mysql
SELECT {{列名}}
FROM {{表名}}
WHERE {{条件}}
GROUP BY {{分组字段}}
HAVING {{分组后条件}}
ORDER BY {{排序字段}}
LIMIT {{分页限定}}
```

#### 改

```mysql
UPDATE {{表名}} set {{程序语句}} WHERE {{条件}}
```

#### 事务

事务能实现多条命令捆绑，一旦失败，会回滚所有操作。

```mysql
-- 开启事务
BEGIN;
-- 回滚事务
ROLLBACK;
-- 提交事务
COMMIT;
```

#### 数据库设计

**一对多**

如博客系统一个用户对应多篇文章，需要在文章表处引一条外键连向数据表。

**多对多**

如购物系统中一个商品对应多个订单，一个订单也被多个商品所共有。

实现方式：新建一张表引出两条外键分别连向商品表和订单表的主键，这张数据表的一行代表一件商品与一张订单之间的关系。

**一对一**

用于表拆分，提升常用信息的访问速度。



### JDBC入门

#### 简介

**Java数据库连接**，（**Java Database Connectivity**，简称**JDBC**）是[Java语言](https://zh.wikipedia.org/wiki/Java语言)中用来规范[客户端](https://zh.wikipedia.org/wiki/客户端)程序如何来访问[数据库](https://zh.wikipedia.org/wiki/数据库)的[应用程序接口](https://zh.wikipedia.org/wiki/应用程序接口)，提供了诸如查询和更新数据库中数据的方法。JDBC也是[Sun Microsystems](https://zh.wikipedia.org/wiki/Sun_Microsystems)的[商标](https://zh.wikipedia.org/wiki/商标)[[1\]](https://zh.wikipedia.org/wiki/Java数据库连接#cite_note-1)。JDBC是面向[关系型数据库](https://zh.wikipedia.org/wiki/关系型数据库)的。

#### 步骤

**注册驱动**

```java
Class.forName("com.mysql.jdbc.Driver")
```

**获取连接对象**

```java
Connection conn= DriverManager.getConnection("jdbc:mysql://127.0.0.1:3306/{{数据库名}}","username","password");
```

**获取连接状态**

有两种方式，后者可以预处理sql模板。

```java
String sql="SELECT * FROM customers";//查询sql语句
Statement stmt=conn.createStatement();
PreparedStatement pstmt=conn.prepareStatement(sql);
```

**发送查询请求**

```java
ResultSet rs=stmt.executeQuery(sql);
Resultset rs=pstmt.executeQuery();
```

**将查询请求封装为对象储存**

```java
while(rs.next()) {
    Customer customer = new Customer();
    int customerId = rs.getInt("customer_id");
    String firstName = rs.getString("firstName");
    String lastName = rs.getString("lastName");
    Date birthDate = rs.getDate("birthDate");
    int points = rs.getInt("points");
    customer.setId(customerId);
    customer.setBirthDate(birthDate);
    customer.setFirstName(firstName);
    customer.setLastName(lastName);
    customer.setPoints(points);
    customers.add(customer);
}
```

**使用PreparedStatement模板查询或修改数据**

使用`？`作为占位符，在后续代码中再进行数据填充。

```java
String sql="insert customers(first_name,last_name,birth_date,points,address,city,state) value(?,?,?,?,?,?,?);";
PreparedStatement pstmt=conn.prepareStatement(sql);
pstmt.setString(1,firstName);
pstmt.setString(2,lastName);
pstmt.setDate(3,birthDate);
pstmt.setInt(4,points);
pstmt.setString(5,addtress);
pstmt.setString(6,city);
pstmt.setString(7,state);
```

这样做的优点是可以预防SQL注入。

PreparedStatement对象会对输入的字符串做转义处理，可以防止原理为简单字符串拼接生效的SQL注入。（当然还有模板注入防不了）

### Druid数据库连接池的简单使用

#### 简介

在[软件工程](https://zh.wikipedia.org/wiki/软件工程)中，**连接池**（英语：connection pool）是维护的[数据库连接](https://zh.wikipedia.org/wiki/数据库连接)的缓存，以便在将来需要对数据库发出请求时可以重用连接。 连接池用于提高在数据库上执行命令的性能。为每个用户打开和维护数据库连接，尤其是对动态数据库驱动的[网站](https://zh.wikipedia.org/wiki/網站)应用程序发出的请求，既昂贵又浪费资源。在连接池中，创建连接之后，将连接放在池中并再次使用，这样就不必创建新的连接。如果所有连接都正在使用，则创建一个新连接并将其添加到池中。连接池还减少了用户必须等待创建与数据库的连接的时间。

Druid是由阿里巴巴开发的数据库连接池。

#### 配置文件的书写

```properties
driverClassName=com.mysql.jdbc.Driver
url={{数据库地址}}
username={{your username}}
password={{your password}}
# 默认连接数
initialSize=5
# 最大连接数
maxActive=10
# 最长等待时间
maxWait=3000
```

#### 从数据库连接池中获取连接

```java
Properties prop=new Properties();
prop.load(new FileInputStream("src/druid.properties"));//填写druid配置文件的路径
DataSource dataSource= DruidDataSourceFactory.createDataSource(prop);
Connection conn=dataSource.getConnection();
```


