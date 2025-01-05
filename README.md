# Social-Pulse-Analyzer

<div align="center">
  <img src="https://github.com/user-attachments/assets/2be45bf1-3c7b-4dd1-a313-42d2fc216da4" alt="Social Pulse Analyzer">
</div>

## Overview

Social Pulse Analyzer is a powerful tool designed to analyze social media engagement and sentiment across various platforms. Currently, it supports Twitter, with plans to expand to Telegram, Discord, and Reddit. The application leverages Natural Language Processing (NLP) techniques to provide insights into community health, engagement metrics, and risk factors associated with social media accounts.

## Special Feature

Social Pulse Analyzer currently supports extracting Twitter data from pump.fun by providing:
- **A Solana Token Address.**
- **A Twitter Profile URL directly.**

This allows seamless integration for analyzing social media activity linked to specific blockchain projects or individual Twitter accounts.

## Features

- **Engagement Metrics**: Calculate total engagement rates, activity growth, and platform breakdowns.
- **Sentiment Analysis**: Analyze sentiment scores and interpret them into human-readable formats.
- **Community Insights**: Gather insights on total followers, active members, and growth rates.
- **Risk Assessment**: Identify potential risks based on community health and engagement metrics.
- **Trending Topics**: Extract trending topics from social media discussions.

## Demo Output

Here’s an example of the output generated by the Social Pulse Analyzer:
```json
{
  "data": {
    "community_insights": {
      "active_members": 21,
      "activity_distribution": {
        "twitter": [
          "Tue Dec 10 14:02:42 +0000 2024",
          "Sun Jan 05 15:09:20 +0000 2025",
          "Fri Jan 03 16:00:52 +0000 2025",
          "Fri Jan 03 14:16:31 +0000 2025",
          "Thu Jan 02 19:00:16 +0000 2025",
          "Thu Jan 02 18:59:59 +0000 2025",
          "Thu Jan 02 15:02:15 +0000 2025",
          "Wed Jan 01 16:57:10 +0000 2025",
          "Wed Jan 01 16:56:59 +0000 2025",
          "Wed Jan 01 16:06:18 +0000 2025",
          "Wed Jan 01 14:02:19 +0000 2025",
          "Tue Dec 31 17:58:12 +0000 2024",
          "Tue Dec 31 15:24:59 +0000 2024",
          "Mon Dec 30 20:12:51 +0000 2024",
          "Mon Dec 30 19:37:30 +0000 2024",
          "Mon Dec 30 18:00:34 +0000 2024",
          "Mon Dec 30 14:05:28 +0000 2024",
          "Sat Dec 28 18:31:14 +0000 2024",
          "Sat Dec 28 17:02:14 +0000 2024",
          "Fri Dec 27 18:20:27 +0000 2024",
          "Fri Dec 27 14:18:30 +0000 2024"
        ]
      },
      "growth_rate": 1.0,
      "total_followers": 760135
    },
    "content_analysis": {
      "trending_topics": [
        "Magic Eden",
        "Magic",
        "Eden",
        "Eden app",
        "January",
        "app",
        "MagicEden",
        "Bitcoin",
        "NFT marketplace",
        "day"
      ]
    },
    "engagement_metrics": {
      "activity_growth": 2.2,
      "platform_breakdown": {
        "twitter": {
          "likes": 23527,
          "replies": 12559,
          "retweets": 4625,
          "total": 40711
        }
      },
      "total_engagement_rate": 40711
    },
    "overview": {
      "community_health_score": 100,
      "sentiment_score": {
        "interpretation": "Negative sentiment",
        "value": -0.137729727994828
      }
    },
    "risk_assessment": [
        "Low content creation frequency in the past week"
      ],
      "risk_level": "High Risk: Negative sentiment"
    }
  },
  "status": "success"
```

## Current Status

- **Platforms Under Development**: Currently, only Twitter is fully developed. Support for Telegram, Discord, and Reddit is in progress.
- **Data Retrieval**: Implementing a method to retrieve followers count from the previous week.
- **NLP Model Optimization**: Enhancing the NLP model for better accuracy and performance.
- **Risk Factor Optimization**: Improving the risk assessment algorithms for more reliable insights.

## Future Work

1. **Expand Platform Support**: Integrate additional social media platforms (Telegram, Discord, Reddit).
2. **Historical Data Analysis**: Develop methods to analyze historical engagement and sentiment data.
3. **User Interface**: Create a user-friendly web interface for easier interaction with the analyzer.
4. **Real-time Monitoring**: Implement real-time monitoring of social media accounts for ongoing analysis.
5. **Customizable Alerts**: Allow users to set alerts for specific engagement or sentiment thresholds.
6. **Data Visualization**: Incorporate data visualization tools to present insights in a more digestible format.

## Installation

To get started with Social Pulse Analyzer, clone the repository and install the required dependencies:
```bash
git clone https://github.com/yourusername/social-pulse-analyzer.git
cd social-pulse-analyzer
pip install -r requirements.txt
```

## Usage

Run the application using:
```bash
python app/init.py
```

You can then access the API at `http://127.0.0.1:5000/api/analyze`.


## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Flask](https://flask.palletsprojects.com/) for the web framework.
- [Transformers](https://huggingface.co/transformers/) for NLP capabilities.
- [scikit-learn](https://scikit-learn.org/stable/) for machine learning tools.

---
