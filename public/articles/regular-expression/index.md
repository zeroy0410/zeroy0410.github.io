# 正则表达式 For Beginner


#### 简介

**正则表达式**（英语：Regular Expression，常简写为regex、regexp或RE），又称**正则表示式**、**正则表示法**、**规则表达式**、**常规表示法**，是[计算机科学](https://zh.wikipedia.org/wiki/计算机科学)的一个概念。正则表达式使用单个字符串来描述、匹配一系列匹配某个句法规则的[字符串](https://zh.wikipedia.org/wiki/字符串)。在很多[文本编辑器](https://zh.wikipedia.org/wiki/文本编辑器)里，正则表达式通常被用来检索、替换那些匹配某个模式的文本。

许多[程序设计语言](https://zh.wikipedia.org/wiki/程序设计语言)都支持利用正则表达式进行字符串操作。例如，在[Perl](https://zh.wikipedia.org/wiki/Perl)中就内建了一个功能强大的正则表达式引擎。正则表达式这个概念最初是由[Unix](https://zh.wikipedia.org/wiki/Unix)中的工具软件（例如[sed](https://zh.wikipedia.org/wiki/Sed)和[grep](https://zh.wikipedia.org/wiki/Grep)）普及开的。

#### 语法总结

**需要转义的特殊字符：**

```
.[{()\^$|?*+
```

就像在其它任何语言中那样，转义需要在符号前加上`\`。

**匹配规则：**

```
.       - 除了新行外的任何字符
\d      - 数字 (0-9)
\D      - 非数字 (0-9)
\w      - 单词字母 (a-z, A-Z, 0-9, _)
\W      - 非单词字母
\s      - 空字符 (space, tab, newline)
\S      - 非空字符 (space, tab, newline)

\b      - 单词边界
\B      - 非单词边界
^       - 字符串开头（默认将一行看作一整个字符串）
$       - 字符串结尾（默认将一行看作一整个字符串）

[]      - 匹配字符集
[^ ]    - 匹配除了字符集外的字符
|       - 或者
( )     - Group

Quantifiers:
*       - 0 or More
+       - 1 or More
?       - 0 or One
{3}     - Exact Number
{3,4}   - Range of Numbers (Minimum, Maximum)


[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[0-9a-zA-Z.-]+
```



**一些例子：**

匹配人名：

```
Mr. Schafer
Mr Smith
Ms Davis
Mrs. Robinson
Mr. T

M(r|s|rs)\.?\s[A-Z]\w*
```

匹配两种格式的电话号码：

```321-555-4321
123.555.1234
800-555-4321
900-555-4321

\d{3}[.-]\d{3}[.-]\d{4}
```

匹配三种格式的电子邮件：

```
CoreyMSchafer@gmail.com
corey.schafer@university.edu
corey-321-schafer@my-work.net

[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[0-9a-zA-Z.-]+
```



#### 按Group引用

提取文件中的url，并截取出其中的顶级域名：

```
https://www.google.com
http://coreyms.com
https://youtube.com
https://www.nasa.gov

匹配https?://(www\.)?(\w+)(\.\w+)
引用：$2$3
结果：
google.com
coreyms.com
youtube.com
nasa.gov
```


