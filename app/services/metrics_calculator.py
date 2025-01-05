from typing import Dict, Any, List
from datetime import datetime, timedelta
import numpy as np

class MetricsCalculator:
    def calculate_engagement(self, platform_data: Dict[str, Any]) -> Dict[str, float]:
        total_engagement = 0
        platform_breakdown = {}
        
        for platform, data in platform_data.items():
            platform_engagement = self._calculate_platform_engagement(platform, data)
            platform_breakdown[platform] = platform_engagement
            total_engagement += platform_engagement['total']

        week_ago = (datetime.utcnow() - timedelta(days=7)).timestamp()
        activity_growth = self._calculate_activity_growth(platform_data, week_ago)

        return {
            'total_engagement_rate': total_engagement,
            'activity_growth': activity_growth,
            'platform_breakdown': platform_breakdown
        }

    def analyze_community(self, platform_data: Dict[str, Any]) -> Dict[str, Any]:
        total_followers = 0
        active_members = 0
        activity_distribution = {}
        
        for platform, data in platform_data.items():
            platform_stats = self._calculate_platform_community_stats(platform, data)
            total_followers += platform_stats['followers']
            active_members += platform_stats['active_members']
            activity_distribution[platform] = platform_stats['activity_pattern']

        growth_rate = self._calculate_growth_rate(platform_data)

        return {
            'total_followers': total_followers,
            'active_members': active_members,
            'growth_rate': growth_rate,
            'activity_distribution': activity_distribution
        }

    def _calculate_platform_engagement(self, platform: str, data: Dict[str, Any]) -> Dict[str, float]:
        if platform == 'twitter':
            return self._calculate_twitter_engagement(data)
        elif platform == 'reddit':
            return self._calculate_reddit_engagement(data)
        # Add other platforms as needed
        return {'total': 0.0}

    def _calculate_twitter_engagement(self, data: Dict[str, Any]) -> Dict[str, float]:
        engagement_metrics = {'total': 0.0, 'likes': 0, 'retweets': 0, 'replies': 0}
        
        for tweet in data['recent_activity']:
            metrics = tweet['public_metrics']
            engagement_metrics['likes'] += metrics['favorite_count']
            engagement_metrics['retweets'] += metrics['retweet_count']
            engagement_metrics['replies'] += metrics['reply_count']
        
        engagement_metrics['total'] = sum(
            engagement_metrics[key] for key in ['likes', 'retweets', 'replies']
        )
        
        return engagement_metrics

    def _calculate_activity_growth(self, platform_data: Dict[str, Any], week_ago: float) -> float:
        total_activity_last_week = 0
        total_activity_current_week = 0
        
        for platform, data in platform_data.items():
            # Assuming 'recent_activity' contains timestamps and some activity metric
            for activity in data.get('recent_activity', []):
                activity_time = activity.get('created_at')
                if activity_time:
                    # Parse the date string using strptime
                    try:
                        activity_timestamp = datetime.strptime(activity_time, '%a %b %d %H:%M:%S %z %Y').timestamp()
                        if activity_timestamp < week_ago:
                            total_activity_last_week += 1  # Count activity from last week
                        else:
                            total_activity_current_week += 1  # Count current week activity
                    except ValueError as e:
                        print(f"Error parsing date: {e}")  # Handle parsing errors

        # Calculate growth rate
        if total_activity_last_week == 0:
            return total_activity_current_week  # If no activity last week, return current week activity
        return (total_activity_current_week - total_activity_last_week) / total_activity_last_week

    def _calculate_platform_community_stats(self, platform: str, data: Dict[str, Any]) -> Dict[str, Any]:
        if platform == 'twitter':
            followers_count = int(data.get('profile', {}).get('followers_count', 0))
            active_members = len(data.get('recent_activity', []))  # Count of recent activities as active members
            activity_pattern = self._analyze_activity_pattern(data.get('recent_activity', []))
            
            return {
                'followers': followers_count,
                'active_members': active_members,
                'activity_pattern': activity_pattern
            }
        elif platform == 'reddit':
            community_info = data.get('community_info', {})
            followers_count = community_info.get('subscribers', 0)
            active_members = community_info.get('active_users', 0)
            activity_pattern = self._analyze_activity_pattern(data.get('recent_activity', []))
            
            return {
                'followers': followers_count,
                'active_members': active_members,
                'activity_pattern': activity_pattern
            }
        # Add other platforms as needed
        return {'followers': 0, 'active_members': 0, 'activity_pattern': []}

    def _analyze_activity_pattern(self, recent_activity: List[Dict[str, Any]]) -> List[str]:
        # Analyze the activity pattern based on timestamps or content
        activity_pattern = []
        for activity in recent_activity:
            activity_time = activity.get('created_at')
            if activity_time:
                activity_pattern.append(activity_time)  # You can customize this to analyze patterns
        return activity_pattern

    def _calculate_growth_rate(self, platform_data: Dict[str, Any]) -> float:
        total_growth = 0
        total_followers = 0
        
        for platform, data in platform_data.items():
            if platform == 'twitter':
                followers_count = int(data.get('profile', {}).get('followers_count', 0))
                total_followers += followers_count
                # Assuming you have a way to get the followers count from a week ago
                followers_count_last_week = self._get_followers_count_last_week(platform, data)
                total_growth += (followers_count - followers_count_last_week)

            elif platform == 'reddit':
                community_info = data.get('community_info', {})
                followers_count = community_info.get('subscribers', 0)
                total_followers += followers_count
                # Assuming you have a way to get the subscribers count from a week ago
                subscribers_count_last_week = self._get_subscribers_count_last_week(platform, data)
                total_growth += (followers_count - subscribers_count_last_week)

        # Calculate growth rate
        if total_followers == 0:
            return 0.0  # Avoid division by zero
        return total_growth / total_followers

    def _get_followers_count_last_week(self, platform: str, data: Dict[str, Any]) -> int:
        # Placeholder for logic to retrieve followers count from a week ago
        # This could involve storing historical data or querying an API
        return 0  # Replace with actual logic

    def _get_subscribers_count_last_week(self, platform: str, data: Dict[str, Any]) -> int:
        # Placeholder for logic to retrieve subscribers count from a week ago
        return 0  # Replace with actual logic

    # Add other platform-specific calculation methods... 