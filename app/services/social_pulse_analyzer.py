from dataclasses import dataclass
from typing import List, Dict, Any
from services.platform_analyzers import TwitterAnalyzer, RedditAnalyzer, DiscordAnalyzer, TelegramAnalyzer
from services.nlp_processor import NLPProcessor
from services.metrics_calculator import MetricsCalculator
from utils.social_finder import SocialFinder
import numpy as np
from datetime import datetime, timedelta
from textblob import TextBlob
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

@dataclass
class AnalysisResult:
    sentiment_score: float
    engagement_metrics: Dict[str, float]
    community_stats: Dict[str, Any]
    trending_topics: List[str]
    risk_factors: List[str]
    detailed_analysis: Dict[str, Any]

class SocialPulseAnalyzer:
    def __init__(self):
        self.nlp_processor = NLPProcessor()
        self.metrics_calculator = MetricsCalculator()
        self.social_finder = SocialFinder()
        
        # Initialize platform-specific analyzers
        self.analyzers = {
            'twitter': TwitterAnalyzer(),
            'reddit': RedditAnalyzer(),
            #'discord': DiscordAnalyzer(),
            #'telegram': TelegramAnalyzer()
        }

    def analyze_by_contract(self, contract_address: str) -> AnalysisResult:
        # Find social media handles/channels associated with the contract
        social_handles = self.social_finder.find_socials(contract_address)
        print(social_handles)
        return self.analyze_by_socials(social_handles)

    def analyze_by_socials(self, social_handles: Dict[str, str]) -> AnalysisResult:
        all_platform_data = {}
        
        print("analyze_by_socials")
        print(social_handles)

        # Collect data from each platform
        for platform, handle in social_handles.items():
            if platform in self.analyzers:
                platform_data = self.analyzers[platform].collect_data(handle)
                all_platform_data[platform] = platform_data

        print("all_platform_data")
        print(all_platform_data)
        
        # Process collected data
        print("NLP")
        sentiment_score = self.nlp_processor.analyze_sentiment(all_platform_data)
        print("Engagement")
        engagement_metrics = self.metrics_calculator.calculate_engagement(all_platform_data)
        print("Community")
        community_stats = self.metrics_calculator.analyze_community(all_platform_data)
        print("Trending")
        trending_topics = self.nlp_processor.extract_trending_topics(all_platform_data)
        print("Risk")
        risk_factors = self.analyze_risk_factors(all_platform_data)
        print("Detailed")
        detailed_analysis = self.generate_detailed_analysis(all_platform_data)
        print("detailed_analysis",detailed_analysis)

        return AnalysisResult(
            sentiment_score=sentiment_score,
            engagement_metrics=engagement_metrics,
            community_stats=community_stats,
            trending_topics=trending_topics,
            risk_factors=risk_factors,
            detailed_analysis=detailed_analysis
        )

    def analyze_risk_factors(self, platform_data: Dict) -> List[str]:
        risks = []
        
        # Analyze engagement patterns
        print("Analyze engagement patterns")
        engagement_risks = self._analyze_engagement_risks(platform_data)
        risks.extend(engagement_risks)
        
        # Analyze community health
        print("Analyze community health")
        community_risks = self._analyze_community_risks(platform_data)
        risks.extend(community_risks)
        
        # Analyze content patterns
        print("Analyze content patterns")
        content_risks = self._analyze_content_risks(platform_data)
        risks.extend(content_risks)
        
        return risks

    def _analyze_engagement_risks(self, platform_data: Dict) -> List[str]:
        risks = []
        
        for platform, data in platform_data.items():
            if platform == 'twitter':
                profile = data.get('profile', {})
                followers = profile.get('followers_count', 0)
                following = profile.get('following_count', 0)
                
                # Check follower/following ratio
                if followers > 0 and following/followers > 2:
                    risks.append("Suspicious follower-to-following ratio on Twitter")
                
                # Analyze engagement consistency
                recent_engagement = [
                    tweet['public_metrics']['favorite_count'] + 
                    tweet['public_metrics']['retweet_count']
                    for tweet in data.get('recent_activity', [])
                ]
                
                if recent_engagement:
                    engagement_std = np.std(recent_engagement)
                    engagement_mean = np.mean(recent_engagement)
                    if engagement_std > engagement_mean * 3:
                        risks.append("Highly irregular engagement patterns detected")

        return risks

    def _analyze_community_risks(self, platform_data: Dict) -> List[str]:
        risks = []
        total_followers = 0
        active_ratio = 0
        
        for platform, data in platform_data.items():
            if platform == 'twitter':
                total_followers += data.get('profile', {}).get('followers_count', 0)
            elif platform == 'reddit':
                community_info = data.get('community_info', {})
                subscribers = community_info.get('subscribers', 0)
                active_users = community_info.get('active_users', 0)
                total_followers += subscribers
                
                if subscribers > 0:
                    active_ratio = active_users / subscribers
                    if active_ratio < 0.01:  # Less than 1% active users
                        risks.append(f"Low community engagement on Reddit ({active_ratio:.1%} active users)")

        # Check for minimum community size
        if total_followers < 1000:
            risks.append("Small community size may indicate early stage or low adoption")

        return risks

    def _analyze_content_risks(self, platform_data: Dict) -> List[str]:
        risks = []
        
        # Combine all text content for analysis
        all_texts = []
        for platform, data in platform_data.items():
            texts = self._extract_texts({platform: data})
            all_texts.extend(texts)
        
        if all_texts:
            # Check content frequency
            week_ago = (datetime.utcnow() - timedelta(days=7)).timestamp()
            recent_content = [
                text for text in all_texts
                if getattr(text, 'created_at', week_ago) > week_ago
            ]
            
            if len(recent_content) < 5:
                risks.append("Low content creation frequency in the past week")
            
            # Analyze sentiment volatility
            sentiments = [TextBlob(text).sentiment.polarity for text in all_texts]
            sentiment_std = np.std(sentiments)
            if sentiment_std > 0.5:
                risks.append("High sentiment volatility detected")
            
            # Check for spam patterns
            if self._detect_spam_patterns(all_texts):
                risks.append("Potential spam or artificial activity detected")
        
        return risks

    def _detect_spam_patterns(self, texts: List[str]) -> bool:
        # Implement spam detection logic
        duplicate_threshold = 0.8
        similar_content_count = 0
        
        for i, text1 in enumerate(texts):
            for text2 in texts[i+1:]:
                similarity = self._calculate_similarity(text1, text2)
                if similarity > duplicate_threshold:
                    similar_content_count += 1
        
        return similar_content_count > len(texts) * 0.1  # More than 10% similar content

    def generate_detailed_analysis(self, platform_data: Dict[str, Any]) -> Dict[str, Any]:
        discussions = []
        sentiment_scores = []
        total_engagement = 0

        for platform, data in platform_data.items():
            if platform == 'twitter':
                for tweet in data.get('recent_activity', []):
                    sentiment_score = self.nlp_processor.analyze_sentiment(tweet['text'],direct_text=True)  # Assuming you have a method to analyze sentiment
                    engagement_score = tweet['public_metrics']['favorite_count'] + tweet['public_metrics']['retweet_count']
                    
                    discussions.append({
                        'title': tweet['text'][:50],  # Use the first 50 characters as a title
                        'sentiment_score': sentiment_score,
                        'engagement_score': engagement_score,
                        'content': tweet['text']
                    })
                    sentiment_scores.append(sentiment_score)
                    total_engagement += engagement_score

            elif platform == 'reddit':
                for post in data.get('recent_activity', []):
                    sentiment_score = self.nlp_processor.analyze_sentiment(post['title'] + " " + post['selftext'],direct_text=True)  # Analyze sentiment of title and text
                    engagement_score = post['score']  # Reddit score as engagement
                    
                    discussions.append({
                        'title': post['title'],
                        'sentiment_score': sentiment_score,
                        'engagement_score': engagement_score,
                        'content': post['selftext']
                    })
                    sentiment_scores.append(sentiment_score)
                    total_engagement += engagement_score

        # Calculate sentiment distribution
        sentiment_distribution = {
            'positive': sum(1 for score in sentiment_scores if score > 0.1),
            'negative': sum(1 for score in sentiment_scores if score < -0.1),
            'neutral': sum(1 for score in sentiment_scores if -0.1 <= score <= 0.1),
        }

        # Calculate average sentiment score
        average_sentiment_score = sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0

        return {
            'discussions': discussions,
            'sentiment_distribution': sentiment_distribution,
            'total_discussions': len(discussions),
            'average_sentiment_score': average_sentiment_score,
            'total_engagement': total_engagement
        }

    def _extract_texts(self, platform_data: Dict[str, Any]) -> List[str]:
        texts = []
        
        for platform, data in platform_data.items():
            if platform == 'twitter':
                # Extract text from recent tweets
                texts.extend(tweet['text'] for tweet in data.get('recent_activity', []))
            elif platform == 'reddit':
                # Extract text from Reddit posts
                for post in data.get('recent_activity', []):
                    texts.append(post['title'])  # Add post title
                    texts.append(post['text'])    # Add post text
            # Add other platforms as needed
            # For example, if you have Discord or Telegram, extract their messages similarly

        return texts 

    def _calculate_similarity(self, text1: str, text2: str) -> float:
        vectorizer = CountVectorizer().fit_transform([text1, text2])
        vectors = vectorizer.toarray()
        cosine_sim = cosine_similarity(vectors)
        return cosine_sim[0][1] 