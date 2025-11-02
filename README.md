# WordPress自動投稿システム

人間関係に関するブログ記事を毎日自動的にWordPressサイトに投稿するシステムです。

## 機能

- 毎日自動で2000字程度の人間関係に関するブログ記事を生成・投稿
- メンタル的に悩んでいる人や頑張っている人にも響く内容
- OpenAI APIを使用した高品質な記事生成
- スケジュール機能による自動実行

## セットアップ

### 1. 必要な環境

- Python 3.8以上
- WordPressサイト（REST APIが有効）
- OpenAI API キー

### 2. 依存パッケージのインストール

```bash
pip install -r requirements.txt
```

### 3. 環境変数の設定

`.env`ファイルを作成し、以下の情報を設定してください：

```env
# WordPress設定
WORDPRESS_URL=https://freeeeeeestyle.com
WORDPRESS_USERNAME=your_username
WORDPRESS_PASSWORD=your_application_password

# OpenAI API設定（記事生成用）
OPENAI_API_KEY=your_openai_api_key

# スケジューラー設定（投稿時刻）
POST_TIME=09:00
```

#### 📖 詳しい設定方法（小学生でもわかる説明）

**WordPressのアプリケーションパスワードとOpenAI APIキーの取得方法がよくわからない方は、以下のガイドを参照してください：**

👉 **[設定ガイド.md](設定ガイド.md)** を開いて、ステップバイステップで説明を確認してください！

#### WordPress認証情報の取得方法（簡単版）

1. WordPress管理画面にログイン（https://freeeeeeestyle.com/wp-admin/）
2. 「ユーザー」→「プロフィール」に移動
3. 「アプリケーションパスワード」セクションで新しいアプリケーションパスワードを作成
4. 作成されたパスワードを`WORDPRESS_PASSWORD`に設定

**注意**: 通常のログインパスワードではなく、アプリケーションパスワードを使用してください。

## 使い方

### 手動で1回だけ投稿する場合

```bash
python main.py
```

または

```bash
python wordpress_poster.py
```

### スケジューラーとして実行（毎日自動投稿）

⚠️ **注意**: この方法は**パソコンが起動している時のみ**動作します。

```bash
python main.py --scheduler
```

または

```bash
python scheduler.py
```

スケジューラーは指定した時刻（デフォルト: 09:00）に毎日自動で記事を投稿します。
停止するには `Ctrl+C` を押してください。

### ☁️ パソコンがオフでも自動投稿する方法（GitHub Actions）

**パソコンをシャットダウンしていても毎日自動投稿したい場合は、GitHub Actionsを使用してください。**

👉 詳しいセットアップ手順は **[github_actions_setup.md](github_actions_setup.md)** を参照してください。

**メリット：**
- ✅ パソコンがオフでも動作
- ✅ 無料で利用可能
- ✅ クラウドで実行されるため信頼性が高い
- ✅ 実行ログがGitHubで確認できる

### cronジョブとして設定する場合（Linux/Mac）

毎日特定の時刻に実行したい場合は、cronジョブを使用することもできます：

```bash
crontab -e
```

以下の行を追加（例：毎日09:00に実行）：

```
0 9 * * * cd /path/to/project && /usr/bin/python3 main.py
```

## ファイル構成

- `main.py`: メイン実行ファイル
- `wordpress_poster.py`: WordPressへの投稿処理
- `article_generator.py`: AIを使用した記事生成モジュール
- `scheduler.py`: スケジュール実行モジュール
- `requirements.txt`: Python依存パッケージ
- `.env`: 環境変数（gitignoreに含まれています）

## 記事生成について

- OpenAI GPT-4o-miniを使用して記事を生成
- 人間関係に関する15のテーマからランダムに選択
- 約2000字程度の記事を生成
- HTML形式で出力（段落は`<p>`タグで囲まれます）

## トラブルシューティング

### 投稿エラーが発生する場合

1. WordPressのREST APIが有効になっているか確認
2. アプリケーションパスワードが正しく設定されているか確認
3. WordPressサイトのURLが正しいか確認
4. エラーメッセージを確認して問題を特定

### 記事が生成されない場合

1. OpenAI API キーが正しく設定されているか確認
2. API キーの残高があるか確認
3. ネットワーク接続を確認

## ライセンス

このプロジェクトは個人利用・商用利用ともに自由にご利用いただけます。

