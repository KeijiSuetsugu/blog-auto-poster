# 🔧 GitHub Secrets 再設定手順（403エラー解決）

## 問題

ローカルでは成功するのに、GitHub Actionsでは403エラーが出る場合、**GitHub Secretsの設定が間違っている**可能性が高いです。

## ✅ 解決手順

### ステップ1: 正しいパスワードを確認

あなたのWordPressアプリケーションパスワードは：

```
2xdG 6oQl l5ZT wLJF o0Ut jgCz
```

**重要**: スペースも含めて、このまま設定してください。

### ステップ2: GitHub Secretsを削除して再作成

#### 1. GitHubリポジトリページを開く

```
https://github.com/KeijiSuetsugu/blog-auto-poster
```

#### 2. Settings → Secrets and variables → Actions を開く

#### 3. 既存のSecretsを削除

- `WORDPRESS_PASSWORD` の右側の「Delete」をクリック
- 削除を確認

#### 4. 新しいSecretを作成

1. 「New repository secret」をクリック
2. **Name**: `WORDPRESS_PASSWORD`
3. **Secret**: 以下をコピー&ペースト

```
2xdG 6oQl l5ZT wLJF o0Ut jgCz
```

**注意事項**:
- ✅ スペースも含めてコピーする
- ✅ 前後に余分なスペースや改行を入れない
- ✅ 引用符（`"`や`'`）は入れない

4. 「Add secret」をクリック

#### 5. 他のSecretsも確認

- `WORDPRESS_URL`: `https://freeeeeeestyle.com`
- `WORDPRESS_USERNAME`: `onepeace0710`
- `OPENAI_API_KEY`: あなたのOpenAI APIキー

### ステップ3: ワークフローを再実行

1. 「Actions」タブをクリック
2. 「毎日のブログ投稿」ワークフローを選択
3. 「Run workflow」ボタンをクリック
4. 実行ログを確認

### ステップ4: ログで確認

GitHub Actionsのログで以下を確認：

```
DEBUG: ユーザー名: onepeace0710
DEBUG: パスワードの長さ: 29文字
```

パスワードの長さが**29文字**になっていれば正しく設定されています。

## 🔍 よくある間違い

### ❌ 間違い1: スペースを削除してしまう

```
2xdG6oQll5ZTwLJFo0UtjgCz  ← 間違い
```

### ❌ 間違い2: 引用符を付けてしまう

```
"2xdG 6oQl l5ZT wLJF o0Ut jgCz"  ← 間違い
```

### ❌ 間違い3: 前後に余分なスペースが入る

```
 2xdG 6oQl l5ZT wLJF o0Ut jgCz   ← 間違い
```

### ✅ 正しい設定

```
2xdG 6oQl l5ZT wLJF o0Ut jgCz
```

## 📝 確認方法

### ローカルでテスト

```bash
python3 test_wordpress_auth.py
```

以下が表示されればOK：
```
✅ 認証成功！投稿を取得できました
✅ ユーザー情報取得成功
✅ 下書き投稿成功！
```

### GitHub Actionsでテスト

1. ワークフローを実行
2. ログで「DEBUG: パスワードの長さ: 29文字」を確認
3. 「✅ 記事の投稿に成功しました」を確認

## 🆘 まだエラーが出る場合

### 新しいアプリケーションパスワードを作成

1. WordPress管理画面にログイン
   - https://freeeeeeestyle.com/wp-admin/
2. 「ユーザー」→「プロフィール」
3. 「アプリケーションパスワード」セクション
4. 名前を入力（例：「GitHub Actions用2」）
5. 「新しいアプリケーションパスワードを追加」をクリック
6. **表示されたパスワードを全てコピー**
7. GitHub Secretsの`WORDPRESS_PASSWORD`を更新

## ✅ まとめ

1. ✅ GitHub Secretsの`WORDPRESS_PASSWORD`を削除
2. ✅ `2xdG 6oQl l5ZT wLJF o0Ut jgCz`を新しいSecretとして追加
3. ✅ ワークフローを再実行
4. ✅ ログでパスワードの長さが29文字か確認

これで解決するはずです！

