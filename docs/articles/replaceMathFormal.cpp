#include<stdio.h>
using namespace std;
char S[105];
int main(){
    puts("Please input file name:");
    scanf("%s",S+1);
    freopen(S+1,"r",stdin);
    
    return 0;
}