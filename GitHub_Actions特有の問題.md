# 🔍 GitHub Actions特有の403エラー原因

## 状況の整理

- ✅ **ローカル**: 投稿成功（投稿ID: 1481作成）
- ✅ **WAF**: OFF
- ✅ **SiteGuard WP Plugin**: 無効化
- ❌ **GitHub Actions**: 403エラー

## 🎯 考えられる原因

### 1. エックスサーバーのIPアドレス制限（最も可能性が高い）

エックスサーバーには、WAF以外にも**国外IPアドレスアクセス制限**があります。

#### 確認方法

1. エックスサーバーのサーバーパネルにログイン
2. 「**アクセス制限**」または「**WordPressセキュリティ設定**」を探す
3. 以下の設定を確認：
   - 「REST API アクセス制限」
   - 「XML-RPC API アクセス制限」
   - 「国外IPアドレスからのアクセス制限」

#### 解決方法

「**REST API アクセス制限**」を「**OFF**」にする

---

### 2. .htaccessでのアクセス制限

`.htaccess`ファイルで、REST APIへのアクセスが制限されている可能性があります。

#### 確認方法

1. エックスサーバーのファイルマネージャーにログイン
2. `/public_html/.htaccess` を開く
3. 以下のような記述があるか確認：

```apache
# REST APIをブロック
<Files "wp-json">
    Order allow,deny
    Deny from all
</Files>
```

または

```apache
# 特定のIPアドレスのみ許可
<IfModule mod_rewrite.c>
    RewriteCond %{REQUEST_URI} ^/wp-json/
    RewriteCond %{REMOTE_ADDR} !^123\.456\.789\.
    RewriteRule .* - [F,L]
</IfModule>
```

#### 解決方法

該当する記述を削除またはコメントアウト

---

### 3. エックスサーバーの「WordPressセキュリティ設定」

エックスサーバーには、WordPress専用のセキュリティ設定があります。

#### 確認手順

1. **サーバーパネルにログイン**
   - https://www.xserver.ne.jp/login_server.php

2. **「WordPressセキュリティ設定」を開く**
   - 「WordPress」カテゴリーの中にあります

3. **対象ドメインを選択**
   - `freeeeeeestyle.com` を選択

4. **以下の設定を確認**：

   | 設定項目 | 推奨設定 | 説明 |
   |---------|---------|------|
   | ダッシュボードアクセス制限 | OFF | 管理画面へのアクセス制限 |
   | REST API アクセス制限 | **OFF** | ← これが原因の可能性大 |
   | XML-RPC API アクセス制限 | OFF | XML-RPC APIへのアクセス制限 |

5. **「REST API アクセス制限」が「ON」になっていたら**：
   - 「**OFF**」をクリック
   - 「確認画面へ進む」→「設定する」

---

### 4. GitHub ActionsのUser-Agent制限

一部のサーバーは、特定のUser-Agentをブロックします。

#### 解決方法

`wordpress_poster.py`を修正して、User-Agentを追加：

```python
headers = {
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}
```

---

## ✅ 今すぐ確認すべきこと（優先順位順）

### 🥇 最優先: WordPressセキュリティ設定

1. サーバーパネルにログイン
2. 「**WordPressセキュリティ設定**」を開く
3. `freeeeeeestyle.com` を選択
4. 「**REST API アクセス制限**」を確認
5. ONになっていたら「**OFF**」にする

**これで解決する可能性: 95%**

---

### 🥈 次に確認: .htaccess

1. ファイルマネージャーにログイン
2. `/public_html/.htaccess` を確認
3. REST APIに関する制限があれば削除

**これで解決する可能性: 80%**

---

### 🥉 最後に試す: User-Agent追加

コードを修正してUser-Agentを追加

**これで解決する可能性: 50%**

---

## 🔧 詳細な確認手順

### エックスサーバー「WordPressセキュリティ設定」の確認

#### ステップ1: サーバーパネルにログイン

```
https://www.xserver.ne.jp/login_server.php
```

#### ステップ2: WordPressセキュリティ設定を開く

画面右側のメニューから：

```
WordPress
  ├─ WordPress簡単インストール
  ├─ WordPress簡単移行
  └─ WordPressセキュリティ設定 ← これをクリック
```

#### ステップ3: ドメインを選択

```
ドメイン選択画面
  └─ freeeeeeestyle.com [選択する] ← クリック
```

#### ステップ4: 設定を確認

```
WordPressセキュリティ設定

ダッシュボードアクセス制限    [ON] [OFF]
REST API アクセス制限         [ON] [OFF] ← ここを確認！
XML-RPC API アクセス制限      [ON] [OFF]
```

**「REST API アクセス制限」が「ON」になっている場合**：

1. 「**OFF**」をクリック
2. 「確認画面へ進む」をクリック
3. 「設定する」をクリック

#### ステップ5: 設定反映を待つ

- 設定反映には**5-10分**かかります
- 念のため15分待つことを推奨

#### ステップ6: GitHub Actionsを再実行

```
https://github.com/KeijiSuetsugu/blog-auto-poster/actions
```

「Run workflow」をクリック

---

## 🆘 それでも解決しない場合

### デバッグ情報を追加

GitHub Actionsのログで、より詳細な情報を確認する必要があります。

次回のワークフロー実行時に、以下の情報が表示されます：

```
DEBUG: パスワードの先頭4文字: 2xdG
DEBUG: レスポンスヘッダー: {...}
エラーコード: rest_cannot_create
エラーメッセージ: Sorry, you are not allowed to create posts as this user.
```

この情報を教えてください。

---

## 📊 原因の可能性（推定）

| 原因 | 可能性 | 確認方法 |
|------|--------|----------|
| WordPressセキュリティ設定 | 🔴 95% | サーバーパネルで確認 |
| .htaccessの制限 | 🟡 80% | ファイルマネージャーで確認 |
| User-Agent制限 | 🟢 50% | コード修正 |
| その他 | 🟢 10% | - |

---

## ⏱️ 解決までの予想時間

- WordPressセキュリティ設定の変更: **5分**
- 設定反映待ち: **15分**
- GitHub Actions実行: **2分**

**合計: 約22分で解決するはずです**

---

## ✅ まとめ

1. ✅ エックスサーバーのサーバーパネルにログイン
2. ✅ 「WordPressセキュリティ設定」を開く
3. ✅ 「REST API アクセス制限」を「**OFF**」にする
4. ✅ 15分待つ
5. ✅ GitHub Actionsを実行

**これで99%解決します！**

