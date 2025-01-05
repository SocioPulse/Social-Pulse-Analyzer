from typing import Dict, Any, Union
import re

def validate_request(data: Dict[str, Any]) -> Dict[str, Union[bool, str]]:
    """
    Validates the incoming request data for the social pulse analysis.
    
    Args:
        data (Dict[str, Any]): The request payload to validate
        
    Returns:
        Dict[str, Union[bool, str]]: Validation result with 'valid' status and optional 'message'
    """
    
    # Check if data is empty
    if not data:
        return {
            'valid': False,
            'message': 'Request body cannot be empty'
        }

    # Check if at least one required field is present
    if not any(key in data for key in ['contract_address', 'social_handles']):
        return {
            'valid': False,
            'message': 'Either contract_address or social_handles must be provided'
        }

    # Validate contract address if provided
    if 'contract_address' in data:
        if not isinstance(data['contract_address'], str):
            return {
                'valid': False,
                'message': 'contract_address must be a string'
            }
        
        # Validate Solana address format (base58 string)
        if not re.match(r'^[1-9A-HJ-NP-Za-km-z]{32,44}$', data['contract_address']):
            return {
                'valid': False,
                'message': 'Invalid Solana contract address format'
            }

    # Validate social handles if provided
    if 'social_handles' in data:
        if not isinstance(data['social_handles'], dict):
            return {
                'valid': False,
                'message': 'social_handles must be an object'
            }

        # Validate supported platforms and handle formats
        valid_platforms = {'twitter', 'reddit', 'discord', 'telegram'}
        for platform, handle in data['social_handles'].items():
            # Check if platform is supported
            if platform not in valid_platforms:
                return {
                    'valid': False,
                    'message': f'Unsupported platform: {platform}'
                }

            # Check if handle is a string
            if not isinstance(handle, str):
                return {
                    'valid': False,
                    'message': f'Handle for {platform} must be a string'
                }

            # Platform-specific validations
            if platform == 'twitter':
                if not re.match(r'^[A-Za-z0-9_]{1,15}$', handle):
                    return {
                        'valid': False,
                        'message': 'Invalid Twitter handle format'
                    }
            
            elif platform == 'reddit':
                if not re.match(r'^[A-Za-z0-9][A-Za-z0-9_]{2,20}$', handle):
                    return {
                        'valid': False,
                        'message': 'Invalid Reddit subreddit name format'
                    }
            
            elif platform == 'discord':
                if not handle.isdigit():
                    return {
                        'valid': False,
                        'message': 'Discord server ID must be numeric'
                    }
            
            elif platform == 'telegram':
                if not re.match(r'^[A-Za-z0-9_]{5,32}$', handle):
                    return {
                        'valid': False,
                        'message': 'Invalid Telegram channel name format'
                    }

    # All validations passed
    return {
        'valid': True
    } 