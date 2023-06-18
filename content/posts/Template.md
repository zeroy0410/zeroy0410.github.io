---
title: "Templates"
date: 2022-05-20T22:40:09+08:00
url: "articles/templates"
draft: False
---

> @zeroy.site

### 读入输出挂

```cpp
inline int read(){
	char c=getchar();
	int num=0,fl=1;
	while(c<48 || c>57){if(c=='-')fl=-1;c=getchar();}
	while(c>=48 && c<=57){num=(num<<1)+(num<<3)+(c^48);c=getchar();}
	return num*fl; 
}
inline void write(int x){
	if(x<0){
		putchar('-');
		x=-x;
	}
	if(x>9)write(x/10);
	putchar(x%10+'0');
}
```



### 正向表

```cpp
int tot=0,h[M];
struct edge{
    int nxt;
    int to,cost;
}G[3*M];
void add(int a,int b,int c){
    G[++tot]=(edge){h[a],b,c};
    h[a]=tot;
}
//图论题存图用的
//遍历：
for(int i=h[x];i;i=G[i].nxt){
    int u=G[i].to,v=G[i].cost;
    //...
}
```



### 基础数据结构

#### 树状数组

```cpp
void Add(int x,int d){
	while(x<=n){
        C[x]+=d;
        x+=(x&-x);
	}
}
int Sum(int x){
	int res=0;
    while(x){
		res+=C[x];
        x-=(x&-x);
    }
    return res;
}
//在线单点加值，查询前缀和，单次操作复杂度均为O(logn)
```

#### ST表

**预处理**

```cpp
void Init_RMQ(int n){
	for(int i=1;i<=n;i++)f[i][0]=A[i];
	lg2[1]=0;
	for(int i=2;i<=n;i++)lg2[i]=lg2[i>>1]+1;
	for(int j=1;(1<<j)<=n;j++)
		for(int i=1;i+(1<<j)-1<=n;i++)
			f[i][j]=max(f[i][j-1],f[i+(1<<(j-1))][j-1]);
} 
```

**查询**

```cpp
int query(int l,int r){
	int k=lg2[r-l+1];
	return max(f[l][k],f[r-(1<<k)+1][k]);
}
//预处理复杂度为O(nlogn),单次查询复杂度为O(1)
```

#### 线段树

```cpp
struct Segment_tree{
	#define fa tree[p]
	#define lson tree[p<<1]
	#define rson tree[p<<1|1]
	struct node{
		int l,r;
		LL add;//懒标记
        LL sum;
		int len(){return r-l+1;}
	}tree[M<<2];
	void up(int p){
		fa.sum=lson.sum+rson.sum;	
	}
	void down(int p){
		if(fa.add==0)return;
		lson.add+=fa.add;
		lson.sum+=fa.add*lson.len();
		rson.add+=fa.add;
		rson.sum+=fa.add*rson.len();
		fa.add=0;
	}
	void build(int l,int r,int p){
		fa.l=l;fa.r=r;fa.sum=fa.add=0;
		if(l==r){fa.sum=A[l];return;}
		int mid=(l+r)>>1;
		build(l,mid,p<<1);
		build(mid+1,r,p<<1|1);
		up(p);
	}
	void update(int l,int r,LL d,int p){
		if(fa.l==l&&fa.r==r){
			fa.sum+=1LL*fa.len()*d;
			fa.add+=d;
			return;
		}
		int mid=(fa.l+fa.r)>>1;
		down(p);
		if(r<=mid)update(l,r,d,p<<1);
		else if(l>mid)update(l,r,d,p<<1|1);
		else {
			update(l,mid,d,p<<1);
			update(mid+1,r,d,p<<1|1);	
		}
		up(p);
	}
	LL query(int l,int r,int p){
		if(fa.l==l&&fa.r==r)return fa.sum;
		down(p);
		int mid=(fa.l+fa.r)>>1;
		if(r<=mid)return query(l,r,p<<1);
		else if(l>mid)return query(l,r,p<<1|1);
		return query(l,mid,p<<1)+query(mid+1,r,p<<1|1);
	}
}T;
//区间加减，区间查询和，单次操作复杂度均为O(logn)
//可实现的变种：区间乘积，区间染色问题等等。
```

#### 并查集

```cpp
int getfa(int x){
	return fa[x]==x?x:fa[x]=getfa(fa[x]);
}
//初始状态下所有fa[x]=x
void Union(int x,int y){//两个集合合并
    fa[getfa(x)]=getfa(y);
}
```



### 树上算法

#### LCA

**跳重链**

```cpp
void dfs(int x,int f,int d){
	dep[x]=d;
	sz[x]=1;
	fa[x]=f;son[x]=0; 
	for(int i=0;i<G[x].size();i++){
		int u=G[x][i];
		if(u==f)continue;
		dfs(u,x,d+1);
		if(sz[u]>sz[son[x]])son[x]=u;
		sz[x]+=sz[u];
	}
}
void dfs_top(int x,int tp){
	top[x]=tp;
	if(son[x])dfs_top(son[x],tp);
	for(int i=0;i<G[x].size();i++){
		int u=G[x][i];
		if(u==fa[x]||u==son[x])continue;
		dfs_top(u,u);
	}
}
int LCA(int a,int b){
	while(top[a]!=top[b]){
		if(dep[top[a]]>dep[top[b]])a=fa[top[a]];
		else b=fa[top[b]];
	}
	return dep[a]>dep[b]?b:a;
}
```

**倍增**

```cpp
void dfs(int x,int f,int d){
	dep[x]=d;
	fa[x][0]=f;
	for(int i=0;i<G[x].size();i++){
		int u=G[x][i];
		if(u==f)continue;
		dfs(u,x,d+1);
	}
}
int LCA(int a,int b){
	if(dep[a]>dep[b])swap(a,b);
	int step=dep[b]-dep[a];
	for(int i=19;i>=0;i--)
		if(step&1<<i)b=fa[b][i];
	if(a==b)return a;
	for(int i=19;i>=0;i--)
		if(fa[a][i]!=fa[b][i])a=fa[a][i],b=fa[b][i];
	return fa[a][0];
} 
for(int j=1;j<=19;j++)
	for(int i=1;i<=n;i++)
		fa[i][j]=fa[fa[i][j-1]][j-1];
```

#### 树链剖分

**寻找重儿子**

```cpp
void dfs(int x,int f,int d){
	dep[x]=d;fa[x]=f;sz[x]=1;son[x]=0;
	for(int i=h[x];i;i=G[i].nxt){
		int u=G[i].to;
		if(u==f)continue;
		dfs(u,x,d+1); 
		if(sz[u]>sz[son[x]])son[x]=u;
		sz[x]+=sz[u];
	}
}
```

**处理top**

```cpp
void dfs_top(int x,int tp){
	top[x]=tp;ID[x]=++tt;ln[tt]=x;
	if(son[x])dfs_top(son[x],tp);
	for(int i=h[x];i;i=G[i].nxt){
		int u=G[i].to;
		if(u==son[x]||u==fa[x])continue;
		dfs_top(u,u);
	}
}
```

**query**

```cpp
while(top[u]!=top[v]){
	if(dep[top[u]]>dep[top[v]]){
		query(ID[top[u]],ID[u],1);
		u=fa[top[u]];
	}
	else {
		query(ID[top[v]],ID[v],1);
		v=fa[top[v]];
	}
} 
if(dep[u]>dep[v])query(ID[v],ID[u],1);
else query(ID[u],ID[v],1);
```



### 数学

#### 莫比乌斯反演

#### 定义

$\mu$ 为莫比乌斯函数，定义为

$$
\mu(n)=
\begin{cases}
1&n=1\\
0&n\text{ 含有平方因子}\\
(-1)^k&k\text{ 为 }n\text{ 的本质不同质因子个数}\\
\end{cases}
$$

```cpp
void getMu() {
  mu[1] = 1;
  for (int i = 2; i <= n; ++i) {
    if (!flg[i]) p[++tot] = i, mu[i] = -1;
    for (int j = 1; j <= tot && i * p[j] <= n; ++j) {
      flg[i * p[j]] = 1;
      if (i % p[j] == 0) {
        mu[i * p[j]] = 0;
        break;
      }
      mu[i * p[j]] = -mu[i];
    }
  }
}
```

#### 莫比乌斯变换

设 $f(n),g(n)$ 为两个数论函数。

形式一：如果有 $f(n)=\sum_{d\mid n}g(d)$，那么有 $g(n)=\sum_{d\mid n}\mu(d)f(\frac{n}{d})$。

形式二：如果有 $f(n)=\sum_{n|d}g(d)$，那么有 $g(n)=\sum_{n|d}\mu(\frac{d}{n})f(d)$。

#### 扩展欧几里得算法

```cpp
void exgcd(ll a,ll b,ll &d,ll &x,ll &y){
    if(!b){d=a;x=1;y=0;return;}
    exgcd(b,a%b,d,y,x);y-=a/b*x;
} 
```

#### 逆元

```cpp
int inv(int a){
    ll x,y,d;
    exgcd(a,m,d,x,y);
    return (x%MOD+MOD)%MOD;
}
//当a与mod互质时也可使用费马小定理，qkpow(a,mod-2)
int qkpow(int a,int b){
	int res=1;
    while(b){
		if(b&1)res=res*a%mod;
        a=a*a%mod;
        b>>=1;
    }
    return res;
}
//注意不要爆int或者long long
```

#### 线性筛逆元

```cpp
void Init(){
	fac[0]=1;rev[1]=1;
	for(int i=1;i<=n;i++)
		fac[i]=(fac[i-1]*i)%MOD;
	for(int i=2;i<=n;i++)//线性筛逆元 
		rev[i]=(MOD-MOD/i)*rev[MOD%i]%MOD;
}
```

#### FFT

```cpp
struct Complex{
	double x,y;
	Complex(){}
	Complex(double _x,double _y):x(_x),y(_y){}
	Complex operator + (const Complex &res) const{
		return (Complex){x+res.x,y+res.y};	
	}
	Complex operator - (const Complex &res) const{
		return (Complex){x-res.x,y-res.y};	
	}
	Complex operator * (const Complex &res) const{
		return (Complex){x*res.x-y*res.y,x*res.y+y*res.x};	
	}
};
Complex A[M],B[M];
double pi=acos(-1.0);
void FFT(Complex *y,int n,int f){
	if(n==1)return;
	Complex L[n>>1],R[n>>1];
	for(int i=0;i<n;i+=2)L[i>>1]=y[i],R[i>>1]=y[i+1];
	FFT(L,n>>1,f);FFT(R,n>>1,f);
	Complex wn(cos(2*pi/n),f*sin(2*pi/n)),w(1,0);
	for(int i=0;i<(n>>1);i++,w=w*wn){
		y[i]=L[i]+w*R[i];
		y[i+(n>>1)]=L[i]-w*R[i];
	}
}
double q[M],b[M],C[M];
int main(){
    //...
    int nn=n,mm=n;
	mm+=nn;
	for(nn=1;nn<=mm;nn<<=1);
	FFT(A,nn,1);FFT(B,nn,1);
	for(int i=0;i<=nn;i++)A[i]=A[i]*B[i];
	FFT(A,nn,-1);
    //...
}
```



### 字符串算法

#### KMP

给出两个字符串S1和S2，若S1的区间[l,r]与S2完全相同，则称S2在S1中出现了，其出现位置为l。

现在请你求出S2在S1中所有出现的位置。

定义一个字符串S的border为S的一个非S本身的子串t，满足t既是S的前缀，又是S的后缀。

对于S2，你还需要求出对于每个前缀S'的最长border t‘的长度。

```cpp
#include<bits/stdc++.h>
#define M 1000005
using namespace std;
char s1[M],s2[M];
int f[M];
void getf(char *s,int l){
	f[0]=f[1]=0;
	for(int i=1;i<l;i++){
		int j=f[i];
		while(j&&s[i]!=s[j])j=f[j];
		if(s[i]==s[j])j++;
		f[i+1]=j;
	}
}
int main(){
	scanf("%s%s",s1,s2);
	int l1=strlen(s1);
	int l2=strlen(s2);
	getf(s2,l2);
	for(int i=0,j=0;i<l1;i++){
		while(j&&s2[j]!=s1[i])j=f[j];
		if(s2[j]==s1[i])j++;
		if(j==l2)
			printf("%d\n",i-l2+2);
	}
	for(int i=1;i<=l2;i++)
		printf("%d ",f[i]);
	return 0;
}
```

#### 后缀数组

```cpp
int sa[M], rk[M], t1[M], t2[M], tmp[M], cnt1[M], cnt2[M], H[M];
struct node {
    char x;
    int id;
    bool operator<(const node &res) const {
        if (x != res.x)
            return x < res.x;
        return id < res.id;
    }
} A[M];
void Init(char *s, int n) {
    for (int i = 1; i <= n; i++)
        A[i] = (node){s[i], i};
    sort(A + 1, A + n + 1);
    for (int i = 1; i <= n; i++)
        sa[i] = A[i].id;
    rk[sa[1]] = 1;
    for (int i = 2; i <= n; i++) {
        rk[sa[i]] = rk[sa[i - 1]];
        if (s[sa[i]] != s[sa[i - 1]])
            rk[sa[i]]++;
    }
    for (int l = 1; rk[sa[n]] < n; l <<= 1) {
        for (int i = 0; i <= n; i++)
            cnt1[i] = cnt2[i] = 0;
        for (int i = 1; i <= n; i++)
            cnt1[t1[i] = rk[i]]++, cnt2[t2[i] = (l + i <= n) ? rk[i + l] : 0]++;
        for (int i = 1; i <= n; i++)
            cnt1[i] += cnt1[i - 1], cnt2[i] += cnt2[i - 1];
        for (int i = n; i >= 1; i--)
            tmp[cnt2[t2[i]]--] = i;
        for (int i = n; i >= 1; i--)
            sa[cnt1[t1[tmp[i]]]--] = tmp[i];
        rk[sa[1]] = 1;
        for (int i = 2; i <= n; i++) {
            rk[sa[i]] = rk[sa[i - 1]];
            if (t1[sa[i]] != t1[sa[i - 1]] || t2[sa[i]] != t2[sa[i - 1]])
                rk[sa[i]]++;
        }
    }
    for (int i = 1, j = 0; i <= n; i++) {
        j -= j > 0;
        while (s[i + j] == s[sa[rk[i] - 1] + j])
            j++;
        H[rk[i]] = j;
    }
}
struct Stable {
    int mn[M][22], Log[M];
    void Init(int n) {
        for (int i = 1; i <= n; i++) {
            mn[i][0] = H[i];
            if (i > 1)
                Log[i] = Log[i >> 1] + 1;
        }
        for (int j = 1; j < 22; j++)
            for (int i = 1; i + (1 << j - 1) <= n; i++)
                mn[i][j] = min(mn[i][j - 1], mn[i + (1 << j - 1)][j - 1]);
    }
    int Query(int l, int r) {
        int t = Log[r - l + 1];
        return min(mn[l][t], mn[r - (1 << t) + 1][t]);
    }
} st;
int LCP(int l, int r) {
    l = rk[l], r = rk[r];
    if (l > r)
        swap(l, r);
    return st.Query(l + 1, r);
}
```

