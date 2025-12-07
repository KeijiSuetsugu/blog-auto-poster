# 完全実装：AI記事自動生成システム

## 実装完了内容

### ✅ 実装した機能

1. **AI記事への完全変更**
   - テーマを「人間関係・心理学」から「AI技術」に変更
   - 最新AIニュースを自動取得して記事を生成
   - 3000〜4000字の詳細な記事を毎日自動生成

2. **Flux Pro画像生成**
   - Replicate API経由でFlux Proを使用
   - 記事内容に最適化された高品質画像を自動生成
   - 16:9のプロフェッショナルなアスペクト比

3. **重複投稿防止**
   - 過去30日間の投稿履歴を自動管理
   - タイトルの重複を自動検出
   - 最大3回まで自動リトライ

4. **デバッグ機能強化**
   - 画像生成設定の詳細表示
   - 各ステップでのログ出力
   - エラー時の詳細情報表示

## 必要な設定

### .envファイルの設定

```env
# OpenAI API設定（必須）
OPENAI_API_KEY=sk-your-openai-api-key-here

# WordPress設定（必須）
WORDPRESS_URL=https://your-wordpress-site.com
WORDPRESS_USERNAME=your-username
WORDPRESS_PASSWORD=your-application-password

# 画像生成設定（必須）
IMAGE_SOURCE=flux
REPLICATE_API_TOKEN=r8_your-replicate-api-token-here

# NewsAPI設定（オプション - より良い最新ニュース取得）
NEWSAPI_KEY=your-newsapi-key-here
```

### APIキーの取得方法

#### 1. Replicate APIトークン（Flux Pro用）

1. https://replicate.com/ でアカウント作成
2. https://replicate.com/account/api-tokens でトークン取得
3. `.env`に追加：
   ```env
   REPLICATE_API_TOKEN=r8_your-token-here
   IMAGE_SOURCE=flux
   ```

**料金**: 1枚あたり約$0.055（約8円）、月30記事で約240円

#### 2. NewsAPIキー（オプション）

1. https://newsapi.org/ で無料アカウント作成
2. APIキーを取得（1日100リクエストまで無料）
3. `.env`に追加：
   ```env
   NEWSAPI_KEY=your-newsapi-key-here
   ```

**注意**: NewsAPIキーがなくても、OpenAIフォールバックで最新情報を取得できます。

## 使用方法

### 通常の自動投稿

設定後、既存のコマンドで自動的に動作します：

```bash
python wordpress_poster.py
```

**動作内容**:
1. 最新のAIニュースを自動取得
2. 3000〜4000字の詳細な記事を生成
3. Flux Proで高品質画像を生成
4. WordPressに自動投稿
5. 投稿履歴を保存（重複防止）

### テスト実行

```bash
python article_generator.py
```

## 記事の特徴

### 内容
- **最新のAI技術やサービス**の情報
- **AIツールの比較や評価**
- **実用的な活用方法**や使用例
- **最新機能や新機能**の詳細解説
- **読者が試したくなる**具体的なアドバイス

### 文字数
- **3000〜4000字**の詳細な記事
- 読み応えのある充実した内容
- 自動的に文字数を調整

### 画像
- **Flux Pro**による高品質AI画像
- 記事内容に完全に最適化
- 16:9のプロフェッショナルな見た目
- 自動フォールバック（Flux Pro → Unsplash）

## 実行時のログ例

```
============================================================
🤖 AI記事生成モジュール起動
============================================================
DEBUG: APIキーの長さ: 164文字
DEBUG: APIキーのプレビュー: sk-proj-ab...xyz123
📝 画像ソース: flux
🔑 Unsplash APIキー: 未設定
🔑 Replicate APIキー: 設定済み
🔑 NewsAPI キー: 設定済み
============================================================

============================================================
📰 AI記事生成開始
============================================================
画像ソース: flux
画像生成: 有効
============================================================

NewsAPIから最新のAIニュースを取得中...
✓ NewsAPIから5件のニュースを取得しました

OpenAI APIにリクエストを送信中... (モデル: gpt-4o-mini)
生成された記事の文字数: 3245文字

============================================================
画像生成設定の確認
============================================================
画像生成: 有効
画像ソース: flux
============================================================

画像生成を開始します...
Flux Proで画像を生成中...
プロンプト: Professional tech blog header image about AI...
画像生成中... (最大60秒待機)
画像をダウンロード中: https://...
✓ Flux Proで画像を生成しました: /tmp/tmpXXXXXX.jpg
  画像URL: https://...
  画像パス: /tmp/tmpXXXXXX.jpg
✓ 投稿履歴に保存しました: ChatGPTとClaudeの最新比較

============================================================
✅ 生成された記事
============================================================
📝 タイトル: ChatGPTとClaudeの最新比較：2024年最新版
📊 本文の長さ: 3245文字
🖼️  画像パス: /tmp/tmpXXXXXX.jpg
🔗 画像URL: https://...
============================================================
```

## ファイル構成

### 変更ファイル
- `article_generator.py` - 完全にAI記事生成に変更
  - Flux Pro画像生成機能を追加
  - 最新ニュース取得機能を追加
  - 重複防止機能を追加
  - 3000〜4000字の記事生成

### 新規ファイル
- `post_history.json` - 投稿履歴（自動生成）
- `Flux_Pro設定ガイド.md` - Flux Proの詳細設定ガイド
- `完全実装_AI記事生成.md` - このファイル

## トラブルシューティング

### 人間関係の記事が生成される

**原因**: 古いコードがキャッシュされている可能性

**解決方法**:
1. Pythonプロセスを完全に再起動
2. 以下のコマンドで確認：
   ```bash
   python article_generator.py
   ```
3. ログに「AI記事生成モジュール起動」と表示されることを確認

### 画像が生成されない

**原因**: Replicate APIトークンが設定されていない

**解決方法**:
1. `.env`ファイルを確認：
   ```env
   IMAGE_SOURCE=flux
   REPLICATE_API_TOKEN=r8_your-token-here
   ```
2. トークンが`r8_`で始まっているか確認
3. ログで「Replicate APIキー: 設定済み」と表示されることを確認

### 画像生成が失敗する

**解決方法**:
- 自動的にUnsplashにフォールバックされます
- Replicateアカウントのクレジットを確認
- 一時的にUnsplashを使用：
  ```env
  IMAGE_SOURCE=unsplash
  UNSPLASH_ACCESS_KEY=your-key-here
  ```

## コスト

### 月30記事の場合

| 項目 | 料金 |
|------|------|
| OpenAI API (記事生成) | 約$0.30 |
| Flux Pro (画像生成) | 約$1.65 |
| **合計** | **約$1.95 (約280円)** |

### 無料オプション

画像生成を無料にしたい場合：
```env
IMAGE_SOURCE=unsplash
UNSPLASH_ACCESS_KEY=your-key-here
```

月額コスト: 約$0.30（約43円）

## GitHub Actions設定

GitHub Secretsに以下を追加：

```
OPENAI_API_KEY: sk-your-key-here
WORDPRESS_URL: https://your-site.com
WORDPRESS_USERNAME: your-username
WORDPRESS_PASSWORD: your-app-password
IMAGE_SOURCE: flux
REPLICATE_API_TOKEN: r8_your-token-here
NEWSAPI_KEY: your-newsapi-key (オプション)
```

## まとめ

✅ 毎日最新のAIニュースを自動取得  
✅ 3000〜4000字の詳細な記事を自動生成  
✅ Flux Proで高品質画像を自動生成  
✅ 重複投稿を自動防止  
✅ 完全自動化で手間なし  

これで、毎日最新のAI技術に関する詳細な記事が、美しい画像付きで自動投稿されます！

## 次のステップ

1. `.env`ファイルにReplicate APIトークンを追加
2. `python article_generator.py`でテスト実行
3. 問題なければ`python wordpress_poster.py`で投稿
4. GitHub Actionsで自動化（既存の設定で動作）

何か問題があれば、ログを確認して対処してください。


