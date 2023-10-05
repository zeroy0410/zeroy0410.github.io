---
title: "现代密码学 大作业 1"
date: 2023-10-05T15:04:05+08:00
draft: false
url: "posts/cryptography-programing-homework1"
categories: ["现代密码学"]
---

### CBC Padding Oracle

#### 适用条件

1. 已知iv
2. 使用PKCS7来Padding
3. 解密时检测到Padding错误会有回显

#### 攻击过程

首先回顾CBC的解密过程：

![](cbc_decryption.png)

不难发现，当我们可以控制当前Block的上一个Ciphertext时，有以下式子：

```
plaintext_block = AES_DEC(ciphertext_block) XOR user_controlled_value
```

又由于plaintext_block合法时末尾仅可能为：

```
01
02 02
03 03 03
04 04 04 04
05 05 05 05 05
...
```

因此，可以采用**逐位试探**的方法，从低位到高位，调整user_controlled_value，使得plaintext_block通过PKCS7校验。

然后，对于当前这位，假设目前试到了01，那么有：

```
01 = AES_DEC(ciphertext_block) XOR user_controlled_bytes
=> 
real_plaintext_block = AES_DEC(ciphertext_block) XOR user_controlled_bytes XOR user_controlled_bytes XOR real_iv = 01 XOR user_controlled_bytes XOR real_iv
```

其它位以此类推即可。

#### 特殊情况

需要注意的是，还可能存在特殊情况，假设在试01的时候，这串字符串的后三位是这样的：

```
04 04 04 ?
```

那么这位数最后解密的结果为01和04都能够通过PKCS7校验。遇到这种情况就要一个个试，假设是01或者04，再往后找一位，如果后一位能找到合法解，就采用当前解。

#### 代码

```python
from utils import *
from random import randint
from Crypto import Random
from Crypto.Cipher.AES import block_size, key_size
from base64 import b64decode

strings = [
    "MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=",
    "MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=",
    "MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==",
    "MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==",
    "MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl",
    "MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==",
    "MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==",
    "MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=",
    "MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=",
    "MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93",
]

class Oracle:

    def __init__(self, possible_inputs):
        self.iv = Random.new().read(block_size)
        self._key = Random.new().read(key_size[0])
        self._possible_inputs = possible_inputs

    def get_encrypted_message(self):
        chosen_input = self._possible_inputs[randint(0, len(self._possible_inputs) - 1)].encode()
        return aes_cbc_encrypt(chosen_input, self._key, self.iv)

    def decrypt_and_check_padding(self, ciphertext, iv):
        plaintext = aes_cbc_decrypt(ciphertext, self._key, iv, False)
        return is_pkcs7_padded(plaintext)


def create_forced_previous_block(iv, guessed_byte, padding_len, found_plaintext):
    index_of_forced_char = len(iv) - padding_len
    forced_character = iv[index_of_forced_char] ^ guessed_byte ^ padding_len
    output = iv[:index_of_forced_char] + bytes([forced_character])

    m = 0
    for k in range(block_size - padding_len + 1, block_size):
        forced_character = iv[k] ^ found_plaintext[m] ^ padding_len
        output += bytes([forced_character])
        m += 1

    return output


def attack_padding_oracle(ciphertext, oracle):
    plaintext = b''
    ciphertext_blocks = [oracle.iv] + [ciphertext[i:i + block_size] for i in range(0, len(ciphertext), block_size)]

    for c in range(1, len(ciphertext_blocks)):
        plaintext_block = b'' 
        for i in range(block_size - 1, -1, -1):
            padding_len = len(plaintext_block) + 1
            possible_last_bytes = []

            for j in range(256):
                forced_iv = create_forced_previous_block(ciphertext_blocks[c - 1], j, padding_len, plaintext_block)
                if oracle.decrypt_and_check_padding(ciphertext_blocks[c], forced_iv) is True:
                    possible_last_bytes += bytes([j])

            if len(possible_last_bytes) != 1:
                for byte in possible_last_bytes:
                    for j in range(256):
                        forced_iv = create_forced_previous_block(ciphertext_blocks[c - 1], j, padding_len + 1,
                                                                 bytes([byte]) + plaintext_block)

                        if oracle.decrypt_and_check_padding(ciphertext_blocks[c], forced_iv) is True:
                            possible_last_bytes = [byte]
                            break

            plaintext_block = bytes([possible_last_bytes[0]]) + plaintext_block

        plaintext += plaintext_block

    return pkcs7_unpad(plaintext)


def main():

    for string in strings:
        oracle = Oracle([string])
        result = attack_padding_oracle(oracle.get_encrypted_message(), oracle)
        
        print(b64decode(result.decode()))


if __name__ == '__main__':
    main()
```



### Break "random access read/write" AES CTR

#### 适用条件

由于CTR模式的特性，导致CTR模式的加解密算法是相同的，同时，CTR模式是可并行化处理的，也就意味着CTR模式可以访问其中任意一个块进行加密或者解密。

1. 多次的加密解密

#### 攻击过程

核心：将Ciphertext再跑一遍算法，得到的就是Plaintext。

注意使用offset计算首块和尾块的处理细节。

#### 代码

```python
from base64 import b64decode
from utils import *
from Crypto import Random
from Crypto.Cipher import AES 

class Oracle:
    
    def __init__(self) -> None:
        self._key = Random.new().read(AES.key_size[0])

    def encrypt(self, plaintext):
        return aes_ctr(plaintext, self._key, 0)
    
    def edit(self, ciphertext, offset, new_text):
        start_block = int(offset / AES.block_size)
        end_block = int((offset + len(new_text) - 1) / AES.block_size)

        keystream = b''
        cipher = AES.new(self._key, AES.MODE_ECB)
        for block in range(start_block, end_block + 1):
            keystream += cipher.encrypt(struct.pack('<QQ', 0, block))

        key_offset = offset % AES.block_size
        keystream = keystream[key_offset:key_offset + len(new_text)]

        insert = xor_data(new_text, keystream)

        return ciphertext[:offset] + insert + ciphertext[offset + len(insert):]
    
def break_random_access_read_write_aes_ctr(ciphertext, encryption_oracle):
    return encryption_oracle.edit(ciphertext, 0, ciphertext)

def main():
    with open("25.txt") as input_file:
        binary_data = b64decode(input_file.read())

    plaintext = aes_ecb_decrypt(binary_data, b'YELLOW SUBMARINE')
    oracle = Oracle()

    ciphertext = oracle.encrypt(plaintext)
    cracked_plaintext = break_random_access_read_write_aes_ctr(ciphertext, oracle)

    assert plaintext == cracked_plaintext
    print(cracked_plaintext.decode().rstrip())

if __name__ == "__main__":
    main()
```



### CTR bitflipping

它的前身是CBC bitflipping，会CBC bitflipping，自然会这个，所以下面先讲CBC bitflipping。

#### 适用场景

改变字符串中的特定字符。

#### 场景流程

生成随机 AES 密钥。

将填充代码和 CBC 代码结合起来编写两个函数。

第一个函数应该接受任意输入字符串，并在字符串前面添加：

```
comment1=cooking%20MCs;userdata=
```

后面添加：

```
;comment2=%20like%20a%20pound%20of%20bacon
```

该函数应该去除“;” 和“=”字符。

然后，该函数应将输入填充为 16 字节 AES 块长度，并使用随机 AES 密钥对其进行加密。

第二个函数应该解密字符串并查找字符“;admin=true;” 。

根据字符串是否存在返回 true 或 false。

#### 攻击流程

攻击的关键在于，插入的字符串中不能含有";"和"="，因此只能想办法绕过。

方法是，先将"?admin?true"加密，由于我们可以控制iv，并且已知明文为"?"，那么只需要将

```
iv XOR "?" XOR "?"/"="
```

就可以得到我们想要的解密结果。

#### 代码（CBC）

```python
from utils import aes_cbc_encrypt, aes_cbc_decrypt
from Crypto import Random
from Crypto.Cipher import AES


class Oracle:

    def __init__(self):
        self._key = Random.new().read(AES.key_size[0])
        self._iv = Random.new().read(AES.block_size)
        self._prefix = "comment1=cooking%20MCs;userdata="
        self._suffix = ";comment2=%20like%20a%20pound%20of%20bacon"

    def encrypt(self, data):
        data = data.replace(';', '').replace('=', '') 
        plaintext = (self._prefix + data + self._suffix).encode()
        return aes_cbc_encrypt(plaintext, self._key, self._iv)

    def decrypt_and_check_admin(self, ciphertext):
        data = aes_cbc_decrypt(ciphertext, self._key, self._iv)
        print(data)
        if b';admin=true;' in data:
            print("You have successfully logged in!")
        else:
            print("Something wrong!")

def cbc_bit_flip(encryption_oracle):
    block_length = 16
    prefix_length = 32

    additional_prefix_bytes = (block_length - (prefix_length % block_length)) % block_length
    total_prefix_length = prefix_length + additional_prefix_bytes

    plaintext = "?admin?true"
    additional_plaintext_bytes = (block_length - (len(plaintext) % block_length)) % block_length

    final_plaintext = additional_plaintext_bytes * '?' + plaintext
    ciphertext = encryption_oracle.encrypt(additional_prefix_bytes * '?' + final_plaintext)

    print("ciphertext: ", ciphertext)
    semicolon = ciphertext[total_prefix_length - 11] ^ ord('?') ^ ord(';')
    equals = ciphertext[total_prefix_length - 5] ^ ord('?') ^ ord('=')

    forced_ciphertext = ciphertext[:total_prefix_length - 11] + bytes([semicolon]) + \
                        ciphertext[total_prefix_length - 10: total_prefix_length - 5] + \
                        bytes([equals]) + ciphertext[total_prefix_length - 4:]

    return forced_ciphertext


def main():
    encryption_oracle = Oracle()
    forced_ciphertext = cbc_bit_flip(encryption_oracle)

    encryption_oracle.decrypt_and_check_admin(forced_ciphertext)


if __name__ == '__main__':
    main()
```

#### 代码（CTR）

```python
from utils import aes_ctr, xor_data
from Crypto import Random
from Crypto.Cipher import AES
from random import randint


class Oracle:

    def __init__(self):
        self._key = Random.new().read(AES.key_size[0])
        self._nonce = randint(0, 2 ** 32 - 1)        
        self._prefix = "comment1=cooking%20MCs;userdata="
        self._suffix = ";comment2=%20like%20a%20pound%20of%20bacon"

    def encrypt(self, data):
        data = data.decode().replace(';', '').replace('=', '')
        plaintext = (self._prefix + data + self._suffix).encode()
        return aes_ctr(plaintext, self._key, self._nonce)

    def decrypt_and_check_admin(self, ciphertext):
        data = aes_ctr(ciphertext, self._key, self._nonce)
        print(data)
        if b';admin=true;' in data:
            print("You have successfully logged in!")
        else:
            print("Something wrong!")

def ctr_bit_flip(encryption_oracle):
    block_length = 16
    prefix_length = 32

    plaintext = b"?admin?true"
    ciphertext = encryption_oracle.encrypt(plaintext)

    goal_text = b';admin=true'
    insert = xor_data(plaintext, goal_text)

    forced_ciphertext = ciphertext[:prefix_length] + \
                        xor_data(ciphertext[prefix_length:prefix_length + len(plaintext)], insert) + \
                        ciphertext[prefix_length + len(plaintext):]

    return forced_ciphertext


def main():
    encryption_oracle = Oracle()
    forced_ciphertext = ctr_bit_flip(encryption_oracle)

    encryption_oracle.decrypt_and_check_admin(forced_ciphertext)


if __name__ == '__main__':
    main()
```



### Recover the key from CBC with IV=Key

[参考链接](https://bernardoamc.com/ecb-iv-as-key/)

#### 前提条件

1. 加密程序使用相同的IV和KEY
2. 解密失败时，服务器抛出错误，并将解码的消息反映给攻击者

#### 攻击流程

1. 制作长度至少为3个块大小的明文
2. 加密明文，得到密文
3. 让密文的第二个块全0
4. 让密文的第三个块和第一个块一样
5. 解密该密文，得到认证失败的明文
6. 将第一段得到的明文和第三段得到的明文XOR
7. 得到KEY！

![](cbc_decryption.png)

```
first_block_ciphertext = AES_Decrypt(first_block_ciphertext, KEY) XOR KEY
third_block_ciphertext = AES_Decrypt(first_block_ciphertext, KEY) XOR second_block_ciphertext
=>
KEY = AES_Decrypt(first_block_ciphertext, KEY) XOR KEY XOR AES_Decrypt(third_block_ciphertext, KEY) XOR second_block_ciphertext
```

#### 代码

```python
from utils import *
from Crypto import Random

class Oracle:

    def __init__(self):
        self._key = Random.new().read(AES.key_size[0])
        self._iv = self._key
        self._prefix = "comment1=cooking%20MCs;userdata="
        self._suffix = ";comment2=%20like%20a%20pound%20of%20bacon"

    def encrypt(self, data):
        data = data.replace(';', '').replace('=', '') 
        plaintext = (self._prefix + data + self._suffix).encode()
        return aes_cbc_encrypt(plaintext, self._key, self._iv)

    def decrypt_and_check_admin(self, ciphertext):
        plaintext = aes_cbc_decrypt(ciphertext, self._key, self._iv)

        if not all(c < 128 for c in plaintext):
            raise Exception("The message is not valid", plaintext)

        if b';admin=true;' in plaintext:
            print("You have successfully logged in!")
        else:
            print("Something wrong!")

def get_key_from_insecure_cbc(encryption_oracle):

    block_length = 16
    prefix_length = 32

    p_1 = 'A' * block_length
    p_2 = 'B' * block_length
    p_3 = 'C' * block_length
    ciphertext = encryption_oracle.encrypt(p_1 + p_2 + p_3)

    forced_ciphertext = ciphertext[prefix_length:prefix_length + block_length] + b'\x00' * block_length + \
                        ciphertext[prefix_length:prefix_length + block_length]
    
    try:
        encryption_oracle.decrypt_and_check_admin(forced_ciphertext)
    except Exception as e:
        forced_plaintext = e.args[1]

        return xor_data(forced_plaintext[:block_length], forced_plaintext[-block_length:])

    raise Exception("Was not able to hack the key")

def main():
    encryption_oracle = Oracle()
    hacked_key = get_key_from_insecure_cbc(encryption_oracle)

    if encryption_oracle._key == hacked_key:
        print("Hacked!")
    else:
        print("Something Wrong!")
    assert encryption_oracle._key == hacked_key

if __name__ == '__main__':
    main()
```

