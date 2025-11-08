#!/usr/bin/env python3
"""
REST APIの詳細なテストスクリプト
GitHub Actionsと同じ環境で何が起きているか確認
"""
import os
import requests
from dotenv import load_dotenv
import json

load_dotenv()

def test_rest_api_detailed():
    """REST APIの詳細なテスト"""
    
    base_url = os.getenv('WORDPRESS_URL', 'https://freeeeeeestyle.com').strip().rstrip('/')
    username = os.getenv('WORDPRESS_USERNAME')
    password = os.getenv('WORDPRESS_PASSWORD')
    
    print("="*80)
    print("REST API 詳細テスト")
    print("="*80)
    print(f"URL: {base_url}")
    print(f"ユーザー名: {username}")
    print(f"パスワード長: {len(password) if password else 0}文字")
    print(f"パスワード先頭4文字: {password[:4] if password else 'なし'}")
    print("="*80)
    
    # テスト1: ユーザー情報を取得（権限確認）
    print("\n[テスト1] ユーザー情報と権限を確認...")
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
            print(f"  - ID: {user_info.get('id')}")
            print(f"  - 名前: {user_info.get('name')}")
            print(f"  - ユーザー名: {user_info.get('slug')}")
            print(f"  - 権限: {user_info.get('capabilities', {})}")
            
            # 投稿権限があるか確認
            caps = user_info.get('capabilities', {})
            can_publish = caps.get('publish_posts', False) or caps.get('administrator', False)
            print(f"  - 投稿権限: {'✅ あり' if can_publish else '❌ なし'}")
            
            if not can_publish:
                print("\n⚠️  警告: このユーザーには投稿権限がありません！")
                print("WordPress管理画面で、ユーザー権限を「管理者」または「編集者」に変更してください。")
        else:
            print(f"❌ ユーザー情報取得失敗")
            print(f"レスポンス: {response.text}")
    except Exception as e:
        print(f"❌ エラー: {e}")
    
    # テスト2: 投稿一覧を取得（認証確認）
    print("\n[テスト2] 投稿一覧を取得（認証確認）...")
    try:
        posts_url = f"{base_url}/wp-json/wp/v2/posts"
        response = requests.get(
            posts_url,
            auth=(username, password),
            timeout=10
        )
        print(f"ステータスコード: {response.status_code}")
        
        if response.status_code == 200:
            posts = response.json()
            print(f"✅ 認証成功！投稿数: {len(posts)}")
        else:
            print(f"❌ 認証失敗")
            print(f"レスポンス: {response.text}")
    except Exception as e:
        print(f"❌ エラー: {e}")
    
    # テスト3: 実際に投稿を試みる（下書き）
    print("\n[テスト3] 下書き投稿をテスト...")
    try:
        posts_url = f"{base_url}/wp-json/wp/v2/posts"
        
        test_data = {
            'title': 'テスト投稿（自動削除予定）',
            'content': '<p>これはテスト投稿です。自動的に削除されます。</p>',
            'status': 'draft'
        }
        
        print(f"投稿URL: {posts_url}")
        print(f"投稿データ: {json.dumps(test_data, ensure_ascii=False, indent=2)}")
        
        response = requests.post(
            posts_url,
            json=test_data,
            auth=(username, password),
            timeout=10
        )
        
        print(f"\nステータスコード: {response.status_code}")
        print(f"レスポンスヘッダー:")
        for key, value in response.headers.items():
            if key.lower() in ['content-type', 'x-wp-total', 'x-wp-totalpages', 'allow']:
                print(f"  {key}: {value}")
        
        if response.status_code == 201:
            post_info = response.json()
            print(f"\n✅ 投稿成功！")
            print(f"  - 投稿ID: {post_info.get('id')}")
            print(f"  - URL: {post_info.get('link')}")
            print(f"  - ステータス: {post_info.get('status')}")
        elif response.status_code == 403:
            print(f"\n❌ 403 Forbidden エラー")
            print("\n詳細なエラー情報:")
            try:
                error_json = response.json()
                print(f"  - エラーコード: {error_json.get('code', 'なし')}")
                print(f"  - エラーメッセージ: {error_json.get('message', 'なし')}")
                if 'data' in error_json:
                    print(f"  - エラーデータ: {json.dumps(error_json['data'], ensure_ascii=False, indent=4)}")
            except:
                print(f"  - レスポンス（テキスト）: {response.text}")
            
            print("\n考えられる原因:")
            print("1. ユーザー権限が不足している（投稿者以下の権限）")
            print("2. WordPressのユーザーロール設定に問題がある")
            print("3. 別のプラグインがREST APIをブロックしている")
            print("4. .htaccessでREST APIへのPOSTがブロックされている")
        else:
            print(f"\n❌ 投稿失敗: {response.status_code}")
            print(f"レスポンス: {response.text}")
    except Exception as e:
        print(f"❌ エラー: {e}")
        import traceback
        traceback.print_exc()
    
    # テスト4: REST APIのルート情報を取得
    print("\n[テスト4] REST APIのルート情報を確認...")
    try:
        root_url = f"{base_url}/wp-json/"
        response = requests.get(root_url, timeout=10)
        print(f"ステータスコード: {response.status_code}")
        
        if response.status_code == 200:
            root_info = response.json()
            print(f"✅ REST APIは有効")
            print(f"  - 名前: {root_info.get('name', 'なし')}")
            print(f"  - 説明: {root_info.get('description', 'なし')}")
            print(f"  - URL: {root_info.get('url', 'なし')}")
            
            # 認証方法を確認
            if 'authentication' in root_info:
                print(f"  - 認証方法: {root_info['authentication']}")
        else:
            print(f"❌ REST APIへのアクセス失敗")
            print(f"レスポンス: {response.text}")
    except Exception as e:
        print(f"❌ エラー: {e}")
    
    print("\n" + "="*80)
    print("テスト完了")
    print("="*80)

if __name__ == "__main__":
    test_rest_api_detailed()

