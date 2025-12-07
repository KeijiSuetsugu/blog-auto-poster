# 🔧 GitHub Actionsエラー対処法

## エラーメッセージ

```
Process completed with exit code 1
```

## 考えられる原因

1. **GitHub Secretsが設定されていない**
2. **Pythonコードの実行エラー**
3. **依存パッケージのインストールエラー**
4. **環境変数が正しく読み込めていない**

## ✅ 解決方法

### ステップ1: エラーログを詳しく見る

1. GitHubリポジトリページで「Actions」タブをクリック
2. 失敗したワークフロー実行をクリック
3. 「post」ステップをクリックして、詳細なログを確認
4. エラーメッセージを探す

### ステップ2: GitHub Secretsを確認・設定

**これが最も可能性が高い原因です！**

1. GitHubリポジトリページで「Settings」タブをクリック
2. 左メニューの「Secrets and variables」→「Actions」をクリック
3. 以下の4つのSecretsが設定されているか確認：

   - ✅ `WORDPRESS_URL` = `https://your-site.com`
   - ✅ `WORDPRESS_USERNAME` = `your-username`
   - ✅ `WORDPRESS_PASSWORD` = `your-application-password`
   - ✅ `OPENAI_API_KEY` = `sk-proj-your-api-key-here`

4. **もし設定されていない場合：**
   - 「New repository secret」をクリック
   - NameとValueを入力
   - 「Add secret」をクリック
   - 4つすべてを追加

### ステップ3: ワークフローを改善（エラーハンドリング追加）

ワークフローファイルにエラー詳細を表示するステップを追加します。

`.github/workflows/daily_post.yml`を以下のように修正：

```yaml
name: 毎日のブログ投稿

on:
  schedule:
    - cron: '0 0 * * *'
  workflow_dispatch:

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
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: 環境変数を確認
      run: |
        echo "WORDPRESS_URL is set: $([ -z "${{ secrets.WORDPRESS_URL }}" ] && echo 'NO' || echo 'YES')"
        echo "WORDPRESS_USERNAME is set: $([ -z "${{ secrets.WORDPRESS_USERNAME }}" ] && echo 'NO' || echo 'YES')"
        echo "WORDPRESS_PASSWORD is set: $([ -z "${{ secrets.WORDPRESS_PASSWORD }}" ] && echo 'NO' || echo 'YES')"
        echo "OPENAI_API_KEY is set: $([ -z "${{ secrets.OPENAI_API_KEY }}" ] && echo 'NO' || echo 'YES')"
    
    - name: ブログ記事を投稿
      run: python main.py
      env:
        WORDPRESS_URL: ${{ secrets.WORDPRESS_URL }}
        WORDPRESS_USERNAME: ${{ secrets.WORDPRESS_USERNAME }}
        WORDPRESS_PASSWORD: ${{ secrets.WORDPRESS_PASSWORD }}
        OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }
```

### ステップ4: 修正をコミット・プッシュ

1. ワークフローファイルを修正したら：

```bash
git add .github/workflows/daily_post.yml
git commit -m "ワークフローにエラー確認ステップを追加"
git push origin main
```

2. 再度ワークフローを実行

## 🆘 よくあるエラー

### エラー: "WORDPRESS_USERNAMEとWORDPRESS_PASSWORDを.envファイルに設定してください"

**原因：** GitHub Secretsが設定されていない

**解決方法：** ステップ2を参照して、GitHub Secretsを設定

### エラー: "ModuleNotFoundError"

**原因：** 依存パッケージがインストールされていない

**解決方法：** `requirements.txt`に必要なパッケージがすべて含まれているか確認

### エラー: "401 Unauthorized"（WordPress）

**原因：** WordPressの認証情報が間違っている

**解決方法：** GitHub Secretsの`WORDPRESS_USERNAME`と`WORDPRESS_PASSWORD`を確認

### エラー: "429"（OpenAI API）

**原因：** OpenAI APIキーのクォータ不足

**解決方法：** OpenAIアカウントのクレジット残高を確認

## 📝 デバッグのヒント

1. **ログを詳しく見る**
   - どのステップで失敗したか確認
   - エラーメッセージの全文を読む

2. **環境変数を確認**
   - 「環境変数を確認」ステップで、Secretsが正しく設定されているか確認

3. **ローカルでテスト**
   - 同じコードがローカルで動くか確認
   - `.env`ファイルが正しく設定されているか確認

## ✅ まとめ

1. ✅ GitHub Actionsのログを詳しく見る
2. ✅ GitHub Secretsが4つすべて設定されているか確認
3. ✅ ワークフローを改善してエラー詳細を表示
4. ✅ 修正をコミット・プッシュして再度実行

詳しいログを見れば、具体的な原因がわかります！






