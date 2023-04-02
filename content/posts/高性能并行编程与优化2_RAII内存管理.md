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
#include <numeric>

int main() {
    std::vector v = {4, 3, 2, 1};

    int sum = std::reduce(v.begin(), v.end(), 0, [] (int x, int y) {
        return x + y;
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

