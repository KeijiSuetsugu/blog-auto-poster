# Flux Pro（Replicate API）設定ガイド

## 概要

Flux Proは高品質なAI画像生成モデルで、Replicate API経由で利用できます。記事に関連した美しいサムネイル画像を自動生成します。

## 設定手順

### 1. Replicate APIトークンの取得

1. **Replicateアカウントを作成**
   - https://replicate.com/ にアクセス
   - 「Sign up」をクリックしてアカウントを作成

2. **APIトークンを取得**
   - ログイン後、https://replicate.com/account/api-tokens にアクセス
   - 「Create token」をクリック
   - トークンをコピー（`r8_`で始まる文字列）

3. **.envファイルに追加**
   ```env
   REPLICATE_API_TOKEN=r8_your-replicate-api-token-here
   IMAGE_SOURCE=flux
   ```

### 2. GitHub Secretsに追加（GitHub Actions使用時）

1. リポジトリの「Settings」→「Secrets and variables」→「Actions」
2. 「New repository secret」をクリック
3. 以下のシークレットを追加：
   - Name: `REPLICATE_API_TOKEN`
   - Value: `r8_your-replicate-api-token-here`
   - Name: `IMAGE_SOURCE`
   - Value: `flux`

## 料金

Flux Proの料金（2024年12月時点）:
- **1枚あたり約$0.055**（約8円）
- 月30記事の場合: 約$1.65（約240円）

### コスト比較

| 画像ソース | 1枚あたり | 月30記事 | 特徴 |
|-----------|----------|---------|------|
| **Flux Pro** | $0.055 | $1.65 | 最高品質、AI専用デザイン |
| Unsplash | 無料 | 無料 | 既存写真、AI関連画像は限定的 |
| DALL-E 3 | $0.04 | $1.20 | 高品質、やや遅い |

## 使用方法

### 自動投稿（通常使用）

設定後、通常通り実行するだけ：

```bash
python wordpress_poster.py
```

### 手動テスト

```bash
python article_generator.py
```

## Flux Proの特徴

### メリット
- **最高品質**: 16:9のプロフェッショナルな画像
- **AI専用**: AI技術に最適化されたデザイン
- **高速**: 通常10-30秒で生成完了
- **カスタマイズ**: 記事内容に完全に合わせた画像

### デメリット
- **有料**: 1枚あたり約8円
- **API必要**: Replicateアカウントが必要

## フォールバック機能

Flux Proが失敗した場合、自動的にUnsplashにフォールバックします：

```
Flux Pro → Unsplash → 画像なしで投稿
```

## トラブルシューティング

### エラー: "REPLICATE_API_TOKENが設定されていません"

**解決方法**:
1. `.env`ファイルに`REPLICATE_API_TOKEN`が設定されているか確認
2. トークンが`r8_`で始まっているか確認
3. 余分なスペースや改行がないか確認

### エラー: "Flux Pro画像生成失敗"

**解決方法**:
1. Replicateアカウントに十分なクレジットがあるか確認
2. APIトークンが有効か確認
3. 一時的にUnsplashに切り替える：
   ```env
   IMAGE_SOURCE=unsplash
   ```

### エラー: "Flux Pro画像生成タイムアウト"

**原因**: サーバーが混雑している可能性

**解決方法**:
- 自動的にUnsplashにフォールバックされるので問題ありません
- 再実行すると成功する可能性があります

## 環境変数の設定例

### Flux Proを使用（推奨）

```env
# OpenAI API設定
OPENAI_API_KEY=sk-your-openai-api-key-here

# WordPress設定
WORDPRESS_URL=https://your-wordpress-site.com
WORDPRESS_USERNAME=your-username
WORDPRESS_PASSWORD=your-application-password

# 画像生成設定（Flux Pro）
IMAGE_SOURCE=flux
REPLICATE_API_TOKEN=r8_your-replicate-api-token-here

# NewsAPI設定（オプション）
NEWSAPI_KEY=your-newsapi-key-here
```

### Unsplashを使用（無料）

```env
# OpenAI API設定
OPENAI_API_KEY=sk-your-openai-api-key-here

# WordPress設定
WORDPRESS_URL=https://your-wordpress-site.com
WORDPRESS_USERNAME=your-username
WORDPRESS_PASSWORD=your-application-password

# 画像生成設定（Unsplash）
IMAGE_SOURCE=unsplash
UNSPLASH_ACCESS_KEY=your-unsplash-access-key-here

# NewsAPI設定（オプション）
NEWSAPI_KEY=your-newsapi-key-here
```

## よくある質問

### Q: Flux ProとDALL-E 3、どちらが良いですか？

A: **Flux Proを推奨**します。理由：
- AI技術に特化したデザイン
- 16:9の最適なアスペクト比
- より現代的でプロフェッショナルな見た目

### Q: 無料で使いたい場合は？

A: **Unsplashを使用**してください：
```env
IMAGE_SOURCE=unsplash
UNSPLASH_ACCESS_KEY=your-key-here
```

### Q: 画像生成をスキップできますか？

A: はい、コードで`generate_image=False`を指定するか、環境変数を設定しなければスキップされます。

### Q: 複数の画像ソースを併用できますか？

A: はい、フォールバック機能により自動的に切り替わります：
```env
IMAGE_SOURCE=flux  # メイン
# Flux Pro失敗時 → 自動的にUnsplashにフォールバック
```

## まとめ

✅ Flux Proで最高品質のAI画像を生成  
✅ 月額約240円で毎日プロフェッショナルな画像  
✅ 自動フォールバック機能で安心  
✅ 簡単な設定で即座に利用可能  

Flux Proを使用することで、毎日の記事に最適化された美しい画像が自動的に生成されます！


