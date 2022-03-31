
file_name="RSA算法详解.md"
op=0
ANS=""
with open(file_name,"r",encoding="utf-8") as f:
    for line in f:
        ans=""
        if "$$" in line:
            ANS=ANS+line
            continue
        for i in range(len(line)):
            if line[i]=='$':
                if op==0:
                    ans=ans+"\\\("
                else:
                    ans=ans+"\\\)"
                op=~op
            else:
                ans=ans+line[i]
        ANS=ANS+ans

with open(file_name,"w",encoding="utf-8") as f:
    f.write(ANS)