# mysterytwisterc3-challenge-AES key — encoded in the machine readable zone of a European ePassport


#### 题目大意

你收到了一个AES加密的消息（使用CBC模式，零初始化向量和01-00填充）。此外，你还收到了相应的密钥，但不幸的是，密钥的形式并不完整，类似于身份文件上的机器可读区域（MRZ），就像在欧洲使用的电子护照中一样。

```
12345678<8<<<1110182<111116?<<<<<<<<<<<<<<<4
```

现在需要你恢复出密钥，并用恢复出的密钥解密以下文本：
```
9MgYwmuPrjiecPMx61O6zIuy3MtIXQQ0E59T3xB6u0Gyf1gYs2i3K9Jxaa0zj4gTMazJuApwd6+jdyeI5iGHvhQyDHGVlAuYTgJrbFDrfB22Fpil2NfNnWFBTXyf7SDI
```

参考资料：

https://www.icao.int/publications/pages/publication.aspx?docnum=9303

https://github.com/Joel-Q-Xu/MT3-mysterytwisterc3



#### Step1 恢复？处信息

![1](1.png)

```python
# 第一步, 破解"?"处的字符
array = [1, 1, 1, 1, 1, 6]
weights = [7, 3, 1, 7, 3, 1]
question_mark = 0
for i in range(len(array)):
    question_mark += array[i] * weights[i]
    question_mark %= 10
print(question_mark)
//7
```



#### Step2 恢复MRZ_INFORMATION与K_SEED

![2](2.png)

```python
# 第二步 恢复MRZ_INFORMATION与K_SEED
from hashlib import sha1
passport = '12345678<8<<<1110182<1111167<<<<<<<<<<<<<<<4'
no = passport[:10]
birth = passport[13:20]
arrive = passport[21:28]
mrz = no+birth+arrive
h_mrz = sha1(mrz.encode()).hexdigest()
k_seed = h_mrz[:32]
print(k_seed)
```



#### Step3 由K_SEED解出K_a, K_b

![3](3.png)

![4](4.png)

```python
def adjusting_the_parity_bit(x):
    ans = []
    tmp = bin(int(x, 16))[2:] 
    # 将输入参数x解析为16进制，并转换为二进制表示形式。
    # 然后，将二进制表示中的前缀"0b"去除，得到一个二进制字符串tmp。
    for i in range(0, len(tmp), 8):
        if tmp[i:i+7].count('1') % 2 == 0:
            ans.append(tmp[i:i+7] + '1')
        else:
            ans.append(tmp[i:i+7] + '0')
    ans = hex(int(''.join(ans), 2))
    # 将结果列表ans中的二进制字符串连接起来，并将其转换为十六进制表示形式。
    return ans[2:]
    # 返回调整后的结果，去除十六进制表示中的前缀"0x"。

c = '00000001'
D = k_seed + c
H = sha1(bytes.fromhex(D)).hexdigest()
K_a = adjusting_the_parity_bit(H[:16])
K_b = adjusting_the_parity_bit(H[16:32])
key = K_a+K_b
# ea8645d97ff725a898942aa280c43179
```



#### Step4 由生成的Key解出明文

```python
from Crypto.Cipher import AES
import base64

cipher = '9MgYwmuPrjiecPMx61O6zIuy3MtIXQQ0E59T3xB6u0Gyf1gYs2i3K9Jxaa0zj4gTMazJuApwd6+jdyeI5iGHvhQyDHGVlAuYTgJrbFDrfB22Fpil2NfNnWFBTXyf7SDI'
cipher = base64.b64decode(cipher)
 
aes = AES.new(bytes.fromhex(key),AES.MODE_CBC,bytes.fromhex('0'*32))
result = aes.decrypt(cipher).decode()
print(result)
# Herzlichen Glueckwunsch. Sie haben die Nuss geknackt. Das Codewort lautet: Kryptographie!
```



#### 总结

![5](5.png)

这次作业不仅仅是针对某一种加解密算法的攻击，而是让我体验到了现实中的密钥加解密标准，受益匪浅。

