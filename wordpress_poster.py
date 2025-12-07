"""
WordPress自動投稿スクリプト
AI関連の最新ニュースを毎日自動投稿します
アイキャッチ画像のアップロード機能を含みます
"""

import os
import requests
from datetime import datetime
from dotenv import load_dotenv
from article_generator import generate_article
from pathlib import Path

# 環境変数を読み込み
load_dotenv()

class WordPressPoster:
    def __init__(self):
        # 環境変数を読み込み（.envファイルがあれば読み込むが、なくてもOK）
        load_dotenv()
        
        print(f"\n{'='*60}")
        print("🔧 WordPress設定を読み込み中...")
        print(f"{'='*60}")
        
        self.base_url = os.getenv('WORDPRESS_URL', '').strip()
        # 環境変数が空、または不正な場合にデフォルト値を設定
        if not self.base_url or not self.base_url.startswith(('http://', 'https://')):
            self.base_url = 'https://freeeeeeestyle.com'
            print(f"⚠️ WORDPRESS_URLが未設定のため、デフォルト値を使用: {self.base_url}")
        
        # URLの末尾にスラッシュがある場合は削除
        self.base_url = self.base_url.rstrip('/')

        self.username = os.getenv('WORDPRESS_USERNAME')
        self.password = os.getenv('WORDPRESS_PASSWORD')
        
        # 設定状況を表示
        print(f"🌐 WordPress URL: {self.base_url}")
        print(f"👤 ユーザー名: {'✓ 設定済み' if self.username else '✗ 未設定'}")
        print(f"🔑 パスワード: {'✓ 設定済み' if self.password else '✗ 未設定'}")
        
        if not self.username or not self.password:
            raise ValueError(
                f"WORDPRESS_USERNAMEとWORDPRESS_PASSWORDを設定してください。\n"
                f"現在の状態: USERNAME={'設定済み' if self.username else '未設定'}, "
                f"PASSWORD={'設定済み' if self.password else '未設定'}\n"
                f"GitHub Actionsを使用している場合、GitHub Secretsを設定してください。"
            )
        
        # WordPress REST APIのエンドポイント
        if not self.base_url.startswith(('http://', 'https://')):
            raise ValueError(f"無効なWORDPRESS_URL: {self.base_url}")
        self.api_url = f"{self.base_url}/wp-json/wp/v2/posts"
        self.media_api_url = f"{self.base_url}/wp-json/wp/v2/media"
        print(f"📡 API URL: {self.api_url}")
        print(f"{'='*60}\n")
    
    def upload_media(self, image_path: str, title: str = ""):
        """
        WordPressにメディア（画像）をアップロード
        
        Args:
            image_path: アップロードする画像ファイルのパス
            title: 画像のタイトル（省略可）
        
        Returns:
            アップロードされたメディアのID、失敗時はNone
        """
        try:
            # ファイルが存在するか確認
            if not os.path.exists(image_path):
                print(f"⚠️ 画像ファイルが見つかりません: {image_path}")
                return None
            
            # ファイル名とMIMEタイプを取得
            file_name = Path(image_path).name
            mime_type = 'image/jpeg' if image_path.endswith('.jpg') or image_path.endswith('.jpeg') else 'image/png'
            
            print(f"画像をアップロード中: {file_name}")
            
            # ファイルを読み込み
            with open(image_path, 'rb') as img_file:
                files = {
                    'file': (file_name, img_file, mime_type)
                }
                
                headers = {
                    'Content-Disposition': f'attachment; filename="{file_name}"'
                }
                
                # タイトルを設定
                data = {}
                if title:
                    data['title'] = title
                
                response = requests.post(
                    self.media_api_url,
                    files=files,
                    headers=headers,
                    data=data,
                    auth=(self.username, self.password),
                    timeout=60
                )
                
                print(f"DEBUG: メディアアップロードレスポンスステータス: {response.status_code}")
                
                if response.status_code == 201:
                    media_data = response.json()
                    media_id = media_data.get('id')
                    print(f"✓ 画像をアップロードしました (ID: {media_id})")
                    return media_id
                else:
                    print(f"⚠️ 画像アップロード失敗: {response.status_code}")
                    print(f"レスポンス: {response.text}")
                    return None
                    
        except Exception as e:
            print(f"⚠️ 画像アップロードエラー: {e}")
            return None
        
    def create_post(self, title, content, status='publish', featured_media_id=None):
        """
        WordPressに記事を投稿
        
        Args:
            title: 記事のタイトル
            content: 記事の本文（HTML形式）
            status: 公開ステータス（'publish', 'draft', 'pending'など）
            featured_media_id: アイキャッチ画像のメディアID（省略可）
        
        Returns:
            投稿のレスポンス
        """
        headers = {
            'Content-Type': 'application/json',
        }
        
        data = {
            'title': title,
            'content': content,
            'status': status,
            'categories': [],  # 必要に応じてカテゴリーIDを指定
        }
        
        # アイキャッチ画像を設定
        if featured_media_id:
            data['featured_media'] = featured_media_id
            print(f"アイキャッチ画像を設定: ID {featured_media_id}")
        
        try:
            print(f"DEBUG: 投稿URL: {self.api_url}")
            print(f"DEBUG: ユーザー名: {self.username}")
            print(f"DEBUG: パスワードの長さ: {len(self.password) if self.password else 0}文字")
            print(f"DEBUG: パスワードの先頭4文字: {self.password[:4] if self.password else 'なし'}")
            
            response = requests.post(
                self.api_url,
                json=data,
                headers=headers,
                auth=(self.username, self.password),
                timeout=30
            )
            
            print(f"DEBUG: レスポンスステータス: {response.status_code}")
            print(f"DEBUG: レスポンスヘッダー: {dict(response.headers)}")
            
            if response.status_code == 403:
                print("\n" + "="*60)
                print("⚠️  403 Forbidden エラー")
                print("="*60)
                print("WordPressの認証が拒否されました。")
                print("\n考えられる原因:")
                print("1. GitHub ActionsのIPアドレスがブロックされている")
                print("2. WordPressのセキュリティプラグインがREST APIをブロック")
                print("3. アプリケーションパスワードの権限不足")
                print("4. WordPressのユーザー権限が不足している")
                print("\n対処方法:")
                print("1. WordPressのセキュリティ設定を確認")
                print("2. REST APIへのアクセス制限を確認")
                print("3. アプリケーションパスワードを再作成")
                print("="*60 + "\n")
                
                # エラー詳細を表示
                try:
                    error_json = response.json()
                    print(f"エラーコード: {error_json.get('code', 'なし')}")
                    print(f"エラーメッセージ: {error_json.get('message', 'なし')}")
                    if 'data' in error_json:
                        print(f"エラーデータ: {error_json['data']}")
                except:
                    print(f"レスポンス内容（テキスト）: {response.text}")
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.HTTPError as e:
            print(f"HTTPエラー: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"ステータスコード: {e.response.status_code}")
                print(f"レスポンス内容: {e.response.text}")
            raise
        except requests.exceptions.RequestException as e:
            print(f"投稿エラー: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"レスポンス内容: {e.response.text}")
            raise
    
    def post_daily_article(self):
        """
        毎日の記事を生成して投稿（画像付き）
        4000〜5000字の実用的でユニークなAI記事をBanana Pro Nano画像付きで投稿
        """
        print(f"\n{'='*60}")
        print(f"🚀 AI記事自動投稿開始")
        print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}\n")
        
        try:
            # 画像ソースを環境変数から取得（デフォルトはunsplash - 無料）
            image_source = os.getenv('IMAGE_SOURCE', 'unsplash')
            print(f"📝 画像ソース: {image_source}")
            
            # 記事を生成（画像も生成）
            print("\n📰 記事生成を開始します...")
            article_data = generate_article(image_source=image_source, generate_image=True)
            
            print(f"タイトル: {article_data['title']}")
            print(f"本文の長さ: {len(article_data['content'])}文字")
            
            # 画像をアップロード
            featured_media_id = None
            if 'image_path' in article_data and article_data['image_path']:
                print("\n画像をWordPressにアップロードします...")
                featured_media_id = self.upload_media(
                    image_path=article_data['image_path'],
                    title=article_data['title']
                )
                
                # 一時ファイルを削除
                try:
                    os.unlink(article_data['image_path'])
                    print(f"一時ファイルを削除しました: {article_data['image_path']}")
                except Exception as e:
                    print(f"⚠️ 一時ファイルの削除に失敗: {e}")
            
            # WordPressに投稿
            print("\nWordPressへの投稿を開始します...")
            result = self.create_post(
                title=article_data['title'],
                content=article_data['content'],
                status='publish',
                featured_media_id=featured_media_id
            )
            
            print(f"\n✓ 投稿成功！")
            print(f"記事ID: {result.get('id')}")
            print(f"記事URL: {result.get('link', 'N/A')}")
            if featured_media_id:
                print(f"アイキャッチ画像ID: {featured_media_id}")
            
            return result
            
        except Exception as e:
            print(f"投稿処理でエラーが発生しました: {e}")
            raise


if __name__ == "__main__":
    poster = WordPressPoster()
    poster.post_daily_article()

