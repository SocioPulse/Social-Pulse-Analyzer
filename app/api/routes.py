from flask import Blueprint, request, jsonify
from services.social_pulse_analyzer import SocialPulseAnalyzer
from utils.validators import validate_request
from utils.response_formatter import format_analysis_response
from http import HTTPStatus

social_pulse = Blueprint('social_pulse', __name__)

@social_pulse.route('/analyze', methods=['POST'])
def analyze_token_social():
    try:
        data = request.get_json()
        
        # Validate request payload
        validation_result = validate_request(data)
        if not validation_result['valid']:
            return jsonify({
                'status': 'error',
                'message': validation_result['message']
            }), HTTPStatus.BAD_REQUEST

        analyzer = SocialPulseAnalyzer()
        
        if 'contract_address' in data:
            result = analyzer.analyze_by_contract(data['contract_address'])
        elif 'social_handles' in data:
            result = analyzer.analyze_by_socials(data['social_handles'])
        else:
            return jsonify({
                'status': 'error',
                'message': 'Either contract_address or social_handles must be provided'
            }), HTTPStatus.BAD_REQUEST

        print("format_analysis_response")
        response = format_analysis_response(result)
        
        return jsonify({
            'status': 'success',
            'data': response
        }), HTTPStatus.OK

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), HTTPStatus.INTERNAL_SERVER_ERROR 