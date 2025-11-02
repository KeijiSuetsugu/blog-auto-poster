# ✅ GitHub Secrets設定の確認方法

## 現在のエラー

```
DEBUG: WORDPRESS_URL= (空)
DEBUG: WORDPRESS_USERNAME=存在しない
DEBUG: WORDPRESS_PASSWORD=存在しない
```

**原因：** GitHub Secretsが設定されていないか、正しく読み込まれていません。

## 📋 設定手順（画像付き説明）

### ステップ1: GitHubリポジトリのSettingsページを開く

1. ブラウザで以下を開く：
   ```
   https://github.com/KeijiSuetsugu/blog-auto-poster
   ```

2. 画面上部のタブから「**Settings**」をクリック

### ステップ2: Secretsページを開く

1. 左側のメニューから「**Secrets and variables**」をクリック
2. 「**Actions**」をクリック

### ステップ3: Secretsの確認

現在設定されているSecretsの一覧が表示されます。

**確認すべきSecrets（4つ）：**
- ✅ `WORDPRESS_URL`
- ✅ `WORDPRESS_USERNAME`
- ✅ `WORDPRESS_PASSWORD`
- ✅ `OPENAI_API_KEY`

### ステップ4: Secretsを追加（まだ設定されていない場合）

各Secretを追加します：

#### 1. WORDPRESS_URL

1. 「**New repository secret**」ボタンをクリック
2. 以下の値を入力：
   - **Name**: `WORDPRESS_URL`
   - **Secret**: `https://freeeeeeestyle.com`
3. 「**Add secret**」ボタンをクリック

#### 2. WORDPRESS_USERNAME

1. 再度「**New repository secret**」ボタンをクリック
2. 以下の値を入力：
   - **Name**: `WORDPRESS_USERNAME`
   - **Secret**: `onepeace0710`
3. 「**Add secret**」ボタンをクリック

#### 3. WORDPRESS_PASSWORD

1. 再度「**New repository secret**」ボタンをクリック
2. 以下の値を入力：
   - **Name**: `WORDPRESS_PASSWORD`
   - **Secret**: `sOf6 5CLI zoqo DCnS Xt66 bw2D`
3. 「**Add secret**」ボタンをクリック

#### 4. OPENAI_API_KEY

1. 再度「**New repository secret**」ボタンをクリック
2. 以下の値を入力：
   - **Name**: `OPENAI_API_KEY`
   - **Secret**: `.env`ファイルから`OPENAI_API_KEY`の値をコピーして貼り付け
3. 「**Add secret**」ボタンをクリック

### ステップ5: 確認

4つのSecretsがすべて表示されていることを確認してください。

## ⚠️ 重要なポイント

1. **Nameは正確に入力**
   - 大文字・小文字を正確に
   - 余分なスペースがないか確認
   - 例：`WORDPRESS_USERNAME`（`Wordpress_Username`や`WORDPRESS_USERNAME `ではない）

2. **Secretの値も正確に**
   - 全部コピーできているか（途中で切れていないか）
   - 余分なスペースがないか

3. **4つすべてが必要**
   - 1つでも欠けているとエラーになります

## ✅ 設定後の確認

Secretsを設定したら：

1. 「Actions」タブをクリック
2. 「毎日のブログ投稿」ワークフローを選択
3. 「Run workflow」ボタンをクリック
4. 実行ログで「環境変数を確認」ステップを確認
   - すべて「YES」になっているはずです

これで解決するはずです！

