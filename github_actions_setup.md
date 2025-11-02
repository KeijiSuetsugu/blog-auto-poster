# ☁️ GitHub Actionsで毎日自動投稿（PCがオフでもOK）

## 概要

GitHub Actionsを使えば、**パソコンをシャットダウンしていても**毎日自動でブログ記事を投稿できます。

GitHub Actionsは無料プランでも利用可能で、毎月2000分の実行時間が無料で利用できます（1日1回の実行なら十分に足ります）。

## セットアップ手順

### ステップ1: GitHubリポジトリを作成（まだの場合）

1. https://github.com にログイン
2. 右上の「+」→「New repository」をクリック
3. リポジトリ名を入力（例：「blog-auto-poster」）
4. 「Create repository」をクリック

### ステップ2: プロジェクトをGitにコミット

ターミナルで以下のコマンドを実行：

```bash
cd "/Users/keiji/Desktop/開発/新規事業（人間関係）"

# Gitリポジトリを初期化（まだの場合）
git init

# ファイルを追加（.envは除外される）
git add .

# コミット
git commit -m "初期コミット：WordPress自動投稿システム"

# GitHubリポジトリを追加（あなたのリポジトリURLに置き換えてください）
git remote add origin https://github.com/あなたのユーザー名/リポジトリ名.git

# プッシュ
git branch -M main
git push -u origin main
```

### ステップ3: GitHub Secretsに認証情報を設定

`.env`ファイルの内容をGitHub Secretsに設定します（セキュリティのため）。

1. GitHubリポジトリのページを開く
2. 「Settings」タブをクリック
3. 左メニューの「Secrets and variables」→「Actions」をクリック
4. 「New repository secret」をクリック
5. 以下のSecretsを追加：

**WORDPRESS_URL**
- Name: `WORDPRESS_URL`
- Value: `https://freeeeeeestyle.com`

**WORDPRESS_USERNAME**
- Name: `WORDPRESS_USERNAME`
- Value: `あなたのWordPressユーザー名を入力`

**WORDPRESS_PASSWORD**
- Name: `WORDPRESS_PASSWORD`
- Value: `あなたのアプリケーションパスワードを入力`

**OPENAI_API_KEY**
- Name: `OPENAI_API_KEY`
- Value: `あなたのOpenAI APIキーを入力`

**POST_TIME**（オプション）
- Name: `POST_TIME`
- Value: `09:00`

### ステップ4: GitHub Actionsワークフローを作成

#### 📁 フォルダを作る方法（2つの方法があります）

**⚠️ 実は、このフォルダはもう作成済みです！**  
プロジェクトフォルダの中に既に`.github/workflows/`フォルダができているので、このステップは飛ばしてOKです。

もし自分で手動で作る必要がある場合は、以下の方法で作れます：

##### 方法1: ターミナルで作る（コピペで簡単！）

ターミナル（黒い画面）を開いて、以下のコマンドをコピーして貼り付け、Enterキーを押します：

```bash
cd "/Users/keiji/Desktop/開発/新規事業（人間関係）"
mkdir -p .github/workflows
```

**説明：**
- `mkdir` = Make Directory（フォルダを作る）
- `-p` = 親フォルダも一緒に作る（`.github`がない場合、それも作ってくれる）
- `.github/workflows` = 作るフォルダの名前

##### 方法2: Finder（ファイルマネージャー）で作る

1. **Finderを開く**（Macの画面の下にある顔のアイコン）
2. **プロジェクトフォルダに移動**：
   - 左側のサイドバーから「デスクトップ」をクリック
   - 「開発」フォルダを開く
   - 「新規事業（人間関係）」フォルダを開く
3. **新しいフォルダを作る**：
   - フォルダ内で右クリック（または Control + クリック）
   - 「新規フォルダ」を選択
   - フォルダ名を「`.github`」と入力（**ピリオドから始まる**）
   - Enterキーを押す
4. **`.github`フォルダの中に入る**：
   - `.github`フォルダをダブルクリック
5. **さらに新しいフォルダを作る**：
   - フォルダ内で右クリック
   - 「新規フォルダ」を選択
   - フォルダ名を「`workflows`」と入力
   - Enterキーを押す

**これで完成！** `.github/workflows/`というフォルダができました。

#### 📄 ファイルを作る方法

**⚠️ 実は、ファイルも既に作成済みです！**  
`.github/workflows/daily_post.yml`というファイルが既にあるので、このステップも飛ばしてOKです。

もし自分で手動で作る必要がある場合は、以下の方法で作れます：

##### 方法1: VS Code（Cursor）で作る（簡単！）

1. **左側のファイル一覧を見る**（サイドバー）
2. **`.github`フォルダを探す**（ピリオドから始まるので、上か下の方にあるかもしれません）
3. **`.github`フォルダをクリックして開く**
4. **`workflows`フォルダをクリックして開く**
5. **`workflows`フォルダの中で右クリック**
6. **「新しいファイル」を選択**
7. **ファイル名を「`daily_post.yml`」と入力**
8. **ファイルの中に、下のコード（```yamlから```まで）をコピー＆ペースト**
9. **保存**（Command + S または Cursorのメニューから「保存」）

##### 方法2: ターミナルで作る

ターミナルを開いて、以下のコマンドを実行：

```bash
cd "/Users/keiji/Desktop/開発/新規事業（人間関係）"
mkdir -p .github/workflows
```

その後、エディタで`.github/workflows/daily_post.yml`というファイルを新規作成して、内容を貼り付けます。

**📝 ファイルを作る場所の説明：**

フォルダの構造は以下のようになります：

```
新規事業（人間関係）/
  ├── main.py
  ├── article_generator.py
  ├── .github/              ← このフォルダ（ピリオドから始まる）
  │   └── workflows/        ← この中
  │       └── daily_post.yml ← このファイルを作る！
  └── 他のファイル...
```

**「ディレクトリ」って何？**
- **ディレクトリ** = **フォルダ**と同じ意味です
- プログラマーは「ディレクトリ」と言うことが多いですが、フォルダと同じです
- 「`.github/workflows/`ディレクトリ」=「`.github/workflows/`というフォルダ」のことです

以下のファイルを作成（既にあれば上書きOK）：

`.github/workflows/daily_post.yml`（このファイルを作ります）

```yaml
name: 毎日のブログ投稿

on:
  schedule:
    # 毎日09:00（UTC）に実行
    # 日本時間（JST）はUTC+9なので、00:00 UTC = 09:00 JST
    - cron: '0 0 * * *'
  workflow_dispatch: # 手動実行も可能

jobs:
  post:
    runs-on: ubuntu-latest
    
    steps:
    - name: コードをチェックアウト
      uses: actions/checkout@v3
    
    - name: Pythonをセットアップ
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: 依存パッケージをインストール
      run: |
        pip install -r requirements.txt
    
    - name: 環境変数を設定
      env:
        WORDPRESS_URL: ${{ secrets.WORDPRESS_URL }}
        WORDPRESS_USERNAME: ${{ secrets.WORDPRESS_USERNAME }}
        WORDPRESS_PASSWORD: ${{ secrets.WORDPRESS_PASSWORD }}
        OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        POST_TIME: ${{ secrets.POST_TIME }}
    
    - name: ブログ記事を投稿
      run: python main.py
      env:
        WORDPRESS_URL: ${{ secrets.WORDPRESS_URL }}
        WORDPRESS_USERNAME: ${{ secrets.WORDPRESS_USERNAME }}
        WORDPRESS_PASSWORD: ${{ secrets.WORDPRESS_PASSWORD }}
        OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
```

### ステップ5: ファイルをGitHubにプッシュ（アップロード）

#### 🤔 このステップで何をするの？

作成したファイル（`daily_post.yml`）を、GitHubというクラウド（インターネット上）に**アップロード**します。

**例えるなら：**
- 写真を撮って、クラウド（iCloudやGoogleフォト）に保存するような感じ
- 今回の場合：作ったファイルをGitHubというインターネット上の倉庫に保存する

#### 📚 3つのコマンドの意味

以下の3つのコマンドを順番に実行します：

##### 1. `git add` = 「このファイルをアップロードリストに追加する」

**意味：**
- 「このファイルを保存するよ！」とGitに伝える
- 例えるなら：郵便局に行く前に、送りたい手紙を準備する感じ

##### 2. `git commit` = 「このファイルを保存する（説明を付けて）」

**意味：**
- ファイルを保存する（まだインターネットには送っていない）
- 一緒に「何を保存したか」の説明（メッセージ）も書く
- 例えるなら：手紙を封筒に入れて、表に「何を送ったか」を書く感じ

##### 3. `git push` = 「インターネット（GitHub）に送る」

**意味：**
- 保存したファイルを、インターネット上のGitHubに実際に送る
- 例えるなら：封筒をポストに入れる感じ

#### 🖥️ 実際にやってみよう

**ステップ1: ターミナルを開く**

1. Macの「ターミナル」アプリを開く
   - アプリ一覧から「ターミナル」を探す
   - または、「Spotlight検索」（Command + スペース）で「terminal」と入力

**ステップ2: プロジェクトフォルダに移動**

ターミナルが開いたら、以下のコマンドを**コピーして貼り付け**、Enterキーを押します：

```bash
cd "/Users/keiji/Desktop/開発/新規事業（人間関係）"
```

**説明：**
- `cd` = Change Directory（フォルダを移動する）
- これで、プロジェクトフォルダの中に入れます

**ステップ3: Gitリポジトリを初期化（初めての場合）**

もし、まだGitを使ったことがない（`.git`フォルダがない）場合は、以下を実行：

```bash
git init
```

**説明：**
- `git init` = このフォルダでGitを使う準備をする
- 一度だけ実行すればOK

**ステップ4: ファイルを追加（git add）**

以下のコマンドを**コピーして貼り付け**、Enterキーを押します：

```bash
git add .github/workflows/daily_post.yml
```

**何が起きるか：**
- `daily_post.yml`というファイルが「アップロードリスト」に追加されます
- エラーが出なければ、正常に動いています

**ステップ5: 保存する（git commit）**

以下のコマンドを**コピーして貼り付け**、Enterキーを押します：

```bash
git commit -m "GitHub Actionsワークフローを追加"
```

**説明：**
- `-m "..."` = メッセージ（説明文）を書く
- この場合：「GitHub Actionsワークフローを追加」という説明を付けて保存

**何が起きるか：**
- ファイルが保存されます
- 「1 file changed」のようなメッセージが表示されます

**ステップ6: GitHubに送る（git push）**

**⚠️ 重要：このステップの前に、ステップ2（GitHubリポジトリの作成）が完了している必要があります！**

以下のコマンドを**コピーして貼り付け**、Enterキーを押します：

```bash
git push origin main
```

または、もしブランチ名が`master`の場合は：

```bash
git push origin master
```

**何が起きるか：**
- ファイルがインターネット上のGitHubに送られます
- 初めての場合、ユーザー名とパスワード（またはトークン）を聞かれることがあります

#### 📝 全部まとめて実行する方法

上記の3つのコマンドを、**順番に**1つずつ実行します：

```bash
# 1つ目：ファイルを追加
git add .github/workflows/daily_post.yml

# 2つ目：保存する
git commit -m "GitHub Actionsワークフローを追加"

# 3つ目：GitHubに送る
git push origin main
```

**⚠️ 注意：**
- 必ず**順番に**実行してください
- 1つ目が終わってから2つ目、2つ目が終わってから3つ目を実行します

#### 🆘 エラーが出た場合

##### エラー: "fatal: not a git repository"

**意味：** まだGitの準備ができていない

**解決方法：**
```bash
git init
```
を実行してから、もう一度試してください。

##### エラー: "remote 'origin' does not exist"

**意味：** GitHubリポジトリとの接続がまだ設定されていない

**解決方法：**
ステップ2（GitHubリポジトリを作成）を先に完了させて、以下のコマンドを実行：

```bash
git remote add origin https://github.com/あなたのユーザー名/リポジトリ名.git
```

##### エラー: ユーザー名やパスワードを聞かれる

**⚠️ 重要：GitHubでは通常のパスワードは使えません！**

**解決方法：**
1. **GitHubのユーザー名を入力**（例：`KeijiSuetsugu`）
   - ⚠️ ディレクトリのパス（`cd "/Users/..."`）は入力しない
   - GitHubのユーザー名だけを入力

2. **パスワードの代わりにPersonal Access Tokenを使う**
   - GitHubの「Settings」→「Developer settings」→「Personal access tokens」→「Tokens (classic)」
   - 「Generate new token (classic)」をクリック
   - `repo`権限にチェックを入れる
   - トークンをコピー（一度しか表示されない！）
   - パスワードを聞かれたら、トークンを貼り付け

👉 **詳しい手順は [GitHub認証の方法.md](GitHub認証の方法.md) を参照してください。**

#### ✅ 成功したら

GitHubのリポジトリページを開いて、`.github/workflows/daily_post.yml`というファイルが表示されていれば成功です！

次のステップ（ステップ6）に進めます。

### ステップ6: 動作確認

1. GitHubリポジトリのページを開く
2. 「Actions」タブをクリック
3. 左メニューから「毎日のブログ投稿」ワークフローを選択
4. 「Run workflow」ボタンをクリックして手動実行でテスト

## スケジュールの変更

日本時間で毎日09:00に実行するには：
- UTC時間で00:00（日本時間09:00）に設定済み

他の時刻に変更する場合：
- `cron: '0 0 * * *'`の部分を変更
- UTC時間で指定（日本時間 - 9時間 = UTC時間）

例：
- 日本時間 18:00 → UTC 09:00 → `cron: '0 9 * * *'`
- 日本時間 12:00 → UTC 03:00 → `cron: '0 3 * * *'`

## メリット

✅ パソコンをシャットダウンしていても動作  
✅ 無料で利用可能  
✅ クラウドで実行されるため信頼性が高い  
✅ 実行ログがGitHubで確認できる  

## 注意事項

- `.env`ファイルは`.gitignore`に含まれているので、GitHubにはアップロードされません（安全）
- 認証情報は必ずGitHub Secretsに設定してください
- 無料プランは月2000分まで無料です（1日1回の実行なら十分です）

## トラブルシューティング

### ワークフローが実行されない

- GitHub Actionsが有効になっているか確認
- cron式が正しいか確認
- 「Actions」タブでエラーログを確認

### 認証エラー

- GitHub Secretsが正しく設定されているか確認
- Secretsの名前が大文字・小文字を含めて正確か確認

