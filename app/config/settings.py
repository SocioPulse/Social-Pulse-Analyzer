from typing import Dict
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Twitter API
    TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
    TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
    TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
    TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
    TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

    # Reddit API
    REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
    REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
    REDDIT_USER_AGENT = "SocioPulse/1.0"

    # Discord API
    DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

    # Telegram API
    TELEGRAM_API_ID = os.getenv("TELEGRAM_API_ID")
    TELEGRAM_API_HASH = os.getenv("TELEGRAM_API_HASH")
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
settings = Settings() 