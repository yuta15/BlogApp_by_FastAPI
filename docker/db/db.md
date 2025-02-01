# DBコンテナについて
DB用のコンテナを作成する。

## 構成
- バージョン: mysql:latest
- DB名: main
- テーブル名:
    - user
    - article

## ディレクトリ構成
```
.
├── conf.d
│   └── my.cnf              # mysqlの設定を記述
├── db_container.md         # 本資料
├── dockerfile              # DB用Dockerfile
├── initdb.d                
│   └── 0_create_table.sql  # 初期テーブル作成用SQL
└── .env                    # 環境変数を設定する為に使用。自分で作成して下しさい。
```
---

# 環境変数
`.env`ファイルをdbディレクトリ内に作成し、以下の環境変数を記述してください。

|環境変数名          |パラメータ              |用途                          |
|:------------------|:----------------------|:-----------------------------|
|MYSQL_ROOT_PASSWORD|rootuserpassword       |ルートパスワード               |
|MYSQL_DATABASE     |main                   |データベース名                 |
|MYSQL_USER         |testuser               |ユーザー名                     |
|MYSQL_PASSWORD     |testuser1234           |パスワード                     |
※パラメータは例です。


