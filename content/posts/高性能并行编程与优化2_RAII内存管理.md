---
title: "《高性能并行编程与优化2 RAII内存管理》笔记"
date: 2023-04-02T20:16:15+08:00
draft: true
url: "posts/parallels101_2"
categories: ["计算机体系结构","高性能并行编程与优化"]
---

#### **课程作者：@彭于斌**

课程网站：[高性能并行编程与优化](https://github.com/parallel101/course)



#### 从一个案例来看C++的历史

##### 求一个列表中所有数的和

C语言：

```c
#include <stdlib.h>
#include <stdio.h>

int main() {
    size_t nv = 4;
    int *v = (int *)malloc(nv * sizeof(int));
    v[0] = 4;
    v[1] = 3;
    v[2] = 2;
    v[3] = 1;

    int sum = 0;
    for (size_t i = 0; i < nv; i++) {
        sum += v[i];
    }

    printf("%d\n", sum);

    free(v);
    return 0;
}
```

近代：C++98引入STL容器库：

```cpp
#include <vector>
#include <iostream>

int main() {
    std::vector<int> v(4);
    v[0] = 4;
    v[1] = 3;
    v[2] = 2;
    v[3] = 1;

    int sum = 0;
    for (size_t i = 0; i < v.size(); i++) {
        sum += v[i];
    }

    std::cout << sum << std::endl;
    return 0;
}
```

近现代：C++11 引入了 {} 初始化表达式：

```cpp
#include <vector>
#include <iostream>

int main() {
    std::vector<int> v = {4, 3, 2, 1};

    int sum = 0;
    for (size_t i = 0; i < v.size(); i++) {
        sum += v[i];
    }

    std::cout << sum << std::endl;
    return 0;
}
```

近现代：C++11 引入了 range-based for-loop：


```cpp
#include <vector>
#include <iostream>

int main() {
    std::vector<int> v = {4, 3, 2, 1};

    int sum = 0;
    for (int vi: v) {
        sum += vi;
    }

    std::cout << sum << std::endl;
    return 0;
}
```

如果想使用 for_each 这个算法模板呢？

```cpp
#include <vector>
#include <iostream>
#include <algorithm>

int sum = 0;

void func(int vi) {
    sum += vi;
}

int main() {
    std::vector<int> v = {4, 3, 2, 1};

    std::for_each(v.begin(), v.end(), func);

    std::cout << sum << std::endl;
    return 0;
}
```

近现代：C++11 引入了 lambda 表达式：


```cpp
#include <vector>
#include <iostream>
#include <algorithm>

int main() {
    std::vector<int> v = {4, 3, 2, 1};

    int sum = 0;
    std::for_each(v.begin(), v.end(), [&] (auto vi) {
        sum += vi;
    });

    std::cout << sum << std::endl;
    return 0;
}
```

现代：C++14 的 lambda 允许用 auto 自动推断类型：

```cpp
#include <vector>
#include <iostream>
#include <algorithm>

int main() {
    std::vector v = {4, 3, 2, 1};

    int sum = 0;
    std::for_each(v.begin(), v.end(), [&] (auto vi) {
        sum += vi;
    });

    std::cout << sum << std::endl;
    return 0;
}
```

当代：C++17 CTAD / compile-time argument deduction / 编译期参数推断：

```cpp
#include <vector>
#include <iostream>
#include <algorithm>

int main() {
    std::vector v = {4, 3, 2, 1};

    int sum = 0;
    std::for_each(v.begin(), v.end(), [&] (auto vi) {
        sum += vi;
    });

    std::cout << sum << std::endl;
    return 0;
}

```

未来：C++20 引入区间（ranges）

```cpp
#include <vector>
#include <iostream>
#include <numeric>
#include <ranges>
#include <cmath>

int main() {
    std::vector v = {4, 3, 2, 1, 0, -1, -2};

    for (auto &&vi: v
         | std::views::filter([] (auto &&x) { return x >= 0; })
         | std::views::transform([] (auto &&x) { return sqrtf(x); })
         ) {
        std::cout << vi << std::endl;
    }

    return 0;
}
```

未来：C++20 引入模块（module）

```cpp
import <vector>;
import <iostream>;
import <numeric>;
import <ranges>;
import <cmath>;

int main() {
    std::vector v = {4, 3, 2, 1, 0, -1, -2};

    for (auto &&vi: v
         | std::views::filter([] (auto &&x) { return x >= 0; })
         | std::views::transform([] (auto &&x) { return sqrtf(x); })
         ) {
        std::cout << vi << std::endl;
    }

    return 0;
}
```

未来：C++20 引入协程（coroutine）和生成器（generator）

```cpp
import <vector>;
import <iostream>;
import <numeric>;
import <ranges>;
import <cmath>;
import <generator>;

std::generator<int> myfunc(auto &&v) {
    for (auto &&vi: v
         | std::views::filter([] (auto &&x) { return x >= 0; })
         | std::views::transform([] (auto &&x) { return sqrtf(x); })
         ) {
        co_yield vi;
    }
}

int main() {
    std::vector v = {4, 3, 2, 1, 0, -1, -2};
    for (auto &&vi: myfunc(v)) {
        std::cout << vi << std::endl;
    }
    return 0;
}
```

未来：C++20 标准库加入 format 支持

```cpp
import <vector>;
import <iostream>;
import <numeric>;
import <ranges>;
import <cmath>;
import <generator>;
import <format>;

std::generator<int> myfunc(auto &&v) {
    for (auto &&vi: v
         | std::views::filter([] (auto &&x) { return x >= 0; })
         | std::views::transform([] (auto &&x) { return sqrtf(x); })
         ) {
        co_yield vi;
    }
}

int main() {
    std::vector v = {4, 3, 2, 1, 0, -1, -2};
    for (auto &&vi: myfunc(v)) {
        std::format_to(std::cout, "number is {}\n", vi);
    }
    return 0;
}
```



#### C++面向对象思想

##### 封装

将多个逻辑上相关的变量包装成一个类，比如要表达一个数组，需要：起始地址指针v，数组大小nv，因此 C++ 的 vector 将他俩打包起来，避免程序员犯错。

```cpp
size_t nv = 2;
int *v = (int *)malloc(nv * sizeof(int));

->

std::vector<int> v(2);
```

**不变性：**

比如当我要设置数组大小为 4 时，不能只 nv = 4。

还要重新分配数组内存，从而修改数组起始地址 v。

常遇到：当需要修改一个成员时，其他也成员需要被修改，否则出错。

这种情况出现时，就意味着你需要把成员变量的读写封装为**成员函数**。

#### 切勿滥用封装！

仅当出现“修改一个成员时，其他也成员要被修改，否则出错”的现象时，才需要getter/setter 封装。

各个成员之间相互正交，就没必要去搞封装，只会让程序员变得痛苦，同时还有一定性能损失：特别是如果 getter/setter 函数分离了声明和定义，实现在另一个文件时！



#### C++思想：RAII（Resource Acquisition Is Initialization）

**关键：构造函数与析构函数**

如果没有解构函数，则每个带有返回的分支都要手动释放所有之前的资源:

```cpp
#include <fstream>
#include <vector>
#include <cstdio>

int main() {
    std::ifstream f1("1.txt");
    if (checkFileContent(f1)) {
        printf("bad file 1!\n");
        f1.close();
        return 1;
    }

    std::ifstream f2("2.txt");
    if (checkFileContent(f2)) {
        printf("bad file 2!\n");
        f1.close();
        f2.close();
        return 1;
    }

    std::vector<std::ifstream> files;
    files.push_back(std::ifstream("3.txt"));
    files.push_back(std::ifstream("4.txt"));
    files.push_back(std::ifstream("5.txt"));

    for (auto &file: files)
        file.close();

    f1.close();
    f2.close();
    return 0;
}
```



C++ 面向对象部分可以参考**《C++ 程序设计》简明讲义 潘建瑜**



### 智能指针

#### C++98 令人头疼的内存管理

在没有智能指针的 C++ 中，我们只能手动去 new 和 delete 指针。

这非常容易出错，一旦马虎的程序员忘记释放指针，就会导致内存泄露等情况，

更可能被黑客利用空悬指针篡改系统内存从而盗取重要数据等。



#### RAII 解决内存管理的问题：unique_ptr

C++11 引入了 unique_ptr 容器，他的解构函数中会调用 delete p，因此不会有马虎犯错的问题。

这里 `make_unique<C>(...) `可以理解为和之前的 `new C(...)`等价，括号里也可以有其他构造函数的参数。

```cpp
#include <cstdio>
#include <memory>

struct C {
    C() {
        printf("分配内存!\n");
    }

    ~C() {
        printf("释放内存!\n");
    }
};

int main() {
    std::unique_ptr<C> p = std::make_unique<C>();

    if (1 + 1 == 2) {
        printf("出了点小状况……\n");
        return 1;  // 自动释放 p
    }

    return 0;  // 自动释放 p
}
```



#### unique_ptr：封装的智慧

在旧时代 C++ 里，常常听到这样的说法：

“释放一个指针后，必须把这个指针设为 NULL，防止空悬指针！”

```cpp
delete p;
p = nullptr;
```

unique_ptr 则把他们封装成一个操作：只需要 p = nullptr;   即可。也不会保留着一个空悬指针，体现了面向对象“封装：不变性”的思想。



#### unique_ptr：禁止拷贝

unique_ptr 删除了拷贝构造函数，如果拷贝了指针，就有可能出现**重复释放（double free）**的问题

**解决方案1：获取原始指针**

```cpp
#include <cstdio>
#include <memory>

struct C {
    C() {
        printf("分配内存!\n");
    }

    ~C() {
        printf("释放内存!\n");
    }

    void do_something() {
        printf("成员函数!\n");
    }
};

void func(C *p) {
    p->do_something();
}

int main() {
    std::unique_ptr<C> p = std::make_unique<C>();
    func(p.get());
    return 0;
}
```

**解决方案2：unique_ptr不能拷贝，但可以移动**

这个和rust里的转移所有权有点像。

```cpp
#include <cstdio>
#include <memory>
#include <vector>

struct C {
    C() {
        printf("分配内存!\n");
    }

    ~C() {
        printf("释放内存!\n");
    }
};

std::vector<std::unique_ptr<C>> objlist;

void func(std::unique_ptr<C> p) {
    objlist.push_back(std::move(p));  // 进一步移动到 objlist
}

int main() {
    std::unique_ptr<C> p = std::make_unique<C>();
    printf("移交前：%p\n", p.get());  // 不为 null
    func(std::move(p));    // 通过移动构造函数，转移指针控制权
    printf("移交后：%p\n", p.get());  // null，因为移动会清除原对象
    return 0;
}
```

