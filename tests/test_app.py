import json
import requests

class TestSocialPulseAnalyzerAPI():
    def __init__(self) -> None:
        self.client = requests.Session()

    def setUp(self):
        self.app.config['TESTING'] = True

    def test_analyze_with_contract_address(self):
        # Test with a valid contract address
        response = self.client.post('http://127.0.0.1:5000/api/analyze', 
                                     json={"contract_address": "45ZAM7JK8ZGHuBQiJ8kvhdiVdiQGsTQGgt3gRAEQpump"},
                                     )
        print(response.text)
        try:
            data = json.loads(response.data)
            print(data)
        except:
            pass

    def test_analyze_with_social_handles(self):
        # Test with valid social handles
        response = self.client.post('http://127.0.0.1:5000/api/analyze', 
                                     data=json.dumps({"social_handles": {"twitter": "MagicEden"}}),
                                     content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('status', data)
        self.assertEqual(data['status'], 'success')

    def test_analyze_with_missing_data(self):
        # Test with missing data
        response = self.client.post('http://127.0.0.1:5000/api/analyze', 
                                     data=json.dumps({}),  # Empty payload
                                     content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('status', data)
        self.assertEqual(data['status'], 'error')

    def test_analyze_with_invalid_data(self):
        # Test with invalid data
        response = self.client.post('http://127.0.0.1:5000/api/analyze', 
                                     data=json.dumps({"contract_address": ""}),  # Invalid contract address
                                     content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('status', data)
        self.assertEqual(data['status'], 'error')

if __name__ == '__main__':
    tester = TestSocialPulseAnalyzerAPI()
    tester.test_analyze_with_contract_address()