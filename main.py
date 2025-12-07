"""
メイン実行ファイル
手動実行またはスケジューラーとして実行可能
"""

import sys
import os
from wordpress_poster import WordPressPoster

def main():
    """
    メイン関数
    引数なし: 即座に投稿
    --scheduler: スケジューラーとして実行
    """
    if len(sys.argv) > 1 and sys.argv[1] == '--scheduler':
        # スケジューラーとして実行
        from scheduler import run_scheduler
        run_scheduler()
    else:
        # 即座に投稿
        debug_mode = '--debug' in sys.argv
        poster = WordPressPoster(debug=debug_mode)
        poster.post_daily_article()

if __name__ == "__main__":
    main()

