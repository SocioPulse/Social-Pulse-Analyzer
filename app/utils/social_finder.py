from typing import Dict, Optional
import requests
from bs4 import BeautifulSoup
import re
from config.settings import settings

class SocialFinder:
    def __init__(self):
        self.solscan_api = "https://api.solscan.io/account"
        self.known_platforms = {
            'x.com': 'twitter',
            #'t.me': 'telegram',
            #'discord.gg': 'discord',
            'reddit.com/r/': 'reddit'
        }

    def find_socials(self, contract_address: str) -> Dict[str, str]:
        social_handles = {}
        
        # First try to get metadata from Solscan
        token_info = self._get_token_info(contract_address)
        print(token_info)
        if token_info:
            social_handles.update(self._extract_socials_from_metadata(token_info))

        # If website is available, scrape it for social links
        if 'website' in token_info:
            website_socials = self._scrape_website_for_socials(token_info['website'])
            social_handles.update(website_socials)

        return social_handles

    def _get_token_info(self, contract_address: str) -> Optional[Dict]:
        try:
            response = requests.get("https://pump.fun/coin/FrRNaCckVKtXLT67NjXSLRwNjeMnvsa6Tdar412Cpump")
            file_content = response.text

            def find_json_part_with_escapes(content):
                found = []
                patterns = [r'\\"twitter\\":\\\"https://x\.com/[^\\]+\\",', r'\\"telegram\\":\\\"https://t\.me/[^\\]+\\",']
                for pattern in patterns:
                    match = re.search(pattern, content)
                    if match:
                        found.append(match.group(0))
                return found

            escaped_match_result = find_json_part_with_escapes(file_content)
            formatted_data = {}
            for item in escaped_match_result:
                key_value = item.replace('\\', '').strip(',').split('":"')
                key = key_value[0].strip('"')
                value = key_value[1].strip('"')
                formatted_data[key] = value

            return formatted_data if formatted_data else None
        except Exception as e:
            print(f"Error fetching token info: {e}")
            return None

    def _extract_socials_from_metadata(self, token_info: Dict) -> Dict[str, str]:
        socials = {}
        
        # Extract from token metadata
        metadata = token_info
        for key, value in metadata.items():
            if isinstance(value, str):
                platform = self._identify_platform(value)
                if platform:
                    socials[platform] = self._extract_handle(platform, value)

        return socials

    def _scrape_website_for_socials(self, website_url: str) -> Dict[str, str]:
        socials = {}
        try:
            response = requests.get(
                website_url,
                headers={'User-Agent': 'SocioPulse/1.0'},
                timeout=10
            )
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find social links in anchor tags
            for link in soup.find_all('a', href=True):
                href = link['href']
                platform = self._identify_platform(href)
                if platform:
                    socials[platform] = self._extract_handle(platform, href)

        except Exception as e:
            print(f"Error scraping website: {e}")

        return socials

    def _identify_platform(self, url: str) -> Optional[str]:
        for domain, platform in self.known_platforms.items():
            if domain in url.lower():
                return platform
        return None

    def _extract_handle(self, platform: str, url: str) -> str:
        if platform == 'twitter':
            match = re.search(r'twitter\.com/([^/\?]+)', url)
            return match.group(1) if match else url
        elif platform == 'telegram':
            match = re.search(r't\.me/([^/\?]+)', url)
            return match.group(1) if match else url
        elif platform == 'discord':
            match = re.search(r'discord\.gg/([^/\?]+)', url)
            return match.group(1) if match else url
        elif platform == 'reddit':
            match = re.search(r'reddit\.com/r/([^/\?]+)', url)
            return match.group(1) if match else url
        return url 