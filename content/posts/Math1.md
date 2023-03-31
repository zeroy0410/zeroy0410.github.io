---
title: "高等数学（上） 不定积分 总结"
date: 2022-02-16T15:38:32+08:00
draft: false
categories: ["Math","文化课"]
url: "articles/math-integrate"
---



[高等数学上册(微积分)必背公式总结 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/106252437)

**导数：**
$$
\begin{align}
&[\cos(\omega x+\varphi)]^{(n)}=\omega^n\cos(\omega x+\frac{n\pi}{2}+\varphi)\\\
&[\sin(\omega x+\varphi)]^{(n)}=\omega^n\sin(\omega x+\frac{n\pi}{2}+\varphi)\\\
\end{align}
$$


**重难点公式：**
$$
\begin{align}
&\int\frac{1}{a^2+x^2}dx=\frac{1}{a}arctan\frac{x}{a}+C\\\
&\int\frac{1}{a^2-x^2}dx=\frac{1}{2a}ln|\frac{a+x}{a-x}|+C\\\
&\int\frac{1}{\sqrt{a^2-x^2}}dx=arcsin\frac{x}{a}+C\\\
&\int\frac{1}{\sqrt{x^2\pm a^2}}dx=ln|x+\sqrt{x^2\pm a^2}|+C\\\
&\int{tan\ x}dx=-ln|cos\ x|+C\\\
&\int{cot\ x}dx=ln|sin\ x|+C\\\
&\int{csc\ x}dx=ln|csc\ x-cot\ x|+C\\\
&\int{sec\ x}dx=ln|sec\ x+tan\ x|+C\\\
&\int{sec^2\ x}dx=tan\ x+C\\\
&\int{csc^2\ x}dx=-cot\ x+C\\\
&\int{sec\ x\*tan\ x}dx=sec\ x+C\\\
&\int{csc\ x\*cot\ x}dx=-csc\ x+C\\\
\end{align}
$$

**凑系数，拆项：**
$$
\int{\frac{x}{(2x+3)^2}}dx=\frac{1}{2}\int{\frac{2x+3-3}{(2x+3)^2}}dx=\frac{1}{2}\int{\frac{2x+3}{(2x+3)^2}}dx-\frac{1}{2}\int\frac{3}{(2x+3)^2}dx\\
...
$$
分子包含多项的，直接无法求解可以拆项求。

**常见的配凑：**
$$
\begin{align}
&xe^x:\\\
&\int\frac{1+x}{x(xe^x+1)}dx=\int\frac{(1+x)e^x}{xe^x(xe^x+1)}dx=\int\frac{1}{xe^x(xe^x+1)}d(xe^x)\overset{t=xe^x}=\int\frac{1}{t(t+1)}dt\\\
&xlnx:\\\
&\int\frac{(1+lnx)dx}{1+x^2ln^2x}=\int\frac{1}{1+(xlnx)^2}d(xlnx)\\\
&\frac{1}{\sqrt{x}}:\\\
&\int\frac{1}{\sqrt{x(x+4)}}dx=2\int\frac{1}{2\sqrt{x}\sqrt{x+4}}dx=2\int\frac{1}{\sqrt{4+\sqrt{x}^2}}d{\sqrt{x}}\\\
&e^x:\\\
&\int f(e^x){\rm dx}=\int\frac{f(e^x)}{e^x}{\rm de^x}=\int\frac{f(t)}{t}{\rm dt}
\end{align}
$$

**一些题目：**
\
1. 
$$
\begin{align}
(1):\int\frac{\rm dx}{x\sqrt{x^2-1}}
&=\int\frac{\rm dx}{x^2\sqrt{1-\left(\frac{1}{x}\right)^2}}\\\
&=-\int\frac{\rm d\frac{1}{x}}{\sqrt{1-\left(\frac{1}{x}\right)^2}}\\\
&=-\arcsin\frac{1}{x}+C\\\
\end{align}
$$
2. 
$$
\begin{align}
(2):\int\frac{x{\rm dx}}{x^2\sqrt{x^2-1}}&
=\int\frac{\rm d\sqrt{x^2-1}}{(\sqrt{x^2-1})^2+1}\\\
&=\arctan\sqrt{x^2-1}+C
\end{align}
$$
3. 
$$
(3)令\sqrt{x^2-1}=x-t,有x=\frac{t^2+1}{2t}\\\
\begin{align}
\int\frac{\rm dx}{x\sqrt{x^2-1}}
&=-2\int\frac{\rm dt}{t^2+1}\\\
&=-2\arctan t+C\\\
&=-2\arctan(x-\sqrt{x^2-1})+C
\end{align}
$$
4. 
$$
\begin{align}
(4)I=\int\sqrt{Ax^2+B}{\rm dx}
&=x\sqrt{Ax^2+B}-\int\frac{(Ax^2+B)-B}{\sqrt{Ax^2+B}}{\rm dx}\\\
&=x\sqrt{Ax^2+B}-I+\int\frac{B}{\sqrt{Ax^2+B}}{\rm dx}
\end{align}
$$

**奇怪的配凑：**
$$
\int\frac{1}{\sqrt{e^{2x}-1}}dx=\int\frac{1}{\sqrt{e^{2x}(1-e^{-2x})}}dx=\int\frac{e^{-x}}{\sqrt{1-e^{-2x}}}
$$
**有理函数积分：**
$$
\begin{align}
&\int\frac{x-2}{x^2+x+1}dx=\int\frac{A(x^2+x+1)'+B}{x^2+x+1}dx\\\
&A(2x+1)+B=x-2=>A=\frac{1}{2},B=-\frac{5}{2}\\\
&=\frac{1}{2}\int\frac{1}{x^2+x+1}d(x^2+x+1)-\frac{5}{2}\int\frac{1}{x^2+x+1}dx\\\
&=\frac{1}{2}\int\frac{1}{x^2+x+1}d(x^2+x+1)-\frac{5}{2}\int\frac{1}{(x+\frac{1}{2})^2+\frac{3}{4}}\\\
&\text{ps:当分母}\triangle<0\text{时才可以使用,否则直接裂项即可}
\end{align}
$$
**表格法求积分：**

[不定积分表格法的本质(推导) - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/391888816)
$$
\int{x^2e^{2x}}dx=\frac{1}{2}x^2e^{2x}-\frac{1}{2}xe^{2x}+\frac{1}{4}e^{2x}+C
$$
**常见三角换元题：**
$$
\begin{align}
&\int\frac{x^2}{\sqrt{1-x^2}}dx\overset{x=sint}{=}\int\frac{sin^2t}{\sqrt{1-sin^2t}}costdt=\int{sintdt}\\\
&\int{x^2{\sqrt{4-x^2}}}dx\overset{x=2sint}{=}16\int{sin^2tcos^2t}dt=8\int{(\frac{1}{2}sin2t)^2}dt\\\
\end{align}
$$
**凑微分：**
$$
\begin{align}
&\int\frac{1}{x\sqrt{1+x^2}}dx=\int{\frac{x}{x^2\sqrt{1+x^2}}}dx=\frac{1}{2}\int{\frac{1}{x^2\sqrt{1+x^2}}}dx^2\overset{t=x^2}{=}\frac{1}{2}\int{\frac{1}{t\sqrt{1+t}}}dt\\\
 &set\ u=\sqrt{1+t}\\\
 &=\frac{1}{2}\int{\frac{2u}{(u^2-1)u}}du=\int{\frac{1}{u^2-1}}du=-\frac{1}{2}ln|\frac{1+u}{1-u}|+C
\end{align}
$$
**倒代换：**
$$
\int{\frac{1}{x\sqrt{x^4+x^2+1}}}dx\overset{t=\frac{1}{x}}{=}-\int{\frac{1}{\frac{1}{t}\sqrt{\frac{1}{t^4}+\frac{1}{t^2}+1}}}dx=-\frac{\frac{1}{t}}{\sqrt{\frac{1}{t^4}+\frac{1}{t^2}+1}}dt=-\frac{1}{2}\int{\frac{1}{\sqrt{(t^2+\frac{1}{2})^2+(\frac{\sqrt{3}}{2})^2}}}d(t^2+\frac{1}{2})
$$


**一些巧题：**
$$
\begin{align}
&\int{\frac{1}{x\sqrt{x^2-1}}}dx=\int{\frac{1}{x\sqrt{x^2(1-\frac{1}{x^2})}}}dx=\int{\frac{1}{x^2\sqrt{1-\frac{1}{x^2}}}}=-\int{\frac{1}{\sqrt{1-(\frac{1}{x})^2}}}d(\frac{1}{x})\\\
&\int{\frac{1-lnx}{(x-lnx)^2}}dx=\int{\frac{\frac{1-lnx}{x^2}}{(1-\frac{lnx}{x})^2}}dx=-\int{\frac{1}{(1-\frac{lnx}{x})^2}}d(1-\frac{lnx}{x})\\\
&\int{\frac{1+x^2}{1+x^4}}dx=\int{\frac{\frac{1}{x^2}+1}{\frac{1}{x^2}+x^2}}dx=\int{\frac{d(x-\frac{1}{x})}{(x-\frac{1}{x})^2+2}}\\\
&\int{\frac{1}{1+x^4}}dx=\frac{1}{2}\int{\frac{1+x^2-(x^2-1)}{1+x^4}}dx\\\
\end{align}
$$
