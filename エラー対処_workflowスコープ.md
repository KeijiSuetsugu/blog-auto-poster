# 🔧 エラー対処：workflowスコープが必要

## エラーメッセージ

```
refusing to allow a Personal Access Token to create or update workflow 
`.github/workflows/daily_post.yml` without `workflow` scope
```

## 原因

GitHub Actionsのワークフローファイル（`.github/workflows/`内のファイル）をプッシュするには、Personal Access Tokenに**`workflow`スコープ**が必要です。

## 解決方法

### ステップ1: 新しいPersonal Access Tokenを作成

1. https://github.com/settings/tokens にアクセス
2. 「Generate new token」→「Generate new token (classic)」をクリック
3. **重要な設定：**
   - **Note**: 何でもOK（例：「ブログ投稿用（workflow権限付き）」）
   - **Expiration**: 好みで設定
   - **Select scopes（権限）**: 以下にチェックを入れる
     - ✅ **`repo`**（すべてのサブ項目にチェック）
     - ✅ **`workflow`** ← **これが重要！**
4. 「Generate token」をクリック
5. 表示されたトークンをコピー（一度しか表示されない！）

### ステップ2: ターミナルで再度プッシュ

1. ターミナルを開く
2. 以下のコマンドを実行：

```bash
git push origin main
```

3. ユーザー名を聞かれたら：GitHubのユーザー名を入力
4. パスワードを聞かれたら：**新しいトークン**を貼り付け

## 既存のトークンに権限を追加できない場合

Personal Access Tokenは作成時に権限を設定する必要があり、後から追加できません。

そのため、**新しいトークンを作成する必要があります**。

## トークンの権限まとめ

GitHub Actionsを使うには、以下の権限が必要です：

- ✅ **`repo`** - リポジトリへのアクセス
- ✅ **`workflow`** - ワークフローファイルの作成・更新

両方チェックして、新しいトークンを作成してください。

