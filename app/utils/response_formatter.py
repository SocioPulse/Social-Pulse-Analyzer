from typing import Dict, Any
from services.social_pulse_analyzer import AnalysisResult

def format_analysis_response(analysis: AnalysisResult) -> Dict[str, Any]:
    return {
        'overview': {
            'sentiment_score': {
                'value': analysis.sentiment_score,
                'interpretation': interpret_sentiment(analysis.sentiment_score)
            },
            'community_health_score': calculate_health_score(analysis)
        },
        'engagement_metrics': {
            'total_engagement_rate': analysis.engagement_metrics['total_engagement_rate'],
            'activity_growth': analysis.engagement_metrics['activity_growth'],
            'platform_breakdown': analysis.engagement_metrics['platform_breakdown']
        },
        'community_insights': {
            'total_followers': analysis.community_stats['total_followers'],
            'active_members': analysis.community_stats['active_members'],
            'growth_rate': analysis.community_stats['growth_rate'],
            'activity_distribution': analysis.community_stats['activity_distribution']
        },
        'content_analysis': {
            'trending_topics': analysis.trending_topics,
            #'key_discussions': extract_key_discussions(analysis),
            #'sentiment_distribution': analysis.detailed_analysis['sentiment_distribution']
        },
        'risk_assessment': {
            'identified_risks': analysis.risk_factors,
            'risk_level': calculate_risk_level(analysis)
        },
        #'detailed_metrics': analysis.detailed_analysis
    } 

def interpret_sentiment(score: float) -> str:
    """
    Interprets the sentiment score into a human-readable format.
    
    Args:
        score (float): The sentiment score, typically between -1 and 1.
        
    Returns:
        str: Interpretation of the sentiment score.
    """
    if score > 0.1:
        return "Positive sentiment"
    elif score < -0.1:
        return "Negative sentiment"
    else:
        return "Neutral sentiment" 

def calculate_health_score(analysis: AnalysisResult) -> float:
    """
    Calculates a community health score based on engagement metrics and community stats.
    
    Args:
        analysis (AnalysisResult): The analysis result containing engagement and community stats.
        
    Returns:
        float: A score representing the health of the community.
    """
    engagement_score = analysis.engagement_metrics.get('total_engagement_rate', 0)
    follower_count = analysis.community_stats.get('total_followers', 0)
    active_members = analysis.community_stats.get('active_members', 0)

    # Simple formula for health score
    health_score = (engagement_score * 0.5) + (follower_count * 0.3) + (active_members * 0.2)

    # Normalize the score to a scale of 0 to 100
    return min(max(health_score, 0), 100) 

def extract_key_discussions(analysis: AnalysisResult) -> Dict[str, Any]:
    """
    Extracts key discussions from the analysis result based on engagement and sentiment.

    Args:
        analysis (AnalysisResult): The analysis result containing discussions.

    Returns:
        Dict[str, Any]: A dictionary of key discussions.
    """
    print("extract_key_discussions")
    key_discussions = []

    # Assuming detailed_analysis contains discussions with their metrics
    print(analysis)
    discussions = analysis.detailed_analysis.get('discussions', [])
    
    for discussion in discussions:
        sentiment = discussion.get('sentiment_score', 0)
        engagement = discussion.get('engagement_score', 0)

        # Define criteria for key discussions
        if sentiment > 0.1 and engagement > 50:  # Example thresholds
            key_discussions.append({
                'title': discussion.get('title', 'No Title'),
                'sentiment_score': sentiment,
                'engagement_score': engagement,
                'content': discussion.get('content', '')
            })

    return key_discussions 

def calculate_risk_level(analysis: AnalysisResult) -> str:
    """
    Calculates the risk level based on community health and engagement metrics.

    Args:
        analysis (AnalysisResult): The analysis result containing engagement and community stats.

    Returns:
        str: The risk level as a string.
    """
    print("calculate_risk_level",calculate_risk_level)
    print("engagement_score")
    engagement_score = analysis.engagement_metrics.get('total_engagement_rate', 0)
    print("total_followers")
    total_followers = analysis.community_stats.get('total_followers', 0)
    print("active_members")
    active_members = analysis.community_stats.get('active_members', 0)
    print("sentiment_score")
    sentiment_score = analysis.sentiment_score

    # Define risk levels based on thresholds
    if total_followers < 1000:
        return "High Risk: Small community size"
    elif engagement_score < 20:
        return "Medium Risk: Low engagement"
    elif sentiment_score < -0.1:
        return "High Risk: Negative sentiment"
    elif active_members / total_followers < 0.05:  # Less than 5% active members
        return "Medium Risk: Low community activity"
    else:
        return "Low Risk: Healthy community" 