# 🔍 ローカル成功・GitHub Actions失敗の原因

## 状況の整理

- ✅ **ローカル**: 投稿成功
- ✅ **環境変数**: 正しく設定されている（パスワード29文字）
- ❌ **GitHub Actions**: 403 Forbidden エラー

## なぜローカルでは成功するのに、GitHub Actionsでは失敗するのか？

### 答え：**アクセス元のIPアドレスが違うから**

```
ローカルPC → あなたの自宅/会社のIPアドレス → WordPress ✅
GitHub Actions → GitHubのサーバーのIPアドレス → WordPress ❌
```

## 🎯 最も可能性が高い原因

### 1. WordPressのセキュリティプラグインがGitHubをブロック

多くのセキュリティプラグインは、**知らないIPアドレスからのREST APIアクセスをブロック**します。

#### よくあるプラグイン

- **Wordfence Security** ← 最も可能性が高い
- **iThemes Security**
- **All In One WP Security & Firewall**
- **Sucuri Security**
- **Jetpack** のセキュリティ機能

#### これらのプラグインは以下をブロックします：

- 海外からのアクセス
- 新しいIPアドレスからのアクセス
- 短時間に複数回のアクセス
- REST APIへのアクセス

### 2. レンタルサーバーのWAF（Web Application Firewall）

多くのレンタルサーバーには、WAFが標準で有効になっています。

#### 主要レンタルサーバーのWAF

- **エックスサーバー**: WAF設定あり
- **ロリポップ**: WAF設定あり
- **さくらインターネット**: WAF設定あり
- **ConoHa WING**: WAF設定あり

WAFは、REST APIへのPOSTリクエストを「攻撃」と判断してブロックすることがあります。

### 3. .htaccessでのIP制限

`.htaccess`ファイルで特定のIPアドレスのみ許可している場合、GitHub Actionsからのアクセスはブロックされます。

## ✅ 解決方法（優先順位順）

### 方法1: セキュリティプラグインのREST API制限を解除（最優先）

#### Wordfence Securityの場合

1. WordPress管理画面にログイン
2. **Wordfence** → **All Options**
3. **Firewall Options** セクションを探す
4. 以下の設定を確認：
   - 「Rate Limiting」を確認
   - 「Immediately block fake Google crawlers」のような設定を確認
5. **REST API**に関する設定を探して、**認証済みユーザーのアクセスを許可**

#### iThemes Securityの場合

1. WordPress管理画面にログイン
2. **Security** → **Settings**
3. **REST API** タブを開く
4. 「Restrict Access to REST API」を**無効**にする
   - または、「Allow access for authenticated users」を有効にする

#### All In One WP Securityの場合

1. WordPress管理画面にログイン
2. **WP Security** → **Firewall**
3. **Basic Firewall Rules** タブ
4. REST APIに関する制限を解除

### 方法2: レンタルサーバーのWAFを一時的に無効化

#### エックスサーバーの場合

1. サーバーパネルにログイン
2. **WAF設定** をクリック
3. 対象ドメインの「OFF」を選択
4. 設定反映まで数分待つ

#### ロリポップの場合

1. ユーザー専用ページにログイン
2. **セキュリティ** → **WAF設定**
3. 対象ドメインを「無効」にする

#### ConoHa WINGの場合

1. コントロールパネルにログイン
2. **サイト管理** → **サイトセキュリティ**
3. **WAF** を「OFF」にする

### 方法3: 特定のパスをWAFから除外

WAFを完全に無効にしたくない場合、REST APIのパスだけ除外できます。

#### .htaccessに追加（サーバーによって異なる）

```apache
# REST APIへのアクセスをWAFから除外
<IfModule mod_siteguard.c>
    SiteGuard_User_ExcludeSig wp-json
</IfModule>
```

### 方法4: WordPressプラグインでREST APIを保護しつつ許可

**Application Passwords**プラグインを使用している場合、設定を確認します。

1. WordPress管理画面
2. **設定** → **Application Passwords**
3. REST APIへのアクセスが許可されているか確認

## 🔧 すぐに試せる確認方法

### ステップ1: セキュリティプラグインを一時的に無効化

1. WordPress管理画面にログイン
2. **プラグイン** → **インストール済みプラグイン**
3. セキュリティ関連のプラグインを**一時的に無効化**
4. GitHub Actionsを再実行
5. 成功したら、そのプラグインが原因

### ステップ2: WAFを一時的に無効化

1. レンタルサーバーの管理画面にログイン
2. WAF設定を「OFF」にする
3. 5-10分待つ（設定反映に時間がかかる）
4. GitHub Actionsを再実行
5. 成功したら、WAFが原因

### ステップ3: パーマリンク設定を更新

1. WordPress管理画面 → **設定** → **パーマリンク設定**
2. 何も変更せず「**変更を保存**」をクリック
3. REST APIが再初期化される

## 📊 原因の可能性（推定）

| 原因 | 可能性 | 確認方法 |
|------|--------|----------|
| セキュリティプラグイン | 🔴 80% | プラグインを一時的に無効化 |
| レンタルサーバーのWAF | 🟡 15% | WAFを一時的に無効化 |
| .htaccessのIP制限 | 🟢 3% | .htaccessを確認 |
| その他 | 🟢 2% | - |

## 🎯 推奨される対処順序

1. **まず**: セキュリティプラグインを一時的に無効化してテスト
2. **次に**: WAFを一時的に無効化してテスト
3. **最後**: .htaccessを確認

## ⚠️ 重要な注意事項

### セキュリティプラグインやWAFを無効化する場合

- ✅ テスト時のみ一時的に無効化
- ✅ 問題が解決したら、設定を調整して再度有効化
- ❌ 長期間無効のままにしない

### 安全な設定方法

セキュリティプラグインやWAFで、以下のように設定するのが理想的：

```
REST APIへのアクセス:
- 認証なし → ブロック ❌
- 認証あり（アプリケーションパスワード） → 許可 ✅
```

## 🆘 それでも解決しない場合

### デバッグ情報を確認

次回のGitHub Actions実行時に、以下の情報が表示されます：

```
DEBUG: パスワードの先頭4文字: 2xdG
DEBUG: レスポンスヘッダー: {...}
エラーコード: rest_cannot_create
エラーメッセージ: Sorry, you are not allowed to create posts as this user.
```

この情報を元に、より詳しく原因を特定できます。

## ✅ まとめ

**ローカルで成功してGitHub Actionsで失敗する = IPアドレスの違いが原因**

最も可能性が高いのは：
1. **セキュリティプラグイン**がGitHubのIPをブロック
2. **レンタルサーバーのWAF**がREST APIをブロック

まずは、セキュリティプラグインを一時的に無効化してテストしてみてください！

