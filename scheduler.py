"""
毎日自動でブログ記事を投稿するスケジューラー
"""

import schedule
import time
from datetime import datetime
from wordpress_poster import WordPressPoster
import os
from dotenv import load_dotenv

load_dotenv()

def job():
    """
    毎日の投稿ジョブ
    """
    try:
        print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ===== 投稿ジョブ開始 =====\n")
        
        poster = WordPressPoster()
        poster.post_daily_article()
        
        print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ===== 投稿ジョブ完了 =====\n")
        
    except Exception as e:
        print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] エラー: {e}\n")
        # エラーが発生しても次回の実行は継続

def run_scheduler():
    """
    スケジューラーを開始
    """
    # 投稿時間を環境変数から取得（デフォルトは09:00）
    post_time = os.getenv('POST_TIME', '09:00')
    
    print(f"スケジューラーを開始しました")
    print(f"毎日 {post_time} に記事を投稿します")
    print(f"現在時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\nスケジューラーを停止するには Ctrl+C を押してください\n")
    
    # スケジュールを設定
    schedule.every().day.at(post_time).do(job)
    
    # スケジューラーを実行
    while True:
        schedule.run_pending()
        time.sleep(60)  # 1分ごとにチェック

if __name__ == "__main__":
    try:
        run_scheduler()
    except KeyboardInterrupt:
        print("\n\nスケジューラーを停止しました")

