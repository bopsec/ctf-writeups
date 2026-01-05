import math
import re

hex_str = """
01:ad:dc:d1:77:9f:21:c9:3d:22:68:03:7d:b4:d5:
    2f:12:10:ef:39:e9:05:d4:e5:3c:7c:a2:dc:34:81:
    ee:08:12:16:09:10:26:29:b6:02:5b:81:98:93:6a:
    e8:b8:ef:a5:e8:a9:d0:e3:58:8d:b6:31:4b:14:44:
    73:ad:8e:a8:11:17:ba:11:c6:ce:48:25:4e:74:d4:
    56:61:ee:eb:72:aa:34:39:81:c7:0d:28:61:ca:06:
    63:00:fc:9f:78:89:35:04:bb:34:38:e2:e2:bf:cd:
    10:7e:7a:59:33:2c:45:6f:d4:37:f5:2e:ca:8e:c4:
    f1:76:98:a6:10:cc:6c:5e:2f:30:f9:59:f3:c8:f1:
    4c:1c:73:36:18:8d:bb:65:ca:ba:53:70:0e:6d:ce:
    67:8b:9e:a7:04:47:37:7f:f4:47:2d:bb:04:af:2f:
    d0:af:ec:95:67:ff:d8:0b:c8:f6:6e:af:9a:16:eb:
    ca:1a:b9:e5:b0:2c:3c:49:8f:d8:31:60:fe:94:47:
    16:fd:26:4c:a4:e4:43:d1:3b:64:22:5e:7f:49:88:
    87:ca:82:d5:34:83:5a:a6:f8:48:3c:c3:d6:c3:fe:
    db:3c:c2:3c:39:22:a5:26:8c:b7:87:d1:7f:4e:4a:
    1f:c5:2a:7e:c0:49:a3:72:b7:28:1f:1b:76:69:e4:
    85:a6:39:a2:04:f6:87:94:43:26:90:5a:68:1c:7a:
    c6:0a:bf:7d:95:96:03:29:50:1f:ef:a5:f8:6c:23:
    af:a3:c0:81:3d:5f:05:1b:17:ab:83:69:85:f5:c4:
    78:be:91:e6:e7:26:62:d6:8a:66:9d:1d:03:e0:cc:
    1a:8e:b8:17:4e:1a:2e:7c:70:d3:e4:c7:2e:72:fa:
    7d:54:35:ab:44:ba:1d:7c:39:66:8b:1a:12:13:4d:
    c4:f6:99:15:4f:80:b2:ba:02:19:3a:52:54:d4:a1:
    d3:06:18:c5:e0:4a:2a:08:2e:b7:9d:36:45:6f:b3:
    35:45:9d:70:29:2b:78:90:01:58:2e:83:49:29:7d:
    62:ad:df:73:e7:e4:8e:79:cf:44:e6:c6:a4:df:8a:
    31:75:b1:8e:d3:d4:c8:6c:4f:a4:c8:e0:5f:1d:8d:
    1d:37:6a:4b:8b:32:cf:a5:70:7c:3e:30:54:ee:c5:
    44:d5:da:0c:21:4d:38:4c:49:ba:ec:f1:fb:69:08:
    46:52:cf:3c:60:fe:63:ce:87:1b:1c:88:cd:1b:25:
    95:8f:d5:b3:9a:9a:77:61:ac:86:c0:2c:ae:30:b9:
    70:a8:6a:7b:70:0a:17:7e:e8:65:4a:67:90:ce:ae:
    0f:ba:5d:28:2b:23:50:56:80:29:9f:f8:74:3f:8b:
    a5:fa:4a:7b:e0:ef:04:3d:af:56:ad:91:c3:b9:7a:
    5f:2d:10:1b:e0:1f:e4:de:c2:e4:2d:05:30:72:27:
    8c:cf:97:15:32:48:ed:bd:2e:39:86:3d:0f:a4:08:
    b0:84:c8:f7:d9:ef:c8:9b:04:bd:d9:50:d6:e5:d9:
    7b:a6:dd:6b:83:a7:9f:05:47:fa:12:d5:d6:6b:fd:
    4f:9b:50:57:c1:8f:f4:27:81:84:02:25:94:1f:f9:
    1f:c0:cd:72:73:6f:33:ff:0f:0a:e1:23:9c:96:d4:
    1b:ed:08:d6:86:0d:db:3d:1a:1c:1e:19:9d:18:c8:
    af:67:97:4e:bb:12:e2:7f:18:3e:06:03:7e:54:fd:
    fe:25:87:63:46:38:f8:b8:47:3d:2b:31:7f:51:21:
    78:f4:8b:b9:9a:96:66:0b:c3:09:92:31:7a:7c:21:
    57:be:6b:c4:1d:33:dd:ee:bb:91:2d:e9:43:ba:1e:
    07:c0:0d:20:9f:e1:0d:1c:28:0d:76:50:66:c8:47:
    93:47:ee:e8:c8:a7:ad:dd:b1:dc:20:51:34:39:bc:
    1b:be:1a:9c:6a:81:07:8a:c9:db:2e:e4:dd:f2:fa:
    c5:ce:3b:b3:b4:f3:b9:c8:ae:13:15:b8:ad:cf:54:
    ab:85:27:e9:cd:7c:75:6c:ab:5c:b5:2c:52:e5:d5:
    16:a5:ef:e2:b5:be:00:7d:66:7c:cd:55:5a:f0:24:
    f6:60:0b:af:a4:b7:88:35:96:58:6d:af:f5:e0:00:
    16:1a:76:fe:13:af:0e:10:80:04:fe:11:0f:95:60:
    42:5a:de:27:49:a1:44:32:e2:d6:db:6c:33:a6:98:
    a4:73:33:10:2c:65:59:ab:a0:c0:d1:62:d2:42:ef:
    1f:3e:8b:8e:4b:44:80:4d:32:14:3f:3f:3d:a0:b9:
    c2:e2:1d:da:4a:34:5f:5e:d6:58:88:bb:55:24:33:
    6d:0d:38:5b:5c:5a:f0:c0:5f:d9:5a:2e:4a:ec:5a:
    0a:72:a5:40:62:2d:2e:d1:b7:25:e0:4c:d8:e8:bd:
    66:68:dd:4f:82:33:2e:95:8d:a6:cf:74:67:f8:26:
    a5:09:0d:3f:98:65:76:25:d9:2e:c2:7c:69:ba:48:
    00:b3:bb:27:9a:6e:cd:87:b9:d6:28:08:13:1c:82:
    a9:1e:7d:02:1c:46:b5:69:2c:c2:cc:a5:f6:6e:0f:
    f5:e8:2b:3a:af:54:da:c2:e8:48:31:e2:ed
"""

hex_clean = re.sub(r'[^0-9a-fA-F]', '', hex_str)
n = int(hex_clean, 16)
e = 65537

def fermat_factor(n):
    a = math.isqrt(n)
    if a*a < n:
        a += 1

    i = 0
    while True:
        b2 = a*a - n
        b = math.isqrt(b2)
        if b*b == b2:
            return a-b, a+b
        a += 1
        i += 1

p, q = fermat_factor(n)

print("p =", p)
print("q =", q)

phi = (p-1)*(q-1)
d = pow(e, -1, phi)

print("d =", d)


# Nå kan jeg bare lage nøkkel direkte

from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateNumbers, RSAPublicNumbers
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
e = 65537

dp = d % (p-1)
dq = d % (q-1)
qi = pow(q, -1, p)

pub = RSAPublicNumbers(e, n)
priv = RSAPrivateNumbers(p, q, d, dp, dq, qi, pub).private_key(default_backend())

pem = priv.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.OpenSSH,
    encryption_algorithm=serialization.NoEncryption()
)

with open("john_key", "wb") as f:
    f.write(pem)

print("Saved as john_key")
