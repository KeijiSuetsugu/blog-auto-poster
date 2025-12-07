# 🚀 GitHub Secrets簡単設定ガイド

## 現在の状況

ログで以下が表示されています：
- `WORDPRESS_URL is set: NO`
- `WORDPRESS_USERNAME is set: NO`
- `WORDPRESS_PASSWORD is set: NO`
- `OPENAI_API_KEY is set: NO`

**これは、GitHub Secretsが設定されていないことを意味します。**

## ✅ 解決方法（超簡単3ステップ）

### ステップ1: GitHubリポジトリのSettingsページを開く

1. **ブラウザで以下を開く：**
   ```
   https://github.com/KeijiSuetsugu/blog-auto-poster
   ```

2. **画面上部の「Settings」タブをクリック**
   - リポジトリ名の右側にあるタブです

### ステップ2: Secretsページを開く

1. **左側のメニューを下にスクロール**
2. **「Secrets and variables」をクリック**
3. **「Actions」をクリック**

### ステップ3: 4つのSecretsを追加

**現在、Secretsの一覧が表示されているはずです。**
もし「You don't have any secrets」と表示されていれば、まだ何も設定されていません。

#### 1つ目: WORDPRESS_URL

1. 「**New repository secret**」ボタン（右上）をクリック
2. 以下を入力：
   - **Name**: `WORDPRESS_URL`（コピペしてOK）
   - **Secret**: `https://freeeeeeestyle.com`
3. 「**Add secret**」ボタンをクリック

#### 2つ目: WORDPRESS_USERNAME

1. 再度「**New repository secret**」ボタンをクリック
2. 以下を入力：
   - **Name**: `WORDPRESS_USERNAME`
   - **Secret**: `onepeace0710`
3. 「**Add secret**」ボタンをクリック

#### 3つ目: WORDPRESS_PASSWORD

1. 再度「**New repository secret**」ボタンをクリック
2. 以下を入力：
   - **Name**: `WORDPRESS_PASSWORD`
   - **Secret**: `sOf6 5CLI zoqo DCnS Xt66 bw2D`
   - ⚠️ **スペースも含めて全部コピー**
3. 「**Add secret**」ボタンをクリック

#### 4つ目: OPENAI_API_KEY

1. 再度「**New repository secret**」ボタンをクリック
2. 以下を入力：
   - **Name**: `OPENAI_API_KEY`
   - **Secret**: `.env`ファイルを開いて、`OPENAI_API_KEY=`の後の値をコピー
     - `.env`ファイルの場所：`/Users/keiji/Desktop/開発/新規事業（人間関係）/.env`
     - ターミナルで確認する場合：`cat .env | grep OPENAI_API_KEY`
3. 「**Add secret**」ボタンをクリック

## ✅ 確認

設定が完了したら、以下の4つが表示されているはずです：

- ✅ `WORDPRESS_URL`
- ✅ `WORDPRESS_USERNAME`
- ✅ `WORDPRESS_PASSWORD`
- ✅ `OPENAI_API_KEY`

## 🎯 次のステップ

Secretsを設定したら：

1. 「Actions」タブをクリック
2. 「毎日のブログ投稿」ワークフローを選択
3. 「Run workflow」ボタンをクリック
4. 今度は成功するはずです！

## ⚠️ 重要なポイント

1. **Nameは正確に入力**
   - `WORDPRESS_URL`（`WORDPRESS_URL `や`wordpress_url`ではない）
   - 大文字・小文字も正確に

2. **Secretの値も正確に**
   - 全部コピーできているか（途中で切れていないか）
   - 特にパスワードはスペースも含めて正確に

3. **4つすべてが必要**

## 🆘 まだ失敗する場合

もしSecretsを設定したのに「NO」と表示される場合：

1. **Secret名を再確認**
   - 大文字・小文字が正確か
   - 余分なスペースがないか

2. **ワークフローを再度実行**
   - Secretsを追加した後、再度「Run workflow」をクリック

3. **ログを確認**
   - 「環境変数を確認」ステップで、今度は「YES」になっているか確認

これで解決するはずです！






