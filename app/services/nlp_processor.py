from typing import Dict, List, Any
import numpy as np
from transformers import pipeline
from collections import Counter
from textblob import TextBlob
import yake

class NLPProcessor:
    def __init__(self):
        self.sentiment_analyzer = pipeline("sentiment-analysis")
        self.keyword_extractor = yake.KeywordExtractor(
            lan="en",
            n=2,
            dedupLim=0.9,
            top=20,
            features=None
        )

    def analyze_sentiment(self, platform_data: Dict[str, Any], direct_text=False) -> float:
        if direct_text:
            all_texts = [platform_data]
        else:
            all_texts = self._extract_texts(platform_data)
        sentiments = []
        
        for text in all_texts:
            if not text.strip():
                continue
                
            # Use TextBlob for faster processing of large amounts of text
            blob_sentiment = TextBlob(text).sentiment.polarity
            
            # Use transformers for more accurate but slower analysis of important text
            if len(text.split()) < 100:  # Only for shorter texts
                try:
                    transformer_result = self.sentiment_analyzer(text[:512])[0]
                    transformer_score = 1 if transformer_result['label'] == 'POSITIVE' else -1
                    transformer_score *= transformer_result['score']
                    
                    # Combine both scores with more weight on transformer
                    sentiment = (transformer_score * 0.7) + (blob_sentiment * 0.3)
                except:
                    sentiment = blob_sentiment
            else:
                sentiment = blob_sentiment
                
            sentiments.append(sentiment)
            
        return np.mean(sentiments) if sentiments else 0.0

    def extract_trending_topics(self, platform_data: Dict[str, Any]) -> List[str]:
        all_texts = self._extract_texts(platform_data)
        combined_text = " ".join(all_texts)
        
        # Extract keywords using YAKE
        keywords = self.keyword_extractor.extract_keywords(combined_text)
        
        # Sort by score (lower is better in YAKE) and get top 10
        sorted_keywords = sorted(keywords, key=lambda x: x[1])[:10]
        
        return [keyword[0] for keyword in sorted_keywords]

    def _extract_texts(self, platform_data: Dict[str, Any]) -> List[str]:
        texts = []
        
        for platform, data in platform_data.items():
            if platform == 'twitter':
                texts.extend(tweet['text'] for tweet in data['recent_activity'])
            elif platform == 'reddit':
                for post in data['recent_activity']:
                    texts.append(post['title'])
                    texts.append(post['text'])
            # Add other platforms as needed
            
        return texts 