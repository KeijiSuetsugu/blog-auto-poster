# 🔑 APIキーを更新した後の手順

## 現在の状況

`.env`ファイルの`OPENAI_API_KEY`を訂正した場合、**GitHub Secretsも同じ値に更新する必要があります**。

`.env`ファイルとGitHub Secretsは別々に管理されているため、両方を更新する必要があります。

## ✅ 次のステップ

### ステップ1: 正しいAPIキーを確認

`.env`ファイルの`OPENAI_API_KEY`の値を確認してください。

ターミナルで確認する場合：
```bash
cat .env | grep OPENAI_API_KEY
```

### ステップ2: GitHub SecretsのAPIキーを更新

1. **GitHubリポジトリページを開く：**
   ```
   https://github.com/KeijiSuetsugu/blog-auto-poster
   ```

2. **「Settings」タブをクリック**

3. **左メニューから「Secrets and variables」→「Actions」をクリック**

4. **既存の`OPENAI_API_KEY`を更新：**
   - `OPENAI_API_KEY`の行をクリック（または右側の鉛筆アイコンをクリック）
   - 「Update」または「Edit」をクリック
   - **Secret**の欄に、`.env`ファイルからコピーした正しいAPIキーを貼り付け
   - 「Update secret」ボタンをクリック

   **または、削除して再作成：**
   - `OPENAI_API_KEY`の右側の「削除」ボタンをクリック
   - 「New repository secret」をクリック
   - Name: `OPENAI_API_KEY`
   - Secret: `.env`ファイルの正しいAPIキーを貼り付け
   - 「Add secret」をクリック

### ステップ3: 他のSecretsも確認

念のため、他のSecretsも正しく設定されているか確認：

- ✅ `WORDPRESS_URL` = `https://freeeeeeestyle.com`
- ✅ `WORDPRESS_USERNAME` = `onepeace0710`
- ✅ `WORDPRESS_PASSWORD` = `sOf6 5CLI zoqo DCnS Xt66 bw2D`
- ✅ `OPENAI_API_KEY` = `.env`ファイルの正しい値

### ステップ4: 再度ワークフローを実行

1. **「Actions」タブをクリック**
2. **「毎日のブログ投稿」ワークフローを選択**
3. **「Run workflow」ボタンをクリック**
4. **実行ログを確認**

   「環境変数を確認」ステップで、すべて「YES」になっているか確認：
   - `OPENAI_API_KEY is set: YES`

### ステップ5: 成功を確認

成功すると、WordPressに記事が投稿されます！

## ⚠️ 重要なポイント

1. **`.env`ファイルとGitHub Secretsは別々**
   - ローカルの`.env`ファイルを更新しても、GitHub Secretsは自動では更新されません
   - 両方を手動で更新する必要があります

2. **APIキーの値は正確に**
   - 全部コピーできているか（途中で切れていないか）
   - 余分なスペースがないか

3. **4つすべてのSecretsが必要**
   - 1つでも欠けているとエラーになります

## 🎯 まとめ

1. ✅ `.env`ファイルを更新（完了）
2. ✅ GitHub Secretsの`OPENAI_API_KEY`も更新
3. ✅ ワークフローを再度実行
4. ✅ 成功を確認

これで解決するはずです！






