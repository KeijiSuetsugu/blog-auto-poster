"""
WordPress自動投稿スクリプト
人間関係に関するブログ記事を毎日自動投稿します
"""

import os
import requests
from datetime import datetime
from dotenv import load_dotenv
from article_generator import generate_article

# 環境変数を読み込み
load_dotenv()

class WordPressPoster:
    def __init__(self):
        self.base_url = os.getenv('WORDPRESS_URL', 'https://freeeeeeestyle.com')
        self.username = os.getenv('WORDPRESS_USERNAME')
        self.password = os.getenv('WORDPRESS_PASSWORD')
        
        if not self.username or not self.password:
            raise ValueError("WORDPRESS_USERNAMEとWORDPRESS_PASSWORDを.envファイルに設定してください")
        
        # WordPress REST APIのエンドポイント
        self.api_url = f"{self.base_url}/wp-json/wp/v2/posts"
        
    def create_post(self, title, content, status='publish'):
        """
        WordPressに記事を投稿
        
        Args:
            title: 記事のタイトル
            content: 記事の本文（HTML形式）
            status: 公開ステータス（'publish', 'draft', 'pending'など）
        
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
        
        try:
            response = requests.post(
                self.api_url,
                json=data,
                headers=headers,
                auth=(self.username, self.password),
                timeout=30
            )
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"投稿エラー: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"レスポンス内容: {e.response.text}")
            raise
    
    def post_daily_article(self):
        """
        毎日の記事を生成して投稿
        """
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 記事生成を開始します...")
        
        try:
            # 記事を生成
            article_data = generate_article()
            
            print(f"タイトル: {article_data['title']}")
            print(f"本文の長さ: {len(article_data['content'])}文字")
            
            # WordPressに投稿
            print("WordPressへの投稿を開始します...")
            result = self.create_post(
                title=article_data['title'],
                content=article_data['content'],
                status='publish'
            )
            
            print(f"投稿成功！記事ID: {result.get('id')}")
            print(f"記事URL: {result.get('link', 'N/A')}")
            
            return result
            
        except Exception as e:
            print(f"投稿処理でエラーが発生しました: {e}")
            raise


if __name__ == "__main__":
    poster = WordPressPoster()
    poster.post_daily_article()

