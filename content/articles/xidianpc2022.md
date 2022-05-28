---
title: "西安电子科技大学程序设计校赛2022 G&H"
date: 2022-05-27T22:23:52+08:00
draft: true
categories: ["ACM"]
---

[题目链接](https://acm.xidian.edu.cn/campus/2022/statements.pdf)

### G

#### 思路

关键词：**二进制，判断连通性**

不难发现，要优先选取高位的1。按位枚举，先把这位置为1丢进答案里，再把包含答案的点拎出来，看看能不能凑成包含起点到终点的路径的集合。如果可以说明最终答案这位是1，否则是0。

然后问题转化为给一堆可选点判断是否能让至少一组起点终点连通，我用了并查集，当然可以直接BFS，复杂度还更优Orz。

具体结合代码，不难理解。

#### 代码

```cpp
#include<stdio.h>
#include<iostream>
#define M 1000005
using namespace std;
int T,n,m,s,e;
int fa[M],A[M];
bool havS[M],havE[M];
bool stS[M],stE[M];
int dxy[4][2]={1,0,0,1,-1,0,0,-1};
int getfa(int x){return fa[x]==x?x:fa[x]=getfa(fa[x]);}
int Pos(int x,int y){return (x-1)*m+y;}
void Union(int x,int y){
    int rt1=getfa(x);
    int rt2=getfa(y);
    havS[rt2]=(havS[rt2]|havS[rt1]);
    havE[rt2]=(havE[rt2]|havE[rt1]);
    fa[rt1]=rt2;
}
int main(){
    scanf("%d",&T);
    while(T--){
        scanf("%d%d",&n,&m);
        for(int i=1;i<=n*m;i++){
            fa[i]=i;
            stS[i]=stE[i]=0;
        }
        scanf("%d",&s);
        for(int i=1,x,y;i<=s;i++){
            scanf("%d%d",&x,&y);
            stS[Pos(x,y)]=1;
        }
        scanf("%d",&e);
        for(int i=1,x,y;i<=e;i++){
            scanf("%d%d",&x,&y);
            stE[Pos(x,y)]=1;
        }
        for(int i=1;i<=n;i++)
            for(int j=1;j<=m;j++)
                scanf("%d",&A[Pos(i,j)]);
        long long ans=0;
        for(int i=30;i>=0;i--){
            long long tmp=(ans|(1<<i));
            for(int i=1;i<=n*m;i++){
                fa[i]=i;
                havS[i]=stS[i];
                havE[i]=stE[i];
            }
            for(int j=1;j<=n*m;j++){
                if((A[j]&tmp)==tmp){
                    int x=(j-1)/m+1;
                    int y=j-(x-1)*m;
                    for(int d=0;d<4;d++){
                        int dx=x+dxy[d][0];
                        int dy=y+dxy[d][1];
                        if(dx>n||dx<1||dy>m||dy<1)continue;
                        if((A[Pos(dx,dy)]&tmp)==tmp)Union(j,Pos(dx,dy));
                    }
                }
            }
            bool fl=0;
            for(int j=1;j<=n*m;j++){
                int rt=getfa(j);
                if(havS[rt]&&havE[rt]){
                    fl=1;
                    break;
                }
            }
            if(fl)ans|=(1<<i);
        }
        printf("%lld\n",ans);
    }
    return 0;
}
```



### H

#### 思路

先来看一个子问题：求一个非负数列\\(a\\)，\\(a_1=n\\)，要求\\(a_i>=a_{i+1}\\)，共\\(m\\)项的种数。

考虑将这个问题抽象为一个隔板模型。

```
o
--
oo
---
ooo
----
oooo
oooo
-----
ooooo
ooooo
ooooo
```

相当于在n个球之间放了m-1个隔板，且两个球之间可以放多个隔板，因为限制条件是非负和小于等于，所以最后一个球底下和第一个球顶上也可以放板子。

考虑n+m-1个球之间放m-1个隔板，每个隔板之间至少要有一个球，这样的方案数是C_{n+m-1}^{m-1}
