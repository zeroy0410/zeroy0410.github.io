---
title: "实现一个自己的shell（操作系统Lab2）"
date: 2023-03-31T21:00:58+08:00
draft: false
categories: ["操作系统","计算机体系结构"]
url: "posts/oslab2"
---

## 实验题目

Project 1—UNIX Shell and History Feature

This project consists of designing a C program to serve as a shell interface

that accepts user commands and then executes each command in a separate

process. This project can be completed on any Linux, UNIX, or Mac OS X system.

A shell interface gives the user a prompt, after which the next command

is entered. The example below illustrates the prompt osh> and the user’s

next command: cat prog.c. (This command displays the file prog.c on the

terminal using the UNIX cat command.)

osh> cat prog.c

One technique for implementing a shell interface is to have the parent process

first read what the user enters on the command line (in this case, cat

prog.c), and then create a separate child process that performs the command.

Unless otherwise specified, the parent process waits for the child to exit

before continuing. This is similar in functionality to the new process creation

illustrated in Figure 3.10. However, UNIX shells typically also allow the child

process to run in the background, or concurrently. To accomplish this, we add

an ampersand (&) at the end of the command. Thus, if we rewrite the above

command as

osh> cat prog.c &

the parent and child processes will run concurrently.

The separate child process is created using the fork() system call, and the

user’s command is executed using one of the system calls in the exec() family

(as described in Section 3.3.1).

A C program that provides the general operations of a command-line shell

is supplied in Figure 3.36. The main() function presents the prompt osh->

and outlines the steps to be taken after input from the user has been read. The

main() function continually loops as long as should run equals 1; when the

user enters exit at the prompt, your program will set should run to 0 and

terminate.

This project is organized into two parts: (1) creating the child process and

executing the command in the child, and (2) modifying the shell to allow a

history feature.

## 相关原理与知识（完成实验所用到的相关原理与知识）

Linux 进程相关基础知识。

Linux下C语言编程。

如何使用终端颜色控制字符调整终端输出字符的颜色。

命令行解析。

## 实验过程（清晰展示实际操作过程，相关截图及解释）

### 模型归纳

一个典型的shell可以简化为以下形式：

```c
while(1)
{
  	init();
    read_command();
    int pid = fork();

    if(pid < 0)
    {
        puts("Unable to fork the child, inner error.");
    }
    else if(pid == 0) // the child thread
    {
        execve(command); //execve the command
    }
    else // the parent thread
    {
        wait(NULL); //waiting for the child to exit
    }
}
```

当在shell中进行输入时，fork()出子进程来执行我们的输入，父进程则等待我们的子进程执行完成。

#### 美化实现

通过查阅终端颜色控制符实现几个函数，用于打印彩色字符。

```c
void PrintBlue(char *ch) { printf("\033[1;34m%s\033[0m", ch); }

void PrintRed(char *ch) { printf("\033[1;31m%s\033[0m", ch); }

void PrintPink(char *ch) { printf("\033[1;35m%s\033[0m", ch); }
```

通过`getcwd`函数，加上一个小的`parser`实现获取当前文件夹名称。

```c
void PrintCurrentDir() {
    char tmp[114];
    int tcnt = 0;
    char *cwd = getcwd(NULL, 0);
    int cur = strlen(cwd) - 1;
    while (cwd[cur] != '/') {
        tmp[tcnt++] = cwd[cur];
        cur--;
    }
    for (int i = 0; i < tcnt/2;i++) {
        char c = tmp[i];
        tmp[i] = tmp[tcnt - i - 1];
        tmp[tcnt - i - 1] = c;
    }
    tmp[tcnt] = 0;
    PrintPink(tmp);
}
```

最终效果如下：

![1](https://zeroyblog-1307855373.cos.ap-nanjing.myqcloud.com/images%2Foslab21.png)

### 核心功能实现

#### 解析输入命令

```c
fgets(buffer, MAX_ARGS_LEN * MAX_ARGS, stdin);
FILE *fp = fmemopen(buffer, strlen(buffer), "r");
for (int i = 0; i < args_count; i++)
  free(args[i]);
args_count = 0;
while (1) {
  args[args_count] = (char *)malloc(MAX_ARGS_LEN);
  int fl = fscanf(fp, "%s", args[args_count]);
  if (fl < 0)
    break;
  args_count++;
}
if (args_count == 0)
  continue;
free(args[args_count]);
args[args_count] = NULL;
```

这段代码实现了：安全地读取一行的内容，并将这一行的内容映射成文件，通过`fscanf`实现模式匹配地读入命令，并将读取的字符串存储在`args`这个字符串数组中。

#### 实现cd命令与exit命令

```c
if (strcmp(args[0], "cd") == 0) {
  if (chdir(args[1]) == -1) {
    PrintRed("z-shell: error!\n");
    fflush(stdout);
    continue;
  } else {
    PrintBlue("z-shell: you are now in ");
    printf("%s\n", args[1]);
    fflush(stdout);
  }
  continue;
}

if (strcmp(args[0], "exit") == 0) {
  printf("Bye bye! Thanks to use z-shell!\n");
  fflush(stdout);
  break;
}
```

`chdir`函数能够实现切换工作目录的功能，若出现错误，则返回`-1`。`exit`较简单，不再赘述。

#### 实现命令执行

```c
if (strcmp(args[args_count - 1], "&") == 0) {
  flag = FLAG_EXECVE_NOTWAIT;
}
pid_t pid = fork();
if (pid == -1) {
  PrintRed("z-shell: an error occurred while forking\n");
  fflush(stdout);
} else if (pid == 0) {
  int fl = execvp(args[0], args);
  if (fl == -1) {
    PrintRed("z-shell: unable to execute the programme ");
    printf("%s.\n", args[0]);
    fflush(stdout);
  }
  exit(0);
} else if (flag == FLAG_EXECVE_WAIT)
  wait(NULL);
```

`fork()`函数相当于复制当前状态机，子进程的`pid=0`用于命令执行，父进程则等待子进程执行完毕。若添加了`&`参数，则父进程无需等待子进程结束。

#### 实现历史记录功能

```c
typedef struct history {
    char *buf[MAX_HISTORY];
    int his_count;
} history;

if (strcmp(args[0], "!!") == 0) {
  if (his.his_count == 0) {
    PrintRed("z-shell: no commands in history!\n");
    continue;
  }
  strcpy(buffer, his.buf[his.his_count]);
  goto PARSER;
}
if (strcmp(args[0], "!") == 0) {
  if (args_count == 1) {
    PrintRed("z-shell: please input number!\n");
    continue;
  }
  int num = atoi(args[1]);
  if (num == -1) {
    PrintRed("z-shell: number illegal!\n");
    continue;
  }
  int cur = his.his_count - num + 1;
  if (cur <= 0) {
    PrintRed("z-shell: no commands in history!\n");
    continue;
  }
  strcpy(buffer, his.buf[cur]);
  goto PARSER;
}
```

使用`history`这一数据结构存储历史记录，解析`!`和`!!`命令访问历史记录，从容器中取出匹配的命令赋值给`buffer`，当正常的命令结束后，将`buffer`存储到`history`。

#### 测试程序

测试截图如下：

![2](https://zeroyblog-1307855373.cos.ap-nanjing.myqcloud.com/images%2Foslab22.png)

## 问题分析与总结

实验中遇到的问题较少，学到了如何控制终端输出彩色字符。

要注意使用前先`malloc`分配内存，在不用时及时`free`，避免段错误或内存泄露。

### 完整代码

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

#define MAX_ARGS 114     // 支持的输入变量个数
#define MAX_ARGS_LEN 114 // 单个变量的长度

#define FLAG_EXECVE_WAIT 0
#define FLAG_EXECVE_NOTWAIT 1

#define MAX_HISTORY 114

typedef struct history {
    char *buf[MAX_HISTORY];
    int his_count;
} history;

void PrintBlue(char *ch) { printf("\033[1;34m%s\033[0m", ch); }

void PrintRed(char *ch) { printf("\033[1;31m%s\033[0m", ch); }

void PrintPink(char *ch) { printf("\033[1;35m%s\033[0m", ch); }

void PrintCurrentDir() {
    char tmp[114];
    int tcnt = 0;
    char *cwd = getcwd(NULL, 0);
    int cur = strlen(cwd) - 1;
    while (cwd[cur] != '/') {
        tmp[tcnt++] = cwd[cur];
        cur--;
    }
    for (int i = 0; i < tcnt/2;i++) {
        char c = tmp[i];
        tmp[i] = tmp[tcnt - i - 1];
        tmp[tcnt - i - 1] = c;
    }
    tmp[tcnt] = 0;
    PrintPink(tmp);
}

int main() {
    char *args[MAX_ARGS];
    char *buffer = (char *)malloc(MAX_ARGS_LEN * MAX_ARGS);
    int args_count = 0;
    int flag = 0;
    history his;
    his.his_count = 0;
    printf("\033[1;33mWelcome to z-shell!\033[0m\n");
    PrintPink("              _          _ _ \n");
    PrintPink(" ____     ___| |__   ___| | |\n");
    PrintPink("|_  /____/ __| '_ \\ / _ \\ | |\n");
    PrintPink(" / /_____\\__ \\ | | |  __/ | |\n");
    PrintPink("/___|    |___/_| |_|\\___|_|_|\n");
    printf("\n\n");
    while (1) {
        PrintBlue("[z-shell]$ -> ");
        PrintCurrentDir();
        putchar(' ');
        fflush(stdout);
        fgets(buffer, MAX_ARGS_LEN * MAX_ARGS, stdin);
    PARSER:;
        FILE *fp = fmemopen(buffer, strlen(buffer), "r");
        for (int i = 0; i < args_count; i++)
            free(args[i]);
        args_count = 0;
        while (1) {
            args[args_count] = (char *)malloc(MAX_ARGS_LEN);
            int fl = fscanf(fp, "%s", args[args_count]);
            if (fl < 0)
                break;
            args_count++;
        }
        if (args_count == 0)
            continue;
        free(args[args_count]);
        args[args_count] = NULL;
        if (strcmp(args[0], "!!") == 0) {
            if (his.his_count == 0) {
                PrintRed("z-shell: no commands in history!\n");
                continue;
            }
            strcpy(buffer, his.buf[his.his_count]);
            goto PARSER;
        }
        if (strcmp(args[0], "!") == 0) {
            if (args_count == 1) {
                PrintRed("z-shell: please input number!\n");
                continue;
            }
            int num = atoi(args[1]);
            if (num == -1) {
                PrintRed("z-shell: number illegal!\n");
                continue;
            }
            int cur = his.his_count - num + 1;
            if (cur <= 0) {
                PrintRed("z-shell: no commands in history!\n");
                continue;
            }
            strcpy(buffer, his.buf[cur]);
            goto PARSER;
        }
        if (strcmp(args[0], "exit") == 0) { // 退出
            printf("Bye bye! Thanks to use z-shell!\n");
            fflush(stdout);
            break;
        }
        if (strcmp(args[0], "cd") == 0) {
            if (chdir(args[1]) == -1) {
                PrintRed("z-shell: error!\n");
                fflush(stdout);
                continue;
            } else {
                PrintBlue("z-shell: you are now in ");
                printf("%s\n", args[1]);
                fflush(stdout);
            }
            continue;
        }
        if (strcmp(args[args_count - 1], "&") == 0) {
            flag = FLAG_EXECVE_NOTWAIT;
        }
        pid_t pid = fork();
        if (pid == -1) {
            PrintRed("z-shell: an error occurred while forking\n");
            fflush(stdout);
        } else if (pid == 0) {
            int fl = execvp(args[0], args);
            if (fl == -1) {
                PrintRed("z-shell: unable to execute the programme ");
                printf("%s.\n", args[0]);
                fflush(stdout);
            }
            exit(0);
        } else if (flag == FLAG_EXECVE_WAIT)
            wait(NULL);
        his.his_count++;
        his.buf[his.his_count] = (char *)malloc(MAX_ARGS * MAX_ARGS_LEN);
        strcpy(his.buf[his.his_count], buffer);
    }
    return 0;
}
```

