# Banana Pro (Nano) 設定ガイド

## 概要

Banana Pro Nanoは高速・低コストなAI画像生成モデルで、Flux Nanoを使用して美しいサムネイル画像を自動生成します。

## 特徴

### Nanoモデルの利点
- **超高速**: 通常2-5秒で生成完了
- **低コスト**: Flux Proの約1/5のコスト
- **高品質**: 十分なクオリティのプロフェッショナル画像
- **効率的**: 4ステップの推論で高速生成

## 設定手順

### 1. Banana Pro APIキーの取得

1. **Banana Devアカウントを作成**
   - https://www.banana.dev/ にアクセス
   - 「Sign up」をクリックしてアカウントを作成

2. **APIキーを取得**
   - ログイン後、ダッシュボードでAPIキーを取得
   - APIキーをコピー

3. **.envファイルに追加**
   ```env
   BANANA_API_KEY=your-banana-api-key-here
   IMAGE_SOURCE=banana
   ```

### 2. GitHub Secretsに追加（GitHub Actions使用時）

1. リポジトリの「Settings」→「Secrets and variables」→「Actions」
2. 「New repository secret」をクリック
3. 以下のシークレットを追加：
   - Name: `BANANA_API_KEY`
   - Value: `your-banana-api-key-here`
   - Name: `IMAGE_SOURCE`
   - Value: `banana`

## 料金

Banana Pro Nanoの料金（2024年12月時点）:
- **1枚あたり約$0.01**（約1.5円）
- 月30記事の場合: 約$0.30（約45円）

### コスト比較

| 画像ソース | 1枚あたり | 月30記事 | 生成速度 | 特徴 |
|-----------|----------|---------|---------|------|
| **Banana Pro Nano** | $0.01 | $0.30 | 2-5秒 | 超高速・低コスト |
| Flux Pro | $0.055 | $1.65 | 10-30秒 | 最高品質 |
| Unsplash | 無料 | 無料 | 即座 | 既存写真 |
| DALL-E 3 | $0.04 | $1.20 | 10-20秒 | 高品質 |

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

## Banana Pro Nanoの特徴

### メリット
- **超高速**: 2-5秒で生成完了（Flux Proの1/5の時間）
- **超低コスト**: 1枚約1.5円（Flux Proの1/5のコスト）
- **高品質**: ブログ記事に十分なクオリティ
- **16:9対応**: プロフェッショナルなアスペクト比
- **AI専用**: AI技術に最適化されたデザイン

### デメリット
- **品質**: Flux Proより若干劣る（ただしブログには十分）
- **API必要**: Banana Devアカウントが必要

## フォールバック機能

Banana Pro Nanoが失敗した場合、自動的にUnsplashにフォールバックします：

```
Banana Pro Nano → Unsplash → 画像なしで投稿
```

## トラブルシューティング

### エラー: "BANANA_API_KEYが設定されていません"

**解決方法**:
1. `.env`ファイルに`BANANA_API_KEY`が設定されているか確認
2. 余分なスペースや改行がないか確認

### エラー: "Banana Pro (Nano)画像生成失敗"

**解決方法**:
1. Banana Devアカウントに十分なクレジットがあるか確認
2. APIキーが有効か確認
3. 一時的にUnsplashに切り替える：
   ```env
   IMAGE_SOURCE=unsplash
   ```

### エラー: "Banana Pro (Nano)画像生成タイムアウト"

**原因**: サーバーが混雑している可能性

**解決方法**:
- 自動的にUnsplashにフォールバックされるので問題ありません
- 再実行すると成功する可能性があります

## 環境変数の設定例

### Banana Pro Nanoを使用（推奨）

```env
# OpenAI API設定
OPENAI_API_KEY=sk-your-openai-api-key-here

# WordPress設定
WORDPRESS_URL=https://your-wordpress-site.com
WORDPRESS_USERNAME=your-username
WORDPRESS_PASSWORD=your-application-password

# 画像生成設定（Banana Pro Nano）
IMAGE_SOURCE=banana
BANANA_API_KEY=your-banana-api-key-here

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

### Q: Banana Pro NanoとFlux Pro、どちらが良いですか？

A: **コストパフォーマンスを重視するならBanana Pro Nano**を推奨します。理由：
- 超高速（2-5秒）
- 超低コスト（1枚約1.5円）
- ブログ記事には十分な品質

最高品質が必要な場合のみFlux Proを選択してください。

### Q: 無料で使いたい場合は？

A: **Unsplashを使用**してください：
```env
IMAGE_SOURCE=unsplash
UNSPLASH_ACCESS_KEY=your-key-here
```

### Q: 画像生成をスキップできますか？

A: はい、コードで`generate_image=False`を指定するか、環境変数を設定しなければスキップされます。

### Q: 生成される画像のサイズは？

A: 1024x576ピクセル（16:9アスペクト比）で生成されます。

## 技術仕様

### Nanoモデルの設定

```python
{
    "modelKey": "flux-nano",
    "width": 1024,
    "height": 576,  # 16:9アスペクト比
    "num_inference_steps": 4,  # 高速生成
    "guidance_scale": 3.5
}
```

### 生成プロセス

1. **リクエスト送信**: Banana Pro APIにプロンプトを送信
2. **callID取得**: 非同期処理のIDを取得
3. **ステータス確認**: 1秒ごとにステータスをチェック（最大30秒）
4. **画像取得**: Base64またはURLで画像を取得
5. **保存**: 一時ファイルに保存

## まとめ

✅ Banana Pro Nanoで超高速・低コスト画像生成  
✅ 月額約45円で毎日プロフェッショナルな画像  
✅ 2-5秒の超高速生成  
✅ 自動フォールバック機能で安心  
✅ 簡単な設定で即座に利用可能  

Banana Pro Nanoを使用することで、コストを抑えながら毎日の記事に最適化された美しい画像が自動的に生成されます！

## 月間コスト比較（30記事）

| 項目 | Banana Pro Nano | Flux Pro |
|------|----------------|----------|
| 画像生成 | 約45円 | 約240円 |
| 記事生成 (OpenAI) | 約43円 | 約43円 |
| **合計** | **約88円** | **約283円** |

**Banana Pro Nanoなら月額100円以下で運用可能！**


