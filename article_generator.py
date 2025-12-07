"""
AI関連の最新ニュースを基にしたブログ記事生成モジュール
最新機能や比較など読者が興味を持つ内容を含む3000字程度の記事を生成します
画像生成機能（Unsplash API / DALL-E 3）も含みます
重複投稿防止機能付き
"""

import os
import sys
import re
import requests
import tempfile
import json
from datetime import datetime, timedelta
from openai import OpenAI
from dotenv import load_dotenv
import random
from typing import Optional, Dict, Tuple, List
from pathlib import Path
import xml.etree.ElementTree as ET
import urllib.request
import time

load_dotenv()

class ArticleGenerator:
    def __init__(self, image_source: str = 'unsplash', debug: bool = False):
        """
        Args:
            image_source: 画像生成のソース ('unsplash' または 'dalle')
        """
        raw_api_key = os.getenv('OPENAI_API_KEY')
        if not raw_api_key:
            raise ValueError("OPENAI_API_KEYが設定されていません。GitHub Secretsを確認してください。")

        # キーの中から'sk-'で始まる部分を探して、そこから後ろを正しいキーとして抜き出す
        sk_index = raw_api_key.find('sk-')
        if sk_index != -1:
            api_key = raw_api_key[sk_index:].strip()
        else:
            api_key = raw_api_key.strip()

        # 最終チェック
        if not api_key.startswith(('sk-', 'sk-proj-')):
            error_preview = raw_api_key.replace('\n', ' ').replace('\r', ' ')[0:20]
            raise ValueError(f"無効なAPIキー形式です。取得したキーの先頭部分: '{error_preview}...'")
        
        if api_key.startswith('sk-proj-'):
            print("⚠️ プロジェクトAPIキーが使用されています。プロジェクトのクォータ設定を確認してください。")
        
        # デバッグ用（APIキーの最初と最後の数文字のみ表示）
        api_key_preview = f"{api_key[:10]}...{api_key[-10:]}" if len(api_key) > 20 else "***"
        print(f"DEBUG: APIキーの長さ: {len(api_key)}文字")
        print(f"DEBUG: APIキーのプレビュー: {api_key_preview}")
        
        self.client = OpenAI(api_key=api_key)
        
        # 画像生成の設定
        self.image_source = image_source
        self.unsplash_access_key = os.getenv('UNSPLASH_ACCESS_KEY', '')
        self.banana_api_key = os.getenv('BANANA_API_KEY', '')
        
        # NewsAPI設定（オプション）
        self.newsapi_key = os.getenv('NEWSAPI_KEY', '')
        
        # 投稿履歴ファイルのパス
        self.history_file = Path('post_history.json')
        
        print(f"📝 画像ソース: {self.image_source}")
        print(f"🔑 Unsplash APIキー: {'設定済み' if self.unsplash_access_key else '未設定'}")
        print(f"🔑 Banana Pro APIキー: {'設定済み' if self.banana_api_key else '未設定'}")
        print(f"🔑 NewsAPI キー: {'設定済み' if self.newsapi_key else '未設定'}")
        print("=" * 60 + "\n")
        
        # デバッグモード
        self.debug = debug
        self.debug_dir = Path('debug_output')
        if self.debug:
            self.debug_dir.mkdir(exist_ok=True)
            print(f"🔧 デバッグモード有効: {self.debug_dir.absolute()}")
        
        # 記事のテーマ（AI関連のトピック - フォールバック用）
        self.ai_topics = [
            "ChatGPTとClaudeの比較：どちらが優れているか",
            "GPT-4oの新機能と実用的な活用法",
            "AI画像生成ツール比較：Midjourney vs DALL-E 3 vs Stable Diffusion",
            "AIプログラミングアシスタント：GitHub Copilot vs Cursor vs Codeium",
            "AI音声生成技術の最新動向：ElevenLabsとその競合",
            "AI動画生成の最前線：Runway MLとPikaの比較",
            "AI検索エンジン：Perplexity vs Googleの違い",
            "AIコードレビューツールの実用性",
            "AI翻訳ツールの精度比較：DeepL vs Google翻訳 vs ChatGPT",
            "AI音楽生成：Suno AIとUdioの可能性",
            "AI自動化ツール：Zapier vs Make vs n8n",
            "AIデータ分析ツールの比較",
            "AIライティングツール：Jasper vs Copy.ai vs Writesonic",
            "AIデザインツール：Canva AI vs Adobe Firefly",
            "AI教育ツールの最新動向",
            "AIヘルスケアアプリケーションの現状",
            "AI金融サービス：ロボアドバイザーの比較",
            "AIセキュリティツールの重要性",
            "AIマーケティングツールの活用方法",
            "AI開発フレームワーク：LangChain vs LlamaIndex",
        ]
    
    def _load_post_history(self) -> List[Dict]:
        """
        投稿履歴を読み込む
        
        Returns:
            投稿履歴のリスト
        """
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    history = json.load(f)
                    return history if isinstance(history, list) else []
            except Exception as e:
                print(f"⚠️ 投稿履歴の読み込みエラー: {e}")
                return []
        return []
    
    def _save_post_history(self, history: List[Dict]):
        """
        投稿履歴を保存する
        
        Args:
            history: 投稿履歴のリスト
        """
        try:
            # 30日以上前の履歴を削除
            cutoff_date = datetime.now() - timedelta(days=30)
            filtered_history = [
                h for h in history
                if datetime.fromisoformat(h.get('date', '2000-01-01')) > cutoff_date
            ]
            
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(filtered_history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️ 投稿履歴の保存エラー: {e}")
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """
        2つのテキストの類似度を計算（簡易版）
        
        Args:
            text1: テキスト1
            text2: テキスト2
            
        Returns:
            類似度（0.0〜1.0）
        """
        # 単語に分割
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        # 共通単語の割合を計算
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0
    
    def _is_duplicate(self, title: str, content: str = "") -> bool:
        """
        タイトルと内容が重複していないかチェック（厳密版）
        
        Args:
            title: 記事のタイトル
            content: 記事の内容（オプション）
            
        Returns:
            重複している場合True
        """
        history = self._load_post_history()
        
        title_lower = title.lower().strip()
        
        for entry in history:
            existing_title = entry.get('title', '').lower().strip()
            existing_theme = entry.get('theme', '').lower().strip()
            
            # 1. 完全一致チェック
            if title_lower == existing_title:
                print(f"⚠️ 完全一致: {existing_title}")
                return True
            
            # 2. タイトルの類似度チェック（70%以上で重複）
            similarity = self._calculate_similarity(title_lower, existing_title)
            if similarity > 0.7:
                print(f"⚠️ 高類似度 ({similarity:.2%}): {existing_title}")
                return True
            
            # 3. 最初の30文字が一致している場合
            if len(title_lower) > 30 and len(existing_title) > 30:
                if title_lower[:30] == existing_title[:30]:
                    print(f"⚠️ 冒頭一致: {existing_title}")
                    return True
            
            # 4. テーマの重複チェック（同じテーマは避ける）
            if existing_theme and len(existing_theme) > 10:
                theme_similarity = self._calculate_similarity(title_lower, existing_theme)
                if theme_similarity > 0.6:
                    print(f"⚠️ テーマ重複 ({theme_similarity:.2%}): {existing_theme}")
                    return True
        
        return False
    
    def _save_debug_artifact(self, name: str, content: str):
        """
        デバッグ用のアーティファクトを保存
        """
        if not self.debug:
            return
            
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{timestamp}_{name}"
            filepath = self.debug_dir / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"🔧 デバッグ情報を保存: {filepath}")
        except Exception as e:
            print(f"⚠️ デバッグ情報保存エラー: {e}")

    def _fetch_rss_news(self) -> Optional[str]:
        """
        RSSフィードから最新ニュースを取得
        """
        rss_urls = [
            "https://openai.com/news/rss.xml",
            "https://blogs.microsoft.com/ai/feed/",
            "https://aws.amazon.com/blogs/machine-learning/feed/",
            "https://research.google/blog/rss/",
            "https://www.mit.edu/rss/news.xml",  # MIT News (general, but often AI)
            "https://venturebeat.com/category/ai/feed/",
            "https://techcrunch.com/category/artificial-intelligence/feed/",
            "https://www.artificialintelligence-news.com/feed/",
        ]
        
        all_news = []
        
        print("RSSフィードから最新ニュースを取得中...")
        
        for url in rss_urls:
            try:
                print(f"  - Fetching: {url}")
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=5) as response:
                    xml_content = response.read()
                    root = ET.fromstring(xml_content)
                    
                    # チャンネル情報を取得
                    channel_title = "Unknown Source"
                    channel = root.find('channel')
                    if channel is not None:
                        title_elem = channel.find('title')
                        if title_elem is not None:
                            channel_title = title_elem.text
                    
                    # アイテムを取得
                    count = 0
                    for item in root.findall('.//item'):
                        if count >= 2: break  # 各ソースから最新2件
                        
                        title = item.find('title').text if item.find('title') is not None else "No Title"
                        desc = item.find('description').text if item.find('description') is not None else ""
                        link = item.find('link').text if item.find('link') is not None else ""
                        
                        # HTMLタグを除去
                        if desc:
                            desc = re.sub(r'<[^>]+>', '', desc)[:200] + "..."
                        
                        all_news.append(f"- [{channel_title}] {title}: {desc} ({link})")
                        count += 1
                        
            except Exception as e:
                print(f"  ⚠️ RSS取得エラー ({url}): {e}")
        
        if all_news:
            result = "\n".join(all_news)
            print(f"✓ RSSから{len(all_news)}件のニュースを取得しました")
            self._save_debug_artifact("rss_news.txt", result)
            return result
            
        return None

    def _get_latest_ai_news(self) -> Optional[str]:
        """
        最新のAIニュースを取得
        
        Returns:
            ニュースの要約テキスト、失敗時はNone
        """
        # 1. NewsAPIを使用
        if self.newsapi_key:
            try:
                print("NewsAPIから最新のAIニュースを取得中...")
                url = "https://newsapi.org/v2/everything"
                params = {
                    'q': 'artificial intelligence OR AI OR machine learning OR ChatGPT OR GPT-4',
                    'language': 'ja',
                    'sortBy': 'publishedAt',
                    'pageSize': 5,
                    'from': (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
                }
                headers = {
                    'X-API-Key': self.newsapi_key
                }
                
                response = requests.get(url, params=params, headers=headers, timeout=10)
                response.raise_for_status()
                
                data = response.json()
                articles = data.get('articles', [])
                
                if articles:
                    # 最新の記事を要約
                    news_summary = []
                    for article in articles[:3]:  # 最新3件
                        title = article.get('title', '')
                        description = article.get('description', '')
                        if title and description:
                            news_summary.append(f"- {title}: {description}")
                    
                    if news_summary:
                        result = "\n".join(news_summary)
                        print(f"✓ NewsAPIから{len(articles)}件のニュースを取得しました")
                        self._save_debug_artifact("newsapi_result.txt", result)
                        return result
                        
            except Exception as e:
                print(f"⚠️ NewsAPI取得エラー: {e}")
        
        # 2. RSSフィードを使用（フォールバック1）
        rss_news = self._fetch_rss_news()
        if rss_news:
            return rss_news
        
        # 3. OpenAIを使用して最新情報を検索（フォールバック2）
        try:
            print("OpenAIを使用して最新のAIニュースを検索中...")
            search_prompt = """最新のAI（人工知能）関連のニュースや技術動向について、2024年以降の最新情報を幅広く教えてください。
大手テック企業だけでなく、スタートアップ、研究論文、倫理的課題、規制など、多角的な視点からの情報を求めています。

特に以下のトピックに関連する情報を優先してください：
- 新しいAIモデルやサービスのリリース（マイナーなものも含む）
- AIツールの比較や評価
- AI技術の実用的な活用事例
- AI業界の最新トレンドや議論
- AI規制や倫理に関する新しい動き

最新の情報を5-7件、簡潔にまとめてください。各項目は「- タイトル: 説明」の形式で出力してください。"""
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "あなたはAI技術の専門家です。最新のAIニュースや技術動向について正確な情報を提供します。"},
                    {"role": "user", "content": search_prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            news_summary = response.choices[0].message.content.strip()
            print("✓ OpenAIから最新情報を取得しました")
            self._save_debug_artifact("openai_news_search.txt", news_summary)
            return news_summary
            
        except Exception as e:
            print(f"⚠️ 最新情報取得エラー: {e}")
            return None
    
    def _generate_image_keywords(self, theme: str) -> str:
        """
        記事テーマから画像検索用のキーワードを生成（OpenAIを使用）
        
        Args:
            theme: 記事のテーマ
            
        Returns:
            英語の検索キーワード
        """
        try:
            print(f"画像検索用キーワードを生成中... (テーマ: {theme})")
            prompt = f"""Based on the following article theme/title, generate 3-5 specific English keywords for searching high-quality stock photos (Unsplash).
Theme: {theme}

Requirements:
- Keywords should be in English
- Specific and relevant to the topic
- Suitable for finding professional, modern technology images
- Return ONLY the keywords separated by spaces (no punctuation, no explanations)
- Example output: artificial intelligence robot future technology blue"""

            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an expert at finding the perfect stock photos for tech articles."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=50
            )
            
            keywords = response.choices[0].message.content.strip()
            print(f"✓ 生成されたキーワード: {keywords}")
            return keywords
            
        except Exception as e:
            print(f"⚠️ キーワード生成エラー: {e}")
            # フォールバック
            return 'artificial intelligence technology future'
    
    def generate_image_from_unsplash(self, theme: str) -> Optional[Tuple[str, str]]:
        """
        Unsplash APIから記事テーマに関連する画像を取得
        
        Args:
            theme: 記事のテーマ
            
        Returns:
            (画像URL, 画像ファイルパス) のタプル、失敗時はNone
        """
        if not self.unsplash_access_key:
            print("⚠️ UNSPLASH_ACCESS_KEYが設定されていません。画像生成をスキップします。")
            return None
        
        try:
            keywords = self._generate_image_keywords(theme)
            print(f"Unsplash APIで画像を検索中... (キーワード: {keywords})")
            
            # Unsplash APIで画像を検索
            # キャッシュバスターとランダム性を追加
            random_sig = int(time.time() * 1000) % 10000
            # キーワードにランダムな要素を追加して多様性を出す
            random_terms = ["technology", "future", "digital", "cyber", "network", "data", "code"]
            enhanced_keywords = f"{keywords} {random.choice(random_terms)}"
            
            url = "https://api.unsplash.com/photos/random"
            params = {
                'query': enhanced_keywords,
                'orientation': 'landscape',
                'content_filter': 'high',
                'sig': random_sig  # キャッシュ回避
            }
            headers = {
                'Authorization': f'Client-ID {self.unsplash_access_key}'
            }
            
            if self.debug:
                print(f"🔧 Unsplash Request: {url} params={params}")
            
            response = requests.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            image_url = data['urls']['regular']  # 1080px幅の画像
            
            # 画像をダウンロード
            print(f"画像をダウンロード中: {image_url}")
            image_response = requests.get(image_url, timeout=30)
            image_response.raise_for_status()
            
            # 一時ファイルに保存
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
            temp_file.write(image_response.content)
            temp_file.close()
            
            print(f"✓ Unsplashから画像を取得しました: {temp_file.name}")
            return (image_url, temp_file.name)
            
        except Exception as e:
            print(f"⚠️ Unsplash画像取得エラー: {e}")
            return None
    
    def generate_image_from_banana_pro(self, theme: str, title: str) -> Optional[Tuple[str, str]]:
        """
        Banana Pro (Nano)で記事テーマに関連する画像を生成
        
        Args:
            theme: 記事のテーマ
            title: 記事のタイトル
            
        Returns:
            (画像URL, 画像ファイルパス) のタプル、失敗時はNone
        """
        if not self.banana_api_key:
            print("⚠️ BANANA_API_KEYが設定されていません。")
            return None
        
        try:
            import base64
            
            # プロンプトを生成（英語で）
            prompt = f"""Professional tech blog header image about {theme}. 
Modern, clean design with AI and technology theme. 
Futuristic, high quality, 4K, professional photography style.
Colors: blues, purples, tech gradients. No text."""
            
            print(f"Banana Pro (Nano)で画像を生成中...")
            print(f"プロンプト: {prompt[:100]}...")
            
            # Banana Pro APIを使用して画像生成
            url = "https://api.banana.dev/start/v4"
            headers = {
                "Content-Type": "application/json"
            }
            
            data = {
                "apiKey": self.banana_api_key,
                "modelKey": "flux-nano",  # Nanoモデルを使用
                "modelInputs": {
                    "prompt": prompt,
                    "width": 1024,
                    "height": 576,  # 16:9アスペクト比
                    "num_inference_steps": 4,  # Nanoは高速生成
                    "guidance_scale": 3.5
                }
            }
            
            # 画像生成リクエスト
            response = requests.post(url, json=data, headers=headers, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            
            # callIDを取得
            call_id = result.get('callID')
            if not call_id:
                print(f"⚠️ callIDが取得できませんでした: {result}")
                return None
            
            # 結果を取得
            print("画像生成中... (最大30秒待機)")
            check_url = "https://api.banana.dev/check/v4"
            max_wait = 30
            start_time = time.time()
            
            while time.time() - start_time < max_wait:
                check_data = {
                    "apiKey": self.banana_api_key,
                    "callID": call_id
                }
                
                check_response = requests.post(check_url, json=check_data, headers=headers, timeout=10)
                check_response.raise_for_status()
                
                check_result = check_response.json()
                
                if check_result.get('finished'):
                    model_outputs = check_result.get('modelOutputs', [{}])
                    if model_outputs and len(model_outputs) > 0:
                        # Base64エンコードされた画像を取得
                        image_base64 = model_outputs[0].get('image_base64')
                        if image_base64:
                            # Base64をデコードして画像として保存
                            image_data = base64.b64decode(image_base64)
                            
                            # 一時ファイルに保存
                            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
                            temp_file.write(image_data)
                            temp_file.close()
                            
                            print(f"✓ Banana Pro (Nano)で画像を生成しました: {temp_file.name}")
                            # URLはローカルファイルパスを返す
                            return (f"file://{temp_file.name}", temp_file.name)
                        else:
                            # URLが返される場合
                            image_url = model_outputs[0].get('image_url')
                            if image_url:
                                # 画像をダウンロード
                                print(f"画像をダウンロード中: {image_url}")
                                image_response = requests.get(image_url, timeout=30)
                                image_response.raise_for_status()
                                
                                # 一時ファイルに保存
                                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
                                temp_file.write(image_response.content)
                                temp_file.close()
                                
                                print(f"✓ Banana Pro (Nano)で画像を生成しました: {temp_file.name}")
                                return (image_url, temp_file.name)
                    
                    print(f"⚠️ 予期しない出力形式: {model_outputs}")
                    return None
                
                # まだ処理中の場合は待機
                time.sleep(1)
            
            print("⚠️ Banana Pro (Nano)画像生成タイムアウト")
            return None
            
        except Exception as e:
            print(f"⚠️ Banana Pro (Nano)画像生成エラー: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def generate_image_from_dalle(self, theme: str, title: str) -> Optional[Tuple[str, str]]:
        """
        DALL-E 3で記事テーマに関連する画像を生成
        
        Args:
            theme: 記事のテーマ
            title: 記事のタイトル
            
        Returns:
            (画像URL, 画像ファイルパス) のタプル、失敗時はNone
        """
        try:
            # プロンプトを生成（英語で）
            prompt = f"""Create a professional, modern illustration for an AI technology blog article about: {theme}. 
The image should be:
- Clean and minimalist design
- Suitable for a technology blog
- Related to artificial intelligence, AI technology, or digital innovation
- Modern tech colors (blues, purples, gradients)
- Futuristic but approachable
- No text in the image
Style: Modern tech illustration, professional, sleek"""
            
            print(f"DALL-E 3で画像を生成中...")
            print(f"プロンプト: {prompt[:100]}...")
            
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1,
            )
            
            image_url = response.data[0].url
            
            # 画像をダウンロード
            print(f"画像をダウンロード中: {image_url}")
            image_response = requests.get(image_url, timeout=30)
            image_response.raise_for_status()
            
            # 一時ファイルに保存
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
            temp_file.write(image_response.content)
            temp_file.close()
            
            print(f"✓ DALL-E 3で画像を生成しました: {temp_file.name}")
            return (image_url, temp_file.name)
            
        except Exception as e:
            print(f"⚠️ DALL-E 3画像生成エラー: {e}")
            return None
    
    def generate_image(self, theme: str, title: str = "") -> Optional[Tuple[str, str]]:
        """
        設定に基づいて画像を生成
        
        Args:
            theme: 記事のテーマ
            title: 記事のタイトル
            
        Returns:
            (画像URL, 画像ファイルパス) のタプル、失敗時はNone
        """
        if self.image_source == 'banana' or self.image_source == 'nano':
            result = self.generate_image_from_banana_pro(theme, title)
            # Banana Proが失敗した場合、Unsplashにフォールバック
            if result is None:
                print("Banana Proが失敗したため、Unsplashにフォールバックします...")
                result = self.generate_image_from_unsplash(theme)
            return result
        elif self.image_source == 'unsplash':
            result = self.generate_image_from_unsplash(theme)
            # Unsplashが失敗した場合、DALL-Eにフォールバック
            if result is None and os.getenv('DALLE_FALLBACK', 'false').lower() == 'true':
                print("Unsplashが失敗したため、DALL-E 3にフォールバックします...")
                result = self.generate_image_from_dalle(theme, title)
            return result
        elif self.image_source == 'dalle':
            return self.generate_image_from_dalle(theme, title)
        else:
            print(f"⚠️ 不明な画像ソース: {self.image_source}")
            return None
        
    def generate_article(self, generate_image: bool = True, max_retries: int = 5):
        """
        AI関連の最新ニュースを基にした4000〜5000字の実用的でユニークな記事を生成
        最新機能や比較など読者が興味を持つ内容を含む
        重複チェックを厳密に行い、絶対に同じ内容の記事を投稿しない
        Banana Pro Nanoで美しい画像を自動生成
        
        Args:
            generate_image: 画像を生成するかどうか
            max_retries: 重複回避のための最大リトライ回数（デフォルト5回）
        
        Returns:
            dict: {'title': str, 'content': str, 'image_path': str (optional), 'image_url': str (optional)}
        """
        print(f"\n{'='*60}")
        print("📰 最新AI記事生成開始")
        print(f"{'='*60}\n")
        
        # 最新ニュースを取得
        print("ステップ1: 最新AIニュースの取得")
        latest_news = self._get_latest_ai_news()
        
        if not latest_news:
            print("⚠️ 最新ニュースの取得に失敗しました。フォールバックトピックを使用します。")
        
        # 使用済みトピックを追跡
        used_topics = set()
        
        # フォールバック用のトピックを選択
        fallback_topic = random.choice(self.ai_topics)
        used_topics.add(fallback_topic)
        
        # 重複を避けながら記事を生成
        print(f"\nステップ2: 記事生成（最大{max_retries}回リトライ）")
        for attempt in range(max_retries):
            print(f"\n--- 生成試行 {attempt + 1}/{max_retries} ---")
            
            system_prompt = """あなたはAI技術の専門知識を持つ経験豊富なテックライターです。
以下の条件を厳密に守って記事を執筆してください：

【文字数について】
- 本文は必ず4000字以上、5000字程度にする（タイトルは除く）
- 詳細で読み応えのある長文記事にする
- 具体的な事例、比較情報、実用的なアドバイスを豊富に含める
- 各セクションを詳しく掘り下げて解説する

【内容について】
- 最新のAI技術やサービスに関する情報を含める
- AIツールの比較や評価を具体的に行う
- 読者が実際に使える実用的な情報を提供する
- 最新機能や新機能について詳しく解説する
- 読者が興味を持つような内容（比較、実用例、メリット・デメリットなど）を含める
- 専門的でありながら、初心者にもわかりやすい説明をする

【ターゲット読者について】
- AIに興味がある一般ユーザーから技術者まで幅広い読者を想定
- 実際にAIツールを使いたい人、比較検討している人を主なターゲットとする
- 実用的な情報を求めている読者に寄り添う
- 業界の動向を広く知りたい人

【記事のスタイル】
- 単なるニュースの羅列ではなく、それらが社会や個人の生活にどう影響するかを考察する
- 複数のニュースを関連付けて、大きなトレンドとして解説する
- 読者が「へぇ、そうなんだ」と思えるような深い洞察を含める

【構成について】
- 導入: 最新のAI技術やサービスの重要性を説明
- 最新動向: 最新ニュースや技術動向を紹介
- 詳細解説: 主要な機能や特徴を詳しく説明
- 比較・評価: 複数のツールやサービスを比較（該当する場合）
- 実用例: 実際の使用例や活用方法を紹介
- まとめ: 読者にとっての価値や今後の展望を提示

【形式について】
- HTML形式で出力する（段落は<p>タグで囲む）
- 見出しは<h2>タグを使用して構造化する
- 重要なポイントは<strong>タグで強調する
- 比較表やリストは<ul>や<ol>タグを使用する

【トーン】
- 専門的でありながら親しみやすい
- 最新技術への興奮や期待を伝える
- 実用的で役立つ情報を提供する
- 読者の興味を引く内容にする

【出力フォーマット】
1行目: タイトル: [記事のタイトル]
2行目以降: [HTML形式の本文]
"""
            
            # ユーザープロンプトを構築
            if latest_news:
                user_prompt = f"""以下の最新AIニュースを基に、上記の条件を守って記事を書いてください：

【最新ニュース情報】
{latest_news}

【重要な指示】
- 上記の最新ニュースの中から、最も興味深いトピックを1つ選んで詳しく解説してください
- 他の記事と重複しないよう、ユニークな視点や切り口で書いてください
- 具体的な日付や最新の情報を含めて、「今日の最新情報」であることを明確にしてください
- AIツールの比較や評価を含めてください（該当する場合）
- 最新機能や新機能について詳しく解説してください
- 実用的な活用方法や使用例を含めてください
- 読者が「このツールを試してみたい」「比較して選びたい」と思える内容にしてください

記事を執筆してください。"""
            else:
                # 使用済みトピックを避ける
                available_topics = [t for t in self.ai_topics if t not in used_topics]
                if available_topics:
                    fallback_topic = random.choice(available_topics)
                    used_topics.add(fallback_topic)
                
                user_prompt = f"""以下のトピックについて、上記の条件を守って記事を書いてください：

トピック: {fallback_topic}

【重要な指示】
- このトピックに関連する最新のAI技術やサービスについて詳しく解説してください
- 他の記事と重複しないよう、ユニークな視点や切り口で書いてください
- 2024年12月時点の最新情報を含めてください
- AIツールの比較や評価を含めてください（該当する場合）
- 最新機能や新機能について詳しく解説してください
- 実用的な活用方法や使用例を含めてください
- 読者が興味を持つような内容（比較、実用例、メリット・デメリットなど）を含めてください

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
                    max_tokens=4500  # 4000〜5000字に対応
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
                        if not title and i == 0:
                            title = line.strip()
                        else:
                            content_lines.append(line)
                    else:
                        content_lines.append(line)
                
                if not title:
                    title = fallback_topic if not latest_news else "最新AI技術の動向"
                
                # 本文を結合
                content = '\n'.join(content_lines).strip()
                
                if not content:
                    content = article_text
                    if title == fallback_topic:
                        first_line = article_text.split('\n')[0]
                        if len(first_line) < 100:
                            title = first_line.strip()
                            content = '\n'.join(article_text.split('\n')[1:]).strip()
                
                # 重複チェック（厳密版）
                print(f"\n重複チェック中: {title}")
                if self._is_duplicate(title, content):
                    print(f"⚠️ 重複する記事が検出されました: {title}")
                    if attempt < max_retries - 1:
                        print(f"別のトピックで再生成します... ({attempt + 1}/{max_retries})")
                        # 別のトピックを選択
                        fallback_topic = random.choice(self.ai_topics)
                        continue
                    else:
                        print("⚠️ 最大リトライ回数に達しました。")
                        print("⚠️ このまま投稿すると重複の可能性がありますが、続行します。")
                
                print(f"✓ 重複なし: 新しい記事として認識されました")
                
                if not content.startswith('<'):
                    paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
                    content = '\n\n'.join([f'<p>{p}</p>' for p in paragraphs])
                
                plain_text = re.sub(r'<[^>]+>', '', content)
                plain_text_length = len(plain_text.strip())
                print(f"生成された記事の文字数: {plain_text_length}文字")
                
                if plain_text_length < 4500:
                    needed_length = max(5000 - plain_text_length, 800)
                    additional_prompt = f"""上記の記事の続きとして、さらに約{needed_length}字以上の内容を追加してください。
同じテーマで、以下の点を含めてください：
- 追加のAI技術情報や最新動向
- 実用的な活用方法や使用例（ステップバイステップで）
- 他のAIツールとの比較や評価
- 読者が実際に試せる具体的なアドバイス
- 今後の展望やトレンド
- さらなる実用的なヒントとコツ

HTML形式（<p>タグ、<h2>タグ、<strong>タグを使用）で出力してください。"""
                    
                    additional_response = self.client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": f"既存の記事:\n{content}\n\n{additional_prompt}"}
                        ],
                        temperature=0.8,
                        max_tokens=2000  # 追加コンテンツを増やす
                    )
                    
                    additional_content = additional_response.choices[0].message.content.strip()
                    if not additional_content.startswith('<'):
                        paragraphs = [p.strip() for p in additional_content.split('\n\n') if p.strip()]
                        additional_content = '\n\n'.join([f'<p>{p}</p>' for p in paragraphs])
                    
                    content += '\n\n' + additional_content
                
                # 画像を生成
                result = {
                    'title': title,
                    'content': content
                }
                
                # 画像生成のデバッグ情報を表示
                print(f"\n{'='*60}")
                print("画像生成設定の確認")
                print(f"{'='*60}")
                print(f"画像生成: {'有効' if generate_image else '無効'}")
                print(f"画像ソース: {self.image_source}")
                if self.image_source == 'unsplash':
                    print(f"Unsplash APIキー: {'設定済み' if self.unsplash_access_key else '未設定'}")
                print(f"{'='*60}\n")
                
                if generate_image:
                    print("画像生成を開始します...")
                    image_theme = latest_news[:100] if latest_news else fallback_topic
                    image_result = self.generate_image(image_theme, title)
                    if image_result:
                        image_url, image_path = image_result
                        result['image_url'] = image_url
                        result['image_path'] = image_path
                        print(f"✓ 画像が正常に生成されました")
                        print(f"  画像URL: {image_url}")
                        print(f"  画像パス: {image_path}")
                    else:
                        print("⚠️ 画像生成に失敗しましたが、記事は正常に生成されました")
                        print("  画像生成をスキップして記事のみ投稿します")
                else:
                    image_theme = fallback_topic
                
                # 投稿履歴に保存（内容の一部も保存して重複チェックを強化）
                history = self._load_post_history()
                content_preview = re.sub(r'<[^>]+>', '', content)[:200]  # 最初の200文字
                history.append({
                    'title': title,
                    'date': datetime.now().isoformat(),
                    'theme': image_theme,
                    'content_preview': content_preview
                })
                self._save_post_history(history)
                print(f"✓ 投稿履歴に保存しました: {title}")
                print(f"✓ 履歴件数: {len(history)}件（過去30日間）")
                
                return result
                
            except Exception as e:
                error_msg = str(e)
                print(f"記事生成エラー: {error_msg}")
            
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


def generate_article(image_source: str = 'banana', generate_image: bool = True):
    """
    記事生成関数（外部から呼び出し可能）
    毎日、最新のAI技術に関する実用的でユニークな4000〜5000字の記事を生成
    Banana Pro Nanoで美しい画像を自動生成
    
    Args:
        image_source: 画像生成のソース ('banana'/'nano', 'unsplash', 'dalle')
        generate_image: 画像を生成するかどうか
    
    Returns:
        dict: {'title': str, 'content': str, 'image_path': str (optional), 'image_url': str (optional)}
    """
    print(f"\n{'='*60}")
    print(f"📰 最新AI記事生成開始")
    print(f"{'='*60}")
    print(f"🖼️  画像ソース: {image_source}")
    print(f"📷 画像生成: {'有効' if generate_image else '無効'}")
    print(f"📝 目標文字数: 4000〜5000字")
    print(f"{'='*60}\n")
    
    generator = ArticleGenerator(image_source=image_source)
    return generator.generate_article(generate_image=generate_image)


if __name__ == "__main__":
    # 環境変数から画像ソースを取得（デフォルトはbanana）
    image_source = os.getenv('IMAGE_SOURCE', 'banana')
    
    print(f"\n{'='*60}")
    print("🚀 AI記事生成テスト実行")
    print(f"{'='*60}\n")
    
    generator = ArticleGenerator(image_source=image_source)
    article = generator.generate_article()
    
    print("\n" + "="*60)
    print("✅ 生成された記事")
    print("="*60)
    print(f"\n📝 タイトル: {article['title']}\n")
    print(f"📊 本文の長さ: {len(article['content'])}文字\n")
    print(f"本文プレビュー:\n{article['content'][:500]}...\n")
    if 'image_path' in article:
        print(f"🖼️  画像パス: {article['image_path']}")
        print(f"🔗 画像URL: {article.get('image_url', 'N/A')}")
    print("="*60)
