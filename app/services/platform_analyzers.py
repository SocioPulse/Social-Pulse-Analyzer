from abc import ABC, abstractmethod
from typing import Dict, Any
import tweepy
import praw
import discord
import telethon
import requests
import json
from datetime import datetime, timedelta
from config import settings

class PlatformAnalyzer(ABC):
    @abstractmethod
    def collect_data(self, handle: str) -> Dict[str, Any]:
        pass

    def _calculate_time_window(self) -> tuple:
        now = datetime.utcnow()
        week_ago = now - timedelta(days=7)
        return week_ago, now

class TwitterAnalyzer(PlatformAnalyzer):
    def __init__(self):
        self.client = tweepy.Client(
            bearer_token="YOUR_BEARER_TOKEN",
            consumer_key="YOUR_API_KEY",
            consumer_secret="YOUR_API_SECRET",
            access_token="YOUR_ACCESS_TOKEN",
            access_token_secret="YOUR_ACCESS_TOKEN_SECRET"
        )

    def collect_data(self, handle: str) -> Dict[str, Any]:
        print("handle",handle)
        username = handle.split("/")[-1]
        username = "MagicEden"
        print("username",username)
        url = f"https://syndication.twitter.com/srv/timeline-profile/screen-name/{username}"

        r = requests.get(url)

        html = r.text

        start_str = '<script id="__NEXT_DATA__" type="application/json">'
        end_str = '</script></body></html>'

        start_index = html.index(start_str) + len(start_str)
        end_index = html.index(end_str, start_index)

        json_str = html[start_index: end_index]
        data = json.loads(json_str)
        print(data)

        user_data = data.get('props', {}).get('pageProps', {}).get('user', {})
        timeline_entries = data.get('props', {}).get('pageProps', {}).get('timeline', {}).get('entries', [])
        try:
            extract_follower = int(str(data).split("normal_followers_count': ")[-1].split(",")[0])
        except Exception:
            print("Invalid or too small account")
            return {
                'profile': {
                    'followers_count': 0,
                    'following_count': 0,
                    'tweet_count': 0
                },
                'recent_activity': [],
            }    
        return {
            'profile': {
                'followers_count': int(str(data).split("normal_followers_count': ")[-1].split(",")[0]),
                'following_count': int(str(data).split("friends_count': ")[-1].split(",")[0]),
                'tweet_count': int(str(data).split("statuses_count': ")[-1].split(",")[0])
            },
            'recent_activity': [
                {
                    'text': entry.get('content', {}).get('tweet', {}).get('text', ''),
                    'created_at': entry.get('content', {}).get('tweet', {}).get('created_at', ''),
                    'public_metrics': {
                        'favorite_count': entry.get('content', {}).get('tweet', {}).get('favorite_count', 0),
                        'retweet_count': entry.get('content', {}).get('tweet', {}).get('retweet_count', 0),
                        'reply_count': entry.get('content', {}).get('tweet', {}).get('reply_count', 0),
                        'quote_count': entry.get('content', {}).get('tweet', {}).get('quote_count', 0),
                    },
                }
                for entry in timeline_entries if entry.get('type') == 'tweet'
            ],
        }

class RedditAnalyzer(PlatformAnalyzer):
    def __init__(self):
        self.reddit = praw.Reddit(
            client_id="YOUR_CLIENT_ID",
            client_secret="YOUR_CLIENT_SECRET",
            user_agent="SocioPulse/1.0"
        )

    def collect_data(self, subreddit_name: str) -> Dict[str, Any]:
        subreddit = self.reddit.subreddit(subreddit_name)
        week_ago, _ = self._calculate_time_window()

        posts = list(subreddit.new(limit=100))
        
        return {
            'community_info': {
                'subscribers': subreddit.subscribers,
                'active_users': subreddit.active_user_count,
                'created_utc': subreddit.created_utc
            },
            'recent_activity': [
                {
                    'title': post.title,
                    'text': post.selftext,
                    'score': post.score,
                    'num_comments': post.num_comments,
                    'created_utc': post.created_utc
                }
                for post in posts
                if post.created_utc > week_ago.timestamp()
            ]
        } 

class DiscordAnalyzer(PlatformAnalyzer):
    def __init__(self):
        self.client = discord.Client()
        self.token = settings.DISCORD_BOT_TOKEN

    async def collect_data(self, server_id: str) -> Dict[str, Any]:
        week_ago, _ = self._calculate_time_window()
        
        try:
            guild = await self.client.fetch_guild(int(server_id))
            channels = await guild.fetch_channels()
            
            messages = []
            for channel in channels:
                if isinstance(channel, discord.TextChannel):
                    async for message in channel.history(limit=100, after=week_ago):
                        messages.append({
                            'content': message.content,
                            'created_at': message.created_at,
                            'reactions': len(message.reactions),
                            'author': str(message.author)
                        })

            return {
                'server_info': {
                    'member_count': guild.member_count,
                    'created_at': guild.created_at
                },
                'recent_activity': messages
            }
        except Exception as e:
            print(f"Error collecting Discord data: {e}")
            return {'server_info': {}, 'recent_activity': []}

class TelegramAnalyzer(PlatformAnalyzer):
    def __init__(self):
        self.client = telethon.TelegramClient(
            'sociopulse_bot',
            settings.TELEGRAM_API_ID,
            settings.TELEGRAM_API_HASH
        )

    async def collect_data(self, channel_name: str) -> Dict[str, Any]:
        week_ago, _ = self._calculate_time_window()
        
        try:
            await self.client.start(bot_token=settings.TELEGRAM_BOT_TOKEN)
            
            channel = await self.client.get_entity(channel_name)
            messages = []
            
            async for message in self.client.iter_messages(channel, limit=100):
                if message.date > week_ago:
                    messages.append({
                        'text': message.text,
                        'date': message.date,
                        'views': message.views,
                        'forwards': message.forwards
                    })

            participants_count = await self.client.get_participants(channel, limit=0)
            
            return {
                'channel_info': {
                    'participants_count': len(participants_count),
                    'created_at': channel.date
                },
                'recent_activity': messages
            }
        except Exception as e:
            print(f"Error collecting Telegram data: {e}")
            return {'channel_info': {}, 'recent_activity': []} 