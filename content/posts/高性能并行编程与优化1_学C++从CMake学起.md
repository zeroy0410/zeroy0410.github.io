---
title: "《高性能并行编程与优化1 学C++从CMake学起》笔记"
date: 2023-04-01T20:16:15+08:00
draft: false
url: "posts/parallels101_1"
categories: ["计算机体系结构","高性能并行编程与优化"]
---

#### **课程作者：@彭于斌**

课程网站：[高性能并行编程与优化](https://github.com/parallel101/course)



#### CMake的命令行调用

读取当前目录的 CMakeLists.txt，并在 build 文件夹下生成 build/Makefile：
> cmake -B build
> 让 make 读取 build/Makefile，并开始构建 a.out：
> make -C build
> 以下命令和上一个等价，但更跨平台：
> cmake --build build
> 执行生成的 a.out：
> build/a.out



#### CMake中的静态库与动态库

CMake 除了 `add_executable` 可以生成可执行文件外，还可以通过 `add_library` 生成库文件。
`add_library `的语法与 `add_executable` 大致相同，除了他需要指定是动态库还是静态库：
`add_library(test STATIC source1.cpp source2.cpp) ` # 生成静态库 libtest.a
`add_library(test SHARED source1.cpp source2.cpp) ` # 生成动态库 libtest.so
动态库有很多坑，特别是 Windows 环境下，初学者自己创建库时，建议使用静态库。
创建库以后，要在某个可执行文件中使用该库，只需要：
`target_link_libraries(myexec PUBLIC test) ` # 为 myexec 链接刚刚制作的库 libtest.a



#### 为什么C++需要声明？

C++ 是一种强烈依赖**上下文**信息的编程语言。

vector < MyClass > a;  // 声明一个由 MyClass 组成的数组

如果编译器不知道 vector 是个模板类，那他完全可以把 vector 看做一个变量名，把 < 解释为小于号，从而理解成判断‘vector’这个变量的值是否小于‘MyClass’这个变量的值。

正因如此，我们常常可以在 C++ 代码中看见这样的写法：typename decay<T>::type

因为 T 是不确定的，导致编译器无法确定 decay<T> 的 type 是一个**类型**，还是一个**值**。因此用 typename 修饰来让编译器确信这是一个类型名……



#### 为什么需要头文件？

便于声明与实现分开，不用在每个文件里都声明一遍，只需include相应头文件就好了。



#### CMake中的子模块

复杂的工程中，我们需要划分子模块，通常一个库一个目录，比如：
这里我们把 hellolib 库的东西移到 hellolib 文件夹下了，里面的 CMakeLists.txt 定义了 hellolib 的生成规则。
要在根目录使用他，可以用 CMake 的 add_subdirectory 添加子目录，子目录也包含一个 CMakeLists.txt，其中定义的库在 add_subdirectory 之后就可以在外面使用。
子目录的 CMakeLists.txt 里路径名（比如 hello.cpp）都是相对路径，这也是很方便的一点。

```bash
-
  - hellolib
    - CMakeLists.txt
    - hello.cpp
    - hello.h
  - CMakeLists.txt
  - main.cpp
```

`hellolib/CMakeLists.txt`

```cmake
add_library(hellolib STATIC hello.cpp)
```

`CMakeLists.txt`

```cmake
cmake_minimum_required(VERSION 3.12)
project(hellocmake LANGUAGES CXX)

add_subdirectory(hellolib)

add_executable(a.out main.cpp)
target_link_libraries(a.out PUBLIC hellolib)
```



#### 子模块的头文件如何处理

因为 hello.h 被移到了 hellolib 子文件夹里，因此 main.cpp 里也要改成：

```C++
#include "hellolib/hello.h"
```

如果要避免修改代码，我们可以通过 target_include_directories 指定 a.out 的头文件搜索目录（第一个是库名，第二个是目录）。

```cmake
cmake_minimum_required(VERSION 3.12)
project(hellocmake LANGUAGES CXX)

add_subdirectory(hellolib)

add_executable(a.out main.cpp)
target_link_libraries(a.out PUBLIC hellolib)
```

这样甚至可以用 <hello.h> 来引用这个头文件了，因为通过 target_include_directories 指定的路径会被视为与系统路径等价。

但是这样如果另一个 b.out 也需要用 hellolib 这个库，难道也得再指定一遍搜索路径吗？

不需要，其实我们只需要定义 hellolib 的头文件搜索路径，引用他的可执行文件 CMake 会**自动添加这个路径**：

```cmake
add_library(hellolib STATIC hello.cpp)
target_include_directories(hellolib PUBLIC .)
```

这里用了 . 表示当前路径，因为子目录里的路径是相对路径，类似还有 .. 表示上一层目录。

此外，如果不希望让引用 hellolib 的可执行文件自动添加这个路径，把 **PUBLIC** 改成**PRIVATE** 即可。这就是他们的用途：决定一个属性要不要在被 link 的时候传播。



#### CMake的一些其他选项

```cmake
除了头文件搜索目录以外，还有这些选项，PUBLIC 和 PRIVATE 对他们同理：
target_include_directories(myapp PUBLIC /usr/include/eigen3)  # 添加头文件搜索目录
target_link_libraries(myapp PUBLIC hellolib)                               # 添加要链接的库
target_add_definitions(myapp PUBLIC MY_MACRO=1)             # 添加一个宏定义
target_add_definitions(myapp PUBLIC -DMY_MACRO=1)         # 与 MY_MACRO=1 等价
target_compile_options(myapp PUBLIC -fopenmp)                     # 添加编译器命令行选项
target_sources(myapp PUBLIC hello.cpp other.cpp)                    # 添加要编译的源文件
以及可以通过下列指令（不推荐使用），把选项加到所有接下来的目标去：
include_directories(/opt/cuda/include)     # 添加头文件搜索目录
link_directories(/opt/cuda)                       # 添加库文件的搜索路径
add_definitions(MY_MACRO=1)             # 添加一个宏定义
add_compile_options(-fopenmp)             # 添加编译器命令行选项
```



#### 第三方库 - 作为纯头文件引入

1. nothings/stb - 大名鼎鼎的 stb_image 系列，涵盖图像，声音，字体等，只需单头文件！

2. Neargye/magic_enum - 枚举类型的反射，如枚举转字符串等（实现方式很巧妙）

3. g-truc/glm - 模仿 GLSL 语法的数学矢量/矩阵库（附带一些常用函数，随机数生成等）

4. Tencent/rapidjson - 单纯的 JSON 库，甚至没依赖 STL（可定制性高，工程美学经典）

5. ericniebler/range-v3 - C++20 ranges 库就是受到他启发（完全是头文件组成）

6. fmtlib/fmt - 格式化库，提供 std::format 的替代品（需要 -DFMT_HEADER_ONLY）

7. gabime/spdlog - 能适配控制台，安卓等多后端的日志库（和 fmt 冲突！）

只需要把他们的 include 目录或头文件下载下来，然后 include_directories(spdlog/include) 即可。

缺点：函数直接实现在头文件里，没有提前编译，从而需要重复编译同样内容，编译时间长。



#### 第三方库 - 作为子模块引入

第二友好的方式则是作为 CMake 子模块引入，也就是通过 add_subdirectory。

方法就是把那个项目（以fmt为例）的源码放到你工程的根目录：

这些库能够很好地支持作为子模块引入：

1. fmtlib/fmt - 格式化库，提供 std::format 的替代品

2. gabime/spdlog - 能适配控制台，安卓等多后端的日志库

3. ericniebler/range-v3 - C++20 ranges 库就是受到他启发

4. g-truc/glm - 模仿 GLSL 语法的数学矢量/矩阵库

5. abseil/abseil-cpp - 旨在补充标准库没有的常用功能

6. bombela/backward-cpp - 实现了 C++ 的堆栈回溯便于调试

7. google/googletest - 谷歌单元测试框架

8. google/benchmark - 谷歌性能评估框架

9. glfw/glfw - OpenGL 窗口和上下文管理

10. libigl/libigl - 各种图形学算法大合集



#### 引用系统中预安装的第三方库

可以通过 find_package 命令寻找系统中的包/库：

```cmake
find_package(fmt REQUIRED)
target_link_libraries(myexec PUBLIC fmt::fmt)
```

为什么是 fmt::fmt 而不是简单的 fmt？

现代 CMake 认为一个**包** (package) 可以提供多个**库**，又称**组件** (components)，比如 TBB 这个包，就包含了 tbb, tbbmalloc, tbbmalloc_proxy 这三个组件。

因此为避免冲突，每个包都享有一个独立的名字空间，以 :: 的分割（和 C++ 还挺像的）。

你可以指定要用哪几个组件：

```cmake
find_package(TBB REQUIRED COMPONENTS tbb tbbmalloc REQUIRED)
target_link_libraries(myexec PUBLIC TBB::tbb TBB::tbbmalloc)
```


#### 还可以使用包管理器安装第三方库



#### 实战 安装并使用RapidJSON库

将RapidJSON库放在include目录下，主文件夹CMakeLists.txt如下图所示：

```cmake
cmake_minimum_required(VERSION 3.12)
project(main)
add_executable(main main.cpp)
target_compile_features(main PUBLIC cxx_std_11)
target_include_directories(main PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include)
```



#### 实战 引入fmtlib/fmt库

使用子模块的方法导入即可。

```cmake
add_subdirectory(fmt)
target_link_libraries(main PUBLIC fmt)
```



#### 扩展 使用现代工具XMake

[xmake](https://xmake.io/#/)
