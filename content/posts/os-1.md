---
title: "操作系统：设计与实现（南京大学蒋炎岩） 并发部分 笔记"
date: 2022-07-10T18:20:17+08:00
draft: true
url: "articles/os1"
categories: ["操作系统"]
---

### 1. 操作系统概述

> Operating System: A body of software, in fact, that is responsible for *making it easy to run programs* (even allowing you to seemingly run many at the same time), allowing programs to share memory, enabling programs to interact with devices, and other fun stuff like that. (OSTEP)

“管理软/硬件资源、为程序提供服务” 的程序。

![](/os1/os-classify.jpg)



### 2. 操作系统上的程序

#### 什么是程序？

程序就是状态机。

C程序的状态机模型（语义，semantic）

+ 状态 = 堆 + 栈
+ 初始状态 = main的第一条语句
+ 迁移=执行一条简单语句
+ + 任何C程序都可以改写成“非复合语句”的C代码



C程序的状态机模型（语义，semantic）

+ 状态 = stack frame 的列表 (每个 frame 有 PC) + 全局变量
+ 初始状态 = main(argc, argv), 全局变量初始化
+ 迁移 = 执行 top stack frame PC 的语句; PC++
+ + 函数调用 = push frame (frame.PC = 入口)
  + 函数返回 = pop frame



任何递归程序都可以转化为非递归：

```c
//非递归版汉诺塔
typedef struct {
  int pc, n;
  char from, to, via;
} Frame;

#define call(...) ({ *(++top) = (Frame) { .pc = 0, __VA_ARGS__ }; })
#define ret()     ({ top--; })
#define goto(loc) ({ f->pc = (loc) - 1; })

void hanoi(int n, char from, char to, char via) {
  Frame stk[64], *top = stk - 1;
  call(n, from, to, via);
  for (Frame *f; (f = top) >= stk; f->pc++) {
    switch (f->pc) {
      case 0: if (f->n == 1) { printf("%c -> %c\n", f->from, f->to); goto(4); } break;
      case 1: call(f->n - 1, f->from, f->via, f->to);   break;
      case 2: call(       1, f->from, f->to,  f->via);  break;
      case 3: call(f->n - 1, f->via,  f->to,  f->from); break;
      case 4: ret();                                    break;
      default: assert(0);
    }
  }
}
```

