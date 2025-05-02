import requests
import json
import base64

class SpeedSMSAPI:
    def __init__(self, access_token):
        self.token = access_token
        self.api_url = "https://api.speedsms.vn/index.php"

    def send_sms(self, phone, content, sms_type, sender):
        url = f"{self.api_url}/sms/send"
        payload = {
            "to": [phone],
            "content": content,
            "type": sms_type,
            "sender": sender
        }

        headers = {
            "Authorization": "Basic " + base64.b64encode((self.token + ":").encode()).decode(),
            "Content-Type": "application/json"
        }

        response = requests.post(url, data=json.dumps(payload), headers=headers)
        return response.json()

    def get_user_info(self):
        url = f"{self.api_url}/user/info"
        headers = {
            "Authorization": "Basic " + base64.b64encode((self.token + ":").encode()).decode()
        }
        response = requests.get(url, headers=headers)
        return response.json()
