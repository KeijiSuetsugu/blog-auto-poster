"""
人間関係に関するブログ記事生成モジュール
2000字程度の記事を生成します
"""

import os
import re
from openai import OpenAI
from dotenv import load_dotenv
import random

load_dotenv()

class ArticleGenerator:
    def __init__(self):
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEYを.envファイルに設定してください")
        
        # APIキーから余分な空白文字を削除
        api_key = api_key.strip()
        
        # APIキーの形式を確認
        if not api_key.startswith('sk-'):
            raise ValueError(f"無効なAPIキー形式です。APIキーは'sk-'で始まる必要があります。")
        
        if api_key.startswith('sk-proj-'):
            print("⚠️ プロジェクトAPIキーが使用されています。プロジェクトのクォータ設定を確認してください。")
        
        # デバッグ用（APIキーの最初と最後の数文字のみ表示）
        api_key_preview = f"{api_key[:10]}...{api_key[-10:]}" if len(api_key) > 20 else "***"
        print(f"DEBUG: APIキーの長さ: {len(api_key)}文字")
        print(f"DEBUG: APIキーのプレビュー: {api_key_preview}")
        
        self.client = OpenAI(api_key=api_key)
        
        # 記事のテーマ（人間関係に関する幅広いテーマ）
        self.themes = [
            "人との距離感を適切に保つ方法",
            "職場での人間関係を円滑にするコツ",
            "家族との関係を改善するためのヒント",
            "友人関係で大切にすべきこと",
            "一人の時間と人との時間のバランス",
            "コミュニケーション能力を高める方法",
            "人間関係のストレスを軽減する考え方",
            "新しい環境で人間関係を築くポイント",
            "誤解を解くための対話の技術",
            "感謝の気持ちを伝える大切さ",
            "共感力の高め方",
            "人間関係で疲れないための境界線の引き方",
            "相手の立場に立って考える習慣",
            "人間関係の悩みを解決するための一歩",
            "温かい人間関係を育む小さな習慣",
        ]
        
    def generate_article(self):
        """
        2000字程度の人間関係に関する記事を生成
        
        Returns:
            dict: {'title': str, 'content': str}
        """
        theme = random.choice(self.themes)
        
        system_prompt = """あなたは人間関係に関する専門的なブログ記事を書く経験豊富なライターです。
以下の条件を厳密に守って記事を執筆してください：

【文字数について】
- 本文は必ず2000字以上、2200字程度にする（タイトルは除く）
- 文字数が不足している場合は、具体例や実践的なアドバイスを追加する

【内容について】
- メンタル的に悩んでいる人、頑張っているが成果が出ない人にも共感できる内容にする
- 読者の気持ちに寄り添う温かいトーンで書く
- 具体的で実践的なアドバイスを必ず含める
- 読者が「やってみよう」と思えるような行動につながる内容にする
- 人間関係の悩みや課題を前向きに解決する方向性を示す

【構成について】
- 導入: 読者が「自分事」として捉えられるような導入
- 本論: 具体的なアドバイスや実践方法を複数のセクションに分けて説明
- まとめ: 行動を促す前向きな締めくくり

【形式について】
- HTML形式で出力する（段落は<p>タグで囲む）
- 見出しは<h2>タグを使用して構造化する

【出力フォーマット】
1行目: タイトル: [記事のタイトル]
2行目以降: [HTML形式の本文]
"""
        
        user_prompt = f"""以下のテーマについて、上記の条件を守って記事を書いてください：

テーマ: {theme}

記事を執筆してください。"""

        try:
            print(f"OpenAI APIにリクエストを送信中... (モデル: gpt-4o-mini)")
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",  # より安価なモデルを使用（必要に応じてgpt-4に変更）
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.8,
                max_tokens=3000  # 2000字程度の記事を生成するため、トークン数を増やす
            )
            
            article_text = response.choices[0].message.content.strip()
            
            # タイトルと本文を分割
            lines = article_text.split('\n')
            title = None
            content_lines = []
            
            for i, line in enumerate(lines):
                if line.startswith('タイトル:') or line.startswith('タイトル：'):
                    title = line.replace('タイトル:', '').replace('タイトル：', '').strip()
                elif title is None and line.strip() and not line.strip().startswith('#'):
                    # タイトルが明確でない場合は最初の行をタイトルとして使用
                    if not title and i == 0:
                        title = line.strip()
                    else:
                        content_lines.append(line)
                else:
                    content_lines.append(line)
            
            # タイトルが見つからない場合はテーマを使用
            if not title:
                title = theme
            
            # 本文を結合
            content = '\n'.join(content_lines).strip()
            
            # 本文が空の場合は全体を本文として使用
            if not content:
                content = article_text
                if title == theme:
                    # 最初の行をタイトルとして抽出を試みる
                    first_line = article_text.split('\n')[0]
                    if len(first_line) < 100:  # タイトルっぽい長さなら
                        title = first_line.strip()
                        content = '\n'.join(article_text.split('\n')[1:]).strip()
            
            # 本文がHTML形式でない場合は<p>タグで囲む
            if not content.startswith('<'):
                paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
                content = '\n\n'.join([f'<p>{p}</p>' for p in paragraphs])
            
            # 文字数を確認（HTMLタグを除去して純粋なテキストの文字数をカウント）
            plain_text = re.sub(r'<[^>]+>', '', content)
            plain_text_length = len(plain_text.strip())
            print(f"生成された記事の文字数: {plain_text_length}文字")
            
            # 文字数が足りない場合は補足を追加
            if plain_text_length < 1800:
                needed_length = max(2000 - plain_text_length, 300)  # 最低300字は追加
                additional_prompt = f"""上記の記事の続きとして、さらに約{needed_length}字以上の内容を追加してください。
同じテーマで、以下の点を含めてください：
- 読者が実践できる具体的なアドバイス
- 具体例やエピソード
- 読者を励ます前向きなメッセージ

HTML形式（<p>タグを使用）で出力してください。"""
                
                additional_response = self.client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"既存の記事:\n{content}\n\n{additional_prompt}"}
                    ],
                    temperature=0.8,
                    max_tokens=1000
                )
                
                additional_content = additional_response.choices[0].message.content.strip()
                if not additional_content.startswith('<'):
                    paragraphs = [p.strip() for p in additional_content.split('\n\n') if p.strip()]
                    additional_content = '\n\n'.join([f'<p>{p}</p>' for p in paragraphs])
                
                content += '\n\n' + additional_content
            
            return {
                'title': title,
                'content': content
            }
            
        except Exception as e:
            error_msg = str(e)
            print(f"記事生成エラー: {error_msg}")
            
            # APIキーエラーの場合
            if "invalid_api_key" in error_msg or "401" in error_msg or "Incorrect API key" in error_msg:
                print("\n" + "="*60)
                print("⚠️  APIキーエラーが発生しました")
                print("="*60)
                print("\n対処方法:")
                print("1. APIキーが正しくコピーされているか確認:")
                print("   - .envファイルのOPENAI_API_KEYの値を確認")
                print("   - 余分なスペースや改行が入っていないか確認")
                print("\n2. 新しいAPIキーを作成:")
                print("   https://platform.openai.com/api-keys")
                print("   - 古いキーが無効化されている可能性があります")
                print("   - 新しいキーを作成して.envファイルを更新してください")
                print("="*60 + "\n")
            # クォータエラーの場合、詳しい説明を表示
            elif "insufficient_quota" in error_msg or "429" in error_msg:
                print("\n" + "="*60)
                print("⚠️  OpenAI APIクォータエラーが発生しました")
                print("="*60)
                print("\n対処方法:")
                print("1. OpenAIダッシュボードを確認:")
                print("   https://platform.openai.com/account/billing")
                print("\n2. プロジェクトのクォータ設定を確認:")
                print("   - APIキーが特定のプロジェクトに紐づいている場合、")
                print("     そのプロジェクトのクォータを使い切っている可能性があります")
                print("   - 新しいAPIキーを生成するか、プロジェクトのクォータを増やしてください")
                print("\n3. 組織レベルのクォータを確認:")
                print("   - 組織全体のクォータ設定も確認してください")
                print("="*60 + "\n")
            
            raise


def generate_article():
    """
    記事生成関数（外部から呼び出し可能）
    
    Returns:
        dict: {'title': str, 'content': str}
    """
    generator = ArticleGenerator()
    return generator.generate_article()


if __name__ == "__main__":
    generator = ArticleGenerator()
    article = generator.generate_article()
    print("\n" + "="*50)
    print("生成された記事")
    print("="*50)
    print(f"\nタイトル: {article['title']}\n")
    print(f"本文:\n{article['content']}\n")
    print("="*50)

