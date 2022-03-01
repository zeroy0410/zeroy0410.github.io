---
title: "高等数学（上） 定积分 总结"
date: 2022-02-17T12:18:48+08:00
draft: true
url: "articles/math-integrate2"
categories: ["文化课","Math"]
---

**定积分的定义**
$$
\lim_{n\to\infty}\sum_{i=1}^{n}f(\frac{i}{n})\frac{1}{n}=\int_{0}^{1}f(x)dx
$$
**常用公式：(还有其它的可在评论区补充)**
$$
\begin{align}
\int_{0}^{+\infty}x^ne^{-x}dx=n!
\end{align}
$$
**解题套路：**

1. 定积分的定义
2. 利用奇偶函数的性质
3. “区间再现”公式

例题：
$$
\begin{align}
I&=\int_{0}^{\frac{\pi}{2}}\frac{sinx}{sinx+cosx}dx
\overset{x+t=0+\frac{\pi}{2}}{=}\int_{\frac{\pi}{2}}^{0}\frac{sin({\frac{\pi}{2}-t})}{sin({\frac{\pi}{2}-t})+cos({\frac{\pi}{2}-t})}d(-t)\\\
&=\int_{0}^{\frac{\pi}{2}}\frac{cost}{sint+cost}dt\\\
&2I=\int_{0}^{\frac{\pi}{2}}\frac{sinx+cosx}{sinx+cosx}dx=\frac{\pi}{2}

\end{align}
$$
