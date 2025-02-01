# APPコンテナについて
Fast APIの稼働する環境


## ディレクトリ構成
```
.
├── app.md              # 本ファイル
├── dockerfile          # Dockerfile
└── requirements.txt    # python依存関係
```
---

# 環境変数
`.env`ファイルをAPPディレクトリ内に作成し、以下の環境変数を記述してください。

|環境変数名          |パラメータ              |用途                          |
|:------------------|:----------------------|:-----------------------------|
|ENV                |Dev                    |環境。テスト時にはtestとなる    |
|ALGORITHM          |HS256                  |ハッシュアルゴリズム            |
|DB_USERNAME        |testuser               |ユーザー名                     |
|DB_PASSWORD        |testuser1234           |DBパスワード                   |
|DB_HOSTNAME        |172.18.0.100           |DBのホスト名 or IP             |
|DB_PORT            |3306                   |DB port numbe                 |
|DB_NAME            |main                   |DB名                          |

※DB関連のパラメータはDBコンテナにて設定している環境変数の値と合わせて設定してください。


