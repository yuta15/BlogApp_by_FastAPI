import uuid
import datetime
import random
import string
from uuid import UUID, uuid4


from app.models.Article import Article



def create_success_articles(
    user_id: UUID,
    number: int = 2,
    is_only_public: bool = False,
):
    """
    insert可能なArticleデータを作成する関数
    args:
        number: int=2
            作成するデータの数. default value is 2
        is_only_public: bool
            publicデータのみを作成したい場合はTrueを選択
        user_id: any
            特定のユーザーIDのArticleを作成したい場合にユーザーIDを指定。
            default value None
    return:
        articles: list
    """
    insert_articles = []
    now = datetime.datetime.now()
    while len(insert_articles) < number:
        insert_article = Article.model_validate(
            {
                'id': uuid4(),
                'title': ''.join(random.choices(string.ascii_letters + string.digits, k=10)),
                'body': """## はじめに
PrivateLinkの動作を確認してみた。

## 結論
マルチAZ環境においてPrivateLink接続を使用した場合、クロスゾーンロードバランシングが有効でない場合においては、エンドポイントのAZ次第で接続先のサーバが確定するということが分かった。
また、エンドポイントとVMを同一サブネット内に配置した場合、同一サブネット内のエンドポイントへ接続することが分かった。


![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1526482/af6b70ac-ec04-3817-66e0-0fa0eaa97052.png)

![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1526482/f4512a79-3cd3-81f7-96df-c55e65cea547.png)

まぁ、全部ここに書いてありましたが...
![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1526482/a56ae207-2631-4094-2366-6128e202f167.png)



## 検証内容
以下構成にて、Client1, Client2からエンドポイントのDNSへcurl接続を行った場合にどのようにどこに接続するかを確認した。
![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1526482/5f0fb533-4f13-5d38-0640-ee132adb2942.png)

SV-1,SV-2ではそれぞれApacheを動かしており、接続先がわかるよう以下のように設定した。
```
sv1
[root@ip-10-0-0-100 html]# curl http://localhost
<h1>sv-1<h1>
[root@ip-10-0-0-100 html]# 
```
```
sv2
[root@ip-10-0-1-100 html]# curl http://localhost
<h1>sv-2<h1>
[root@ip-10-0-1-100 html]#
```
接続するDNSは、1a、1cの両方へ解決されるDNSを使用した。
```
[ec2-user@ip-10-10-0-244 ~]$ dig vpce-0e44d14a27a369e43-rf450lif.vpce-svc-04ee54fb2f549cf66.ap-northeast-1.vpce.amazonaws.com

; <<>> DiG 9.16.48-RH <<>> vpce-0e44d14a27a369e43-rf450lif.vpce-svc-04ee54fb2f549cf66.ap-northeast-1.vpce.amazonaws.com
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 61139
;; flags: qr rd ra; QUERY: 1, ANSWER: 2, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;vpce-0e44d14a27a369e43-rf450lif.vpce-svc-04ee54fb2f549cf66.ap-northeast-1.vpce.amazonaws.com. IN A

;; ANSWER SECTION:
vpce-0e44d14a27a369e43-rf450lif.vpce-svc-04ee54fb2f549cf66.ap-northeast-1.vpce.amazonaws.com. 60 IN A 10.10.0.100
vpce-0e44d14a27a369e43-rf450lif.vpce-svc-04ee54fb2f549cf66.ap-northeast-1.vpce.amazonaws.com. 60 IN A 10.10.1.100

;; Query time: 0 msec
;; SERVER: 10.10.0.2#53(10.10.0.2)
;; WHEN: Wed Jun 12 12:43:49 UTC 2024
;; MSG SIZE  rcvd: 153

[ec2-user@ip-10-10-0-244 ~]$
```

### 結果
1a,1c共有となっているDNS名で接続したにもかかわらず、それぞれ同一AZのサーバーへ接続していることがわかる。
ただし、現段階ではエンドポイントとVMが同一サブネットに存在するため、同一サブネットが優先されている可能性が考えられる。
```
clietn1
Wed Jun 12 12:08:53 UTC 2024
<h1>sv-1<h1>
------------------------------------------------------
Wed Jun 12 12:08:53 UTC 2024
<h1>sv-1<h1>
------------------------------------------------------
Wed Jun 12 12:08:54 UTC 2024
<h1>sv-1<h1>
------------------------------------------------------
Wed Jun 12 12:08:54 UTC 2024
<h1>sv-1<h1>
------------------------------------------------------
Wed Jun 12 12:08:55 UTC 2024
<h1>sv-1<h1>
------------------------------------------------------
Wed Jun 12 12:08:55 UTC 2024
<h1>sv-1<h1>
------------------------------------------------------
Wed Jun 12 12:08:56 UTC 2024
<h1>sv-1<h1>
------------------------------------------------------
Wed Jun 12 12:08:56 UTC 2024
<h1>sv-1<h1>
------------------------------------------------------
Wed Jun 12 12:08:57 UTC 2024
<h1>sv-1<h1>
------------------------------------------------------
Wed Jun 12 12:08:57 UTC 2024
<h1>sv-1<h1>
------------------------------------------------------
Wed Jun 12 12:08:58 UTC 2024
<h1>sv-1<h1>
------------------------------------------------------
Wed Jun 12 12:08:58 UTC 2024
<h1>sv-1<h1>
--
```
```
clietn2
Wed Jun 12 12:08:53 UTC 2024
<h1>sv-2<h1>
------------------------------------------------------
Wed Jun 12 12:08:53 UTC 2024
<h1>sv-2<h1>
------------------------------------------------------
Wed Jun 12 12:08:54 UTC 2024
<h1>sv-2<h1>
------------------------------------------------------
Wed Jun 12 12:08:54 UTC 2024
<h1>sv-2<h1>
------------------------------------------------------
Wed Jun 12 12:08:55 UTC 2024
<h1>sv-2<h1>
------------------------------------------------------
Wed Jun 12 12:08:55 UTC 2024
<h1>sv-2<h1>
------------------------------------------------------
Wed Jun 12 12:08:56 UTC 2024
<h1>sv-2<h1>
------------------------------------------------------
Wed Jun 12 12:08:56 UTC 2024
<h1>sv-2<h1>
------------------------------------------------------
Wed Jun 12 12:08:57 UTC 2024
<h1>sv-2<h1>
------------------------------------------------------
Wed Jun 12 12:08:57 UTC 2024
<h1>sv-2<h1>
------------------------------------------------------
Wed Jun 12 12:08:58 UTC 2024
<h1>sv-2<h1>
------------------------------------------------------
Wed Jun 12 12:08:58 UTC 2024
<h1>sv-2<h1>
------------------------------------------------------
Wed Jun 12 12:08:59 UTC 2024
<h1>sv-2<h1>
------------------------------------------------------
Wed Jun 12 12:08:59 UTC 2024
<h1>sv-2<h1>
--
```

client1から1cのエンドポイントへ接続すると、1cのサーバーへ接続することがわかる。
```
[ec2-user@ip-10-10-0-244 ~]$ curl http://vpce-0e44d14a27a369e43-rf450lif-ap-northeast-1c.vpce-svc-04ee54fb2f549cf66.ap-northeast-1.vpce.amazonaws.com
<h1>sv-2<h1>
[ec2-user@ip-10-10-0-244 ~]$
```

### 別サブネット構成にて再度実施
![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1526482/73d66fb5-93e7-d985-c176-9b40a6174776.png)

今回は交互にロードバランスされることがわかる。
これはつまり、エンドポイントの名前解決が1a、1cのアドレスへと順番に解決されているとわかる。
そのため、同一サブネット内にエンドポイントが存在した場合は、同一サブネット内のエンドポイントへのみ解決されたということみたい。
```
client1
Wed Jun 12 13:22:02 UTC 2024
<h1>sv-2<h1>
Wed Jun 12 13:22:03 UTC 2024
<h1>sv-1<h1>
Wed Jun 12 13:22:03 UTC 2024
<h1>sv-2<h1>
Wed Jun 12 13:22:04 UTC 2024
<h1>sv-1<h1>
Wed Jun 12 13:22:04 UTC 2024
<h1>sv-2<h1>
Wed Jun 12 13:22:05 UTC 2024
<h1>sv-1<h1>
Wed Jun 12 13:22:05 UTC 2024
<h1>sv-2<h1>
```
```
Wed Jun 12 13:23:00 UTC 2024
<h1>sv-2<h1>
Wed Jun 12 13:23:00 UTC 2024
<h1>sv-1<h1>
Wed Jun 12 13:23:01 UTC 2024
<h1>sv-2<h1>
Wed Jun 12 13:23:02 UTC 2024
<h1>sv-1<h1>
Wed Jun 12 13:23:02 UTC 2024
<h1>sv-2<h1>
Wed
```
### ターゲットを削除してみた
クロスゾーンロードバランシング無効化の状態でターゲットを削除すると、
削除中に接続があった場合は接続断になった。
再試行するとSV-2のみに接続できた。
![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1526482/eb843a6f-8de8-a954-2f3e-fc5db6b7c08c.png)

```
 % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:--  0:01:18 --:--:--     0

  0     0    0     0    0     0      0      0 --:--:--  0:01:19 --:--:--     0^C
```
```
client1
Wed Jun 12 13:40:43 UTC 2024
<h1>sv-2<h1>
Wed Jun 12 13:40:43 UTC 2024
<h1>sv-2<h1>
Wed Jun 12 13:40:44 UTC 2024
<h1>sv-2<h1>
Wed Jun 12 13:40:44 UTC 2024
<h1>sv-2<h1>
Wed Jun 12 13:40:45 UTC 2024
<h1>sv-2<h1>
Wed Jun 12 13:40:46 UTC 2024
<h1>sv-2<h1>
```
```
client2
Wed Jun 12 13:39:19 UTC 2024
Wed Jun 12 13:40:40 UTC 2024
<h1>sv-2<h1>
Wed Jun 12 13:40:41 UTC 2024
<h1>sv-2<h1>
Wed Jun 12 13:40:41 UTC 2024
<h1>sv-2<h1>
Wed Jun 12 13:40:42 UTC 2024
<h1>sv-2<h1>
Wed Jun 12 13:40:42 UTC 2024
<h1>sv-2<h1>
```

### クロスゾーンロードバランシング有効化

有効化すると順番にならなくなった。
```
<h1>sv-1<h1>
Wed Jun 12 13:36:15 UTC 2024
<h1>sv-2<h1>
Wed Jun 12 13:36:16 UTC 2024
<h1>sv-1<h1>
Wed Jun 12 13:36:16 UTC 2024
<h1>sv-1<h1>
Wed Jun 12 13:36:17 UTC 2024
<h1>sv-1<h1>
Wed Jun 12 13:36:17 UTC 2024
<h1>sv-1<h1>
Wed Jun 12 13:36:18 UTC 2024
<h1>sv-2<h1>
Wed Jun 12 13:36:18 UTC 2024
<h1>sv-2<h1>
Wed Jun 12 13:36:19 UTC 2024
<h1>sv-1<h1>
Wed Jun 12 13:36:20 UTC 2024
<h1>sv-2<h1>
Wed Jun 12 13:36:20 UTC 2024
<h1>sv-2<h1>
Wed Jun 12 13:36:21 UTC 2024
<h1>sv-2<h1>
Wed Jun 12 13:36:21 UTC 2024
<h1>sv-2<h1>
```
```
Wed Jun 12 13:36:09 UTC 2024
<h1>sv-1<h1>
Wed Jun 12 13:36:09 UTC 2024
<h1>sv-2<h1>
Wed Jun 12 13:36:10 UTC 2024
<h1>sv-1<h1>
Wed Jun 12 13:36:10 UTC 2024
<h1>sv-1<h1>
Wed Jun 12 13:36:11 UTC 2024
<h1>sv-1<h1>
Wed Jun 12 13:36:11 UTC 2024
<h1>sv-2<h1>
Wed Jun 12 13:36:12 UTC 2024
<h1>sv-1<h1>
Wed Jun 12 13:36:12 UTC 2024
<h1>sv-1<h1>
Wed Jun 12 13:36:13 UTC 2024
<h1>sv-1<h1>
Wed Jun 12 13:36:13 UTC 2024
<h1>sv-1<h1>
Wed Jun 12 13:36:14 UTC 2024
<h1>sv-1<h1>
Wed Jun 12 13:36:14 UTC 2024
<h1>sv-1<h1>
Wed Jun 12 13:36:15 UTC 2024
<h1>sv-1<h1>
Wed Jun 12 13:36:15 UTC 2024
<h1>sv-1<h1>
Wed Jun 12 13:36:16 UTC 2024
<h1>sv-2<h1>
```

### ターゲットを削除してみる
クロスゾーンロードバランシングを有効化していると削除しても通信断にならず、
スムーズに切り替わりが実現できた。
```
client1
<h1>sv-2<h1>
Wed Jun 12 13:48:24 UTC 2024
<h1>sv-1<h1>
Wed Jun 12 13:48:25 UTC 2024
<h1>sv-2<h1>
Wed Jun 12 13:48:25 UTC 2024
<h1>sv-2<h1>
Wed Jun 12 13:48:26 UTC 2024
<h1>sv-2<h1>
Wed Jun 12 13:48:26 UTC 2024
<h1>sv-2<h1>
Wed Jun 12 13:48:27 UTC 2024
<h1>sv-2<h1>
```
```
client2
<h1>sv-1<h1>
Wed Jun 12 13:48:23 UTC 2024
<h1>sv-2<h1>
Wed Jun 12 13:48:24 UTC 2024
<h1>sv-1<h1>
Wed Jun 12 13:48:24 UTC 2024
<h1>sv-2<h1>
Wed Jun 12 13:48:25 UTC 2024
<h1>sv-2<h1>
Wed Jun 12 13:48:25 UTC 2024
<h1>sv-2<h1>
Wed Jun 12 13:48:26 UTC 2024
<h1>sv-2<h1>
Wed Jun 12 13:48:27 UTC 2024
<h1>sv-2<h1>
```
""",
                'created_at': now,
                'updated_at': now,
                'is_public': is_only_public if is_only_public else bool(number % 2),
                'user_id': user_id
            }
        )
        insert_articles.append(insert_article)
    return insert_articles
    