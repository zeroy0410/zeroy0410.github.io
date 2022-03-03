---
title: "高等数学（上） 微分方程 总结"
date: 2022-02-27T19:57:59+08:00
draft: true
url: "articles/differential-equation"
categories: ["Math","文化课"]
---

#### 可分离变量的微分方程

将变量分离，两边同时积分。

1. 

$$
\begin{align}
& y'+xy^2-y^2=1-x\\
& => \frac{dy}{dx}=(1-x)(1+y^2)
\end{align}
$$

2. 

$$
\begin{align}
& xydx+(x^2+1)dy=0\\
& \frac{1}{y}dy=\frac{-x}{x^2+1}dx\\
& lny=-\frac{1}{2}ln(x^2+1)+lnC\\
& y=C(x^2+1)^{-\frac{1}{2}}
\end{align}
$$

#### 齐次微分方程

只含有y/x，令y/x=u，y=ux，将原方程化为可分离变量的微分方程。
$$
\begin{align}
& x\frac{dy}{dx}-y=2\sqrt{xy}(x>0)\\
& \frac{dy}{dx}-\frac{y}{x}=2\sqrt{\frac{y}{x}}\\
& set\ u=\frac{y}{x}\\
& x\frac{du}{dx}=2\sqrt{u}\\
\end{align}
$$
