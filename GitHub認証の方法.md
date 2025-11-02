# 🔐 GitHub認証の方法（パスワードではなくトークンが必要）

## ⚠️ 重要な注意

**GitHubでは、2021年以降、通常のパスワード認証が廃止されました。**
代わりに**Personal Access Token（PAT）**という特別なキーを使う必要があります。

## 🎯 今すぐやること

### ステップ1: Personal Access Tokenを作成

#### 1. GitHubのサイトを開く

1. ブラウザで https://github.com にアクセス
2. ログインします

#### 2. Personal Access Tokenの作成ページを開く

以下のどちらかの方法で開きます：

**方法1:**
1. 右上の自分のアイコンをクリック
2. 「Settings」を選択
3. 左メニューの一番下にある「Developer settings」をクリック
4. 「Personal access tokens」→「Tokens (classic)」を選択
5. 「Generate new token」→「Generate new token (classic)」をクリック

**方法2（直接リンク）:**
- https://github.com/settings/tokens にアクセス
- 「Generate new token」→「Generate new token (classic)」をクリック

#### 3. トークンの設定

1. **Note（メモ）**: 何でもOK（例：「ブログ投稿用」）
2. **Expiration（有効期限）**: 
   - お好みで設定（例：90 days、または No expiration）
   - 長期間使うなら「No expiration」でもOK
3. **Select scopes（権限）**: 以下にチェックを入れる
   - ✅ **`repo`**（すべてにチェック）- リポジトリへのアクセス権限
   - ✅ **`workflow`** ← **重要！GitHub Actionsを使う場合必須**
   - または、必要な権限だけ：
     - ✅ `repo` の下のサブ項目：
       - ✅ `repo:status`
       - ✅ `repo_deployment`
       - ✅ `public_repo`
       - ✅ `repo:invite`
       - ✅ `security_events`
4. 画面を下にスクロールして、「**Generate token**」ボタンをクリック

#### 4. トークンをコピー

⚠️ **超重要**: トークンは**一度しか表示されません**！

- 表示されたトークン（`ghp_`で始まる長い文字列）を**今すぐコピー**
- メモ帳に保存しておく（後で見られないので）

例: `ghp_abcdefghijklmnopqrstuvwxyz1234567890ABCDEF`

### ステップ2: ターミナルで入力

#### 1. ユーザー名を入力

ターミナルに戻って、**GitHubのユーザー名**を入力します：

- ターミナルに「Username for 'https://github.com':」と表示されているはず
- そこに、**GitHubのユーザー名**（例：`KeijiSuetsugu`）を入力
- Enterキーを押す

**⚠️ 注意：**
- ディレクトリのパス（`cd "/Users/keiji/..."`）は**入力しない**
- GitHubのユーザー名だけを入力する

#### 2. パスワードの代わりにトークンを入力

次に「Password」と聞かれたら：

1. **コピーしたPersonal Access Tokenを貼り付け**
2. Enterキーを押す

**⚠️ 注意：**
- パスワードを入力する**場所にトークンを入力**する
- 入力しても画面には何も表示されない（通常のパスワードと同じ）
- でも大丈夫、入力されています

### ステップ3: 成功を確認

正しく入力されれば、以下のようなメッセージが表示されます：

```
Enumerating objects: X, done.
Counting objects: 100% (X/X), done.
...
To https://github.com/KeijiSuetsugu/blog-auto-poster.git
 * [new branch]      main -> main
Branch 'main' set up to track remote 'main'.
```

これが出れば成功です！

## 🆘 よくある問題

### 問題1: 「Username」のところに間違ってパスを入力してしまった

**解決方法：**
1. `Ctrl + C`でキャンセル
2. もう一度`git push origin main`を実行
3. 今度は**GitHubのユーザー名だけ**を入力

### 問題2: トークンを間違えてコピーした

**解決方法：**
1. もう一度Personal Access Tokenを作成
2. 古いトークンは削除してもOK（Securityタブから削除可能）
3. 新しいトークンで再度試す

### 問題3: 「Authentication failed」エラーが出る

**原因：**
- トークンが間違っている
- トークンの権限が足りない

**解決方法：**
1. トークンを再確認
2. トークンに`repo`権限が付いているか確認
3. 必要に応じて新しいトークンを作成

### 問題4: トークンを入力しても何も表示されない

**答え：** これは正常です！
- セキュリティのため、パスワード/トークン入力時は何も表示されません
- 入力されているので、そのままEnterキーを押してください

## 💡 ヒント

### トークンを安全に保存する方法

- メモ帳アプリに保存
- パスワード管理アプリ（1Password、LastPassなど）に保存
- ただし、**絶対にGitHubにコミットしないでください**（`.env`ファイルも同じ）

### 次回から簡単にする方法

一度トークンで認証すれば、Macのキーチェーンに保存される場合があります。
次回から自動で認証されることがあります。

## ✅ まとめ

1. ✅ GitHubでPersonal Access Tokenを作成（`repo`権限が必要）
2. ✅ トークンをコピー（一度しか表示されないので注意）
3. ✅ ターミナルでユーザー名を入力（GitHubのユーザー名）
4. ✅ パスワードの代わりにトークンを貼り付け
5. ✅ Enterキーを押して完了

これで、ファイルがGitHubにアップロードされます！

