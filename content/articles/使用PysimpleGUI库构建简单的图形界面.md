---
title: "使用PySimpleGUI库构建简单的图形界面"
date: 2022-01-26T16:49:18+08:00
draft: false
url: articles/PySimpleGUI
categories: ['python']
---

#### 前言

python构建本地GUI程序有很多方式，比如**Tkinter**，**wxPython**，或是**PyQT**。但是对于学生而言，并不需要多么华丽的用户界面，只需要“能用”就行了，开发环节越省力越好。

于是我找到了PySimpleGUI这个库。

[A introduction to PySimpleGUI](https://www.youtube.com/watch?v=-_z2RPAH0Qk)

这个库提供了一种近乎傻瓜化的方式，采用List来描述一个GUI界面，同时支持一个简单程序需要的全部特性，并且支持Win/Mac/Linux三大平台，十分适合拿来封装代码。

#### 安装

```
pip install PySimpleGUI
```

在文件开头加上库引用：

```python
import PySimpleGUI as sg
```

#### 元素

PySimpleGUI有着丰富的控件支持。

1. **文本框（Text）**

```python
sg.Text('文本框',size=(12,1),key='output')
```

`'文本框'`为框体显示的文字，size为框体的大小，key为框体标识，用于之后对文本框的定位。

2. **输入框（Input）**

```python
sg.Input(key='input')
```

3. **按钮（Button）**

```python
sg.Button('Go')
```

`'Go'`为按钮的名字。也可以另外设置key值。

4. **下拉框（Comobo）**

```python
[ sg.Text("City", size = (20, 1)), sg.Combo(("北京", "上海", "深圳"), size=(10, 1), default_value="上海", key = "-CITY-")]
```

5. **弹窗（Popup）**

```python
sg.Popup('弹窗1','This is the first one')
sg.Popup('弹窗2','This is the second one')
sg.Popup('弹窗3','This is the third one')
```

弹出一个窗口包含标题和内容。

6. **选择文件（FileBrowse）**

```python
sg.FileBrowse()
```

7. **选择文件路径（FolderBrowse）**

```python
sg.InputText(size=(15,1)),sg.FolderBrowse()
```

8. **多行列表文本（ListBox）**

```python
list = [1，2，3]
layout = [
    [sg.Listbox(values=list,size=(20,12),key='LIST',enable_events=True)]
]
```

9. **多选框（Checkbox）**

```python
sg.Checkbox('多选框',default=True)
```

10. **单选框（Radio）**

```python
# RADIO1 必有
sg.Radio('单选框','RADIO1',default=True)
```

11. **大文本框（Multiline）**

```python
sg.Multiline(default_text='hello')
```

12. **下拉列表框（InputCombo）**

```python
sg.InputCombo(['box_1','box_2'],size=(20,3))
```

13. **拖动按钮（Slider）**

```python
sg.Slider(range=(1,100),orientation='h',size=(34,20),default_value=85)
 # (range=(1, 100)：数值范围
 # orientation=拖动方向 ‘h’ :横向 ‘v’：竖向
 # size=(34, 20)：大小
 # default_value=85默认值
```

14. **下拉选项（InputOptionMenu）**

```python
sg.InputOptionMenu('Menu_1','Menu_2',size=(20,2))
```

15. **菜单（Menu）**

```python
sg.Menu(menu_def, tearoff=True)
```

16. **控件（Column）**

```python
sg.Column(column1, background_color='')
```

17. **进度条（ProgressBar）**

```python
sg.ProgressBar(10,orientation='h',size=())
# 10：进度条长度
# orientation=‘h’/v 方向
```

18. **调试窗口**

```python
sg.Print('内容', text_color='', background_color='', font='')
```

19. **自带按钮**

```python
sg.OK(), sg.Cancel(),sg.Submit()等 #这三个按钮是自带的，默认的，不需要单独定义其作用
当然，也可以单独设置
sg.Button('Ok'), sg.Button('Cancel')
自带按钮
sg.FolderBrowse()=sg.FileBrowse(), sg.Submit(), sg.Cancel()
```

#### 构建窗口

使用PySimpleGUI构建一个窗口十分简单，你需要使用一个list描述元素之间的位置关系，然后系统便会自动生成布局。

以我上一篇博文[Bilibili直播弹幕收发小程序 | zeroy's blog](https://zeroy.site/articles/Bilibili-send-and-receive/)中的GUI界面为例：

```python
sg.theme('DarkAmber')#选择主题
layout = [
          [sg.Listbox('',size=(75,20),key='-OUT-')],
          [sg.Text('发送弹幕: ', size=(8, 1)),sg.InputText('',key='-input-'),sg.Button("Go"),sg.Button("Exit"),sg.Button("Help")],
          [sg.Text('',key='-error-')]
         ]#使用list描述元素之间的相对关系
window=sg.Window("Bilibili弹幕收发程序",layout)生成窗口
```

怎么样，是不是很方便呢？

窗口中内建了多种方法，用于描述窗口事件。

```python
window.close()#关闭窗口
window.read()#读取窗口内容
window['key名'].update('需要更新的内容')
```

掌握了这些基本的知识，构建一个简单的GUI程序应该没什么难的了。

上面提到的收发弹幕的程序的GUI部分完整代码如下：

```python
import PySimpleGUI as sg
import send
import receive
sg.theme('DarkAmber')
layout = [
          [sg.Listbox('',size=(75,20),key='-OUT-')],
          [sg.Text('发送弹幕: ', size=(8, 1)),sg.InputText('',key='-input-'),sg.Button("Go"),sg.Button("Exit"),sg.Button("Help")],
          [sg.Text('',key='-error-')]
         ]
window=sg.Window("Bilibili弹幕收发程序",layout)
while True:#开启窗口事件
    event,values=window.read(timeout=3)#为输入框设定超时
    try:
        window['-OUT-'].update(receive.Receive())#更新输出框
    except:
        sg.popup('error: ','请先配置好同一目录下的config.json文件')#异常信息处理
        break
    if event in (None,'Exit'):#按到了退出
        break
    if event=='Go':#发送弹幕
        window['-error-'].update(send.Send(values['-input-']))
        window['-input-'].update("")
    if event=='Help':#帮助页面
        sg.popup('帮助: ','请先配置好同一目录下的config.json文件')
window.close()
```

更多的例子以及更高阶的应用指路：[官方代码库](https://github.com/PySimpleGUI/PySimpleGUI)



#### 总结

这个东西过于简洁，适合完全不会写GUI的程序员应急。
