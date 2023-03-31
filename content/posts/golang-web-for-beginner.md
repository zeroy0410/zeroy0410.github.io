---
title: "Golang|Gin Web development for Beginners"
date: 2022-02-11T16:31:25+08:00
url: "articles/Golang-web1"
categories: ["golang-web"]
draft: false
---

#### 自带的net/http库的使用

http库提供了HTTP服务的用户端和服务端的实现。

[官方文档](https://pkg.go.dev/net/http)

[Go语言基础之net/http | 李文周的博客 (liwenzhou.com)](https://www.liwenzhou.com/posts/Go/go_http/)

**示例代码**

监听本地端口，在浏览器输出Hello World字符串。

```go
func sayHello(w http.ResponseWriter,r *http.Request){
    //ResponseWriter为服务端返回的内容
	fmt.Fprintln(w, "Hello World!")
}
func main(){
	http.HandleFunc("/",sayHello)
	http.ListenAndServe(":8080",nil)
}
```

### Gin框架

#### 简介

Gin 是一个用 Go (Golang) 编写的 HTTP web 框架。 它是一个类似于 [martini](https://github.com/go-martini/martini) 但拥有更好性能的 API 框架, 优于 [httprouter](https://github.com/julienschmidt/httprouter)，速度提高了近 40 倍。如果你需要极好的性能，使用 Gin 吧。

[官方中文文档](https://gin-gonic.com/zh-cn/docs/)

[Gin框架介绍及使用 | 李文周的博客 (liwenzhou.com)](https://www.liwenzhou.com/posts/Go/Gin_framework/)

**特性**

##### Gin v1 稳定的特性:

- 零分配路由。
- 仍然是最快的 http 路由器和框架。
- 完整的单元测试支持。
- 实战考验。
- API 冻结，新版本的发布不会破坏你的代码。

#### 框架初识

**使用Gin框架返回一个json文件**

```go
func sayHello(c *gin.Context/*gin框架中的临时变量，便于后续响应请求*/){
	c.JSON(http.StatusOK,gin.H{//返回一个json数据
		"message":"HelloWorld",
	})
}
func main(){
	r:=gin.Default()//获取gin框架默认路由对象
	r.GET("/",sayHello)//处理向"/"目录发起的get请求，并将其使用sayHello函数处理
	r.Run()
}
```

项目实践中一般使用匿名函数：

```go
r.GET("/",func(c *gin.Context){
    c.JSON(http.StatusOK,gin.H{
        "message":"HelloWorld",
    })
})
```

**使用Gin框架返回一个html文件**

```go
func main(){
	r:=gin.Default()
	r.LoadHTMLFiles("hello.html")//解析模板
	r.GET("/",func(c *gin.Context){
		c.HTML(http.StatusOK,"hello.html",gin.H{})
	})
	r.Run()
}
```

#### 模板渲染

[template package - html/template - pkg.go.dev](https://pkg.go.dev/html/template)

[Go语言标准库之http/template | 李文周的博客 (liwenzhou.com)](https://www.liwenzhou.com/posts/Go/go_template/)

**一个简单示例**

```go
type User struct {
    //成员变量名必须为大写，使其可以被外部访问
	Name string 
	Gender string
	Age int
}
func sayHello(w http.ResponseWriter, r *http.Request){
	// 定义模板
	// 解析模板
	t, _ := template.ParseFiles("./hello.tmpl")
	// 渲染模板
	u1 := User{  // u1.Name
		Name:   "zeroy",
		Gender: "男",
		Age:    18,
	}
	m1 := map[string]interface{}{
		"name": "zeroy",
		"gender": "男",
		"age": 18,
	}
	hobbyList := []string{
		"乒乓球",
		"网球",
		"羽毛球",
	}
	t.Execute(w, map[string]interface{}{
		"u1": u1,
		"m1": m1,
		"hobby": hobbyList,
	})
}

func main() {
	http.HandleFunc("/", sayHello)
	http.ListenAndServe(":9000", nil)
}
```

**在Gin框架中渲染模板**

```go
func main(){
	r:=gin.Default()
	r.LoadHTMLFiles("hello.tmpl")//加载模板
	r.GET("/",func(c *gin.Context){
		c.HTML(http.StatusOK,"hello.tmpl",gin.H{//向模板中传递参数
			"name": "zeroy",
			"age": 18,
		})
	})
	r.Run()
}
```

模板文件：

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <h1>name: {{.name}}</h1>
    <h1>age: {{.age}}</h1>
</body>
</html>
```

由于实际开发中大多采用前后端分离式开发，模板技术的应用范围不大，所以这里不再赘述，有需要直接查文档就好。

#### Gin框架返回json

```go
package main
import (
	"github.com/gin-gonic/gin"
	"net/http"
)
func main() {
	r := gin.Default()
	r.GET("/json", func(c *gin.Context) {
		data := gin.H{"name":"zeroy", "message": "hello world!", "age": 18}
		c.JSON(http.StatusOK, data)
	})
	type msg struct{
		Name string `json:"name"`//有时为了方便前端开发，需要为类型名创建别名（反射）
		Message string
		Age int
	}
	r.GET("/another_json", func(c *gin.Context) {
		data := msg{
			"zeroy",
			"Hello golang!",
			18,
		}
		c.JSON(http.StatusOK, data)//本质是msg的序列化
	})
	r.Run()
}
```

#### 获取querystring参数

querystring参数即URL中?后的参数。

```go
username := c.DefaultQuery("username", "zeroy")//若查询不到username则默认值为zeroy
address := c.Query("address")
```

**例程：A+B Problem web版**

```go
package main
import (
	"github.com/gin-gonic/gin"
	"strconv"
)
func main() {
	r:=gin.Default()
	r.GET("/",func (c *gin.Context)  {
		a,_:=strconv.Atoi(c.Query("a"))
		b,_:=strconv.Atoi(c.Query("b"))
		c.JSON(200,gin.H{"sum":a+b,})
	})
	r.Run()
}
```

#### 获取form参数

```go
username := c.PostForm("username")
address := c.PostForm("address")
```

PostForm方法可以获取Post请求提交的参数。

#### 获取path参数

**例程：A+B Problem web版（使用path参数传参）**

```go
func main() {
	r:=gin.Default()
	r.GET("/:a/:b",func (c *gin.Context)  {
		a,_:=strconv.Atoi(c.Param("a"))
		b,_:=strconv.Atoi(c.Param("b"))
		c.JSON(200,gin.H{"sum":a+b,})
	})
	r.Run()
}
```

#### 参数绑定

ShouldBind方法可以自动化绑定参数到某个struct中。

```go
type People struct{
	Name string `form:"name"`//设定别名，方便传参
	Age int	`form:"age"`
	BirthDay string `form:"birthday"`
}
func main() {
	r:=gin.Default()
	r.GET("/", func(c *gin.Context) {
		var zeroy People
        //传递的name，age，birthday等变量可以自动化绑定到zeroy中
		if err := c.ShouldBind(&zeroy); err == nil {
			c.JSON(http.StatusOK, gin.H{
				"name":zeroy.Name,
				"age":zeroy.Age,
			})
		} else {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		}
	})
	r.Run()
}
```

**例程：A+B problem with 参数绑定**

```go
type Node struct{
	X int `form:"x"` 
	Y int `form:"y"`
}
func (node Node) sum() int{
	return node.X+node.Y
}
func main() {
	r:=gin.Default()
	r.GET("/", func(c *gin.Context) {
		var tmp Node
		if err := c.ShouldBind(&tmp); err == nil {
			c.JSON(http.StatusOK, gin.H{
				"sum":tmp.sum(),
			})
		} else {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		}
	})
	r.Run()
}
```

#### 文件上传

```go
c.FormFile("")
dst := fmt.Sprintf("./%s", file.Filename)
// 上传文件到指定的目录
c.SaveUploadedFile(file, dst)
```

```go
form, _ := c.MultipartForm()//多个文件上传
files := form.File["file"]
```

### 总结

掌握了Gin框架的基本操作，我们便有能力搭建一个最最基本的web服务，处理来自用户端的请求。

但是如果要搭建一个真正实用的服务器后端，还需要与本地的数据库进行交互（`database/sql`，`GORM`），进行复杂的鉴权操作。

之后可能会看看数据库交互和一些中间件，实现鉴权和与本地数据库交互。
