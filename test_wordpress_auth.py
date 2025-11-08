#!/usr/bin/env python3
"""
WordPressの認証をテストするスクリプト
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

def test_wordpress_connection():
    """WordPressのREST APIとの接続をテスト"""
    
    base_url = os.getenv('WORDPRESS_URL', 'https://freeeeeeestyle.com').strip().rstrip('/')
    username = os.getenv('WORDPRESS_USERNAME')
    password = os.getenv('WORDPRESS_PASSWORD')
    
    print("="*60)
    print("WordPress接続テスト")
    print("="*60)
    print(f"URL: {base_url}")
    print(f"ユーザー名: {username}")
    print(f"パスワード: {'*' * len(password) if password else 'なし'} ({len(password) if password else 0}文字)")
    print("="*60)
    
    # テスト1: REST APIが有効かチェック
    print("\n[テスト1] REST APIが有効かチェック...")
    try:
        api_root = f"{base_url}/wp-json/wp/v2"
        response = requests.get(api_root, timeout=10)
        print(f"✅ REST APIは有効です (ステータス: {response.status_code})")
    except Exception as e:
        print(f"❌ REST APIへのアクセスに失敗: {e}")
        return
    
    # テスト2: 認証情報をテスト（既存の投稿を取得）
    print("\n[テスト2] 認証情報をテスト（投稿一覧を取得）...")
    try:
        posts_url = f"{base_url}/wp-json/wp/v2/posts"
        response = requests.get(
            posts_url,
            auth=(username, password),
            timeout=10
        )
        print(f"ステータスコード: {response.status_code}")
        if response.status_code == 200:
            print(f"✅ 認証成功！投稿を取得できました")
            posts = response.json()
            print(f"投稿数: {len(posts)}")
        else:
            print(f"❌ 認証失敗: {response.status_code}")
            print(f"レスポンス: {response.text}")
    except Exception as e:
        print(f"❌ エラー: {e}")
    
    # テスト3: ユーザー情報を取得
    print("\n[テスト3] ユーザー情報を取得...")
    try:
        users_url = f"{base_url}/wp-json/wp/v2/users/me"
        response = requests.get(
            users_url,
            auth=(username, password),
            timeout=10
        )
        print(f"ステータスコード: {response.status_code}")
        if response.status_code == 200:
            user_info = response.json()
            print(f"✅ ユーザー情報取得成功")
            print(f"ID: {user_info.get('id')}")
            print(f"名前: {user_info.get('name')}")
            print(f"ユーザー名: {user_info.get('slug')}")
            print(f"権限: {user_info.get('capabilities', {})}")
        else:
            print(f"❌ ユーザー情報取得失敗: {response.status_code}")
            print(f"レスポンス: {response.text}")
    except Exception as e:
        print(f"❌ エラー: {e}")
    
    # テスト4: 下書き投稿を試す
    print("\n[テスト4] 下書き投稿をテスト...")
    try:
        posts_url = f"{base_url}/wp-json/wp/v2/posts"
        test_data = {
            'title': 'テスト投稿（削除してください）',
            'content': 'これはテスト投稿です。削除してください。',
            'status': 'draft'  # 下書きとして投稿
        }
        response = requests.post(
            posts_url,
            json=test_data,
            auth=(username, password),
            timeout=10
        )
        print(f"ステータスコード: {response.status_code}")
        if response.status_code == 201:
            post_info = response.json()
            print(f"✅ 下書き投稿成功！")
            print(f"投稿ID: {post_info.get('id')}")
            print(f"URL: {post_info.get('link')}")
        else:
            print(f"❌ 投稿失敗: {response.status_code}")
            print(f"レスポンス: {response.text}")
            
            # 詳細なエラー情報を表示
            if response.status_code == 403:
                print("\n" + "="*60)
                print("⚠️  403エラーの詳細分析")
                print("="*60)
                try:
                    error_data = response.json()
                    print(f"エラーコード: {error_data.get('code')}")
                    print(f"エラーメッセージ: {error_data.get('message')}")
                    print(f"エラーデータ: {error_data.get('data')}")
                except:
                    print(f"エラー詳細: {response.text}")
                print("="*60)
    except Exception as e:
        print(f"❌ エラー: {e}")
    
    print("\n" + "="*60)
    print("テスト完了")
    print("="*60)

if __name__ == "__main__":
    test_wordpress_connection()

