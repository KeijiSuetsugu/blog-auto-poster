
import os
import sys
from dotenv import load_dotenv
from article_generator import ArticleGenerator

# Load env vars
load_dotenv()

def test_news_fetching():
    print("\n--- Testing News Fetching ---")
    try:
        generator = ArticleGenerator(debug=True)
        print(f"NewsAPI Key present: {bool(generator.newsapi_key)}")
        
        news = generator._get_latest_ai_news()
        if news:
            print("News fetched successfully:")
            print(news[:200] + "...")
        else:
            print("Failed to fetch news.")
    except Exception as e:
        print(f"Error in news fetching: {e}")

def test_image_generation():
    print("\n--- Testing Image Generation ---")
    try:
        generator = ArticleGenerator(debug=True)
        print(f"Image Source: {generator.image_source}")
        print(f"Unsplash Key present: {bool(generator.unsplash_access_key)}")
        
        # Test with a generic keyword that might cause "same image" if logic is flawed
        theme = "Latest AI News"
        print(f"Generating image for theme: '{theme}'")
        
        # Generate twice to see if we get different URLs
        result1 = generator.generate_image(theme, "Test Title 1")
        if result1:
            print(f"Image 1 URL: {result1[0]}")
        else:
            print("Image 1 generation failed.")
            
        result2 = generator.generate_image(theme, "Test Title 2")
        if result2:
            print(f"Image 2 URL: {result2[0]}")
        else:
            print("Image 2 generation failed.")
            
        if result1 and result2 and result1[0] == result2[0]:
            print("WARNING: Generated images have the SAME URL!")
        else:
            print("Generated images have different URLs.")
            
    except Exception as e:
        print(f"Error in image generation: {e}")

if __name__ == "__main__":
    test_news_fetching()
    test_image_generation()
