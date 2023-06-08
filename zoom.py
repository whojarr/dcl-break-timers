import datetime
import json
import os
import requests
from requests.auth import HTTPBasicAuth


class Zoom():

    def __init__(self, account_id, client_id, client_secret):

        self.account_id = account_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token_expires = None
        self.access_token_data = ""


    def chat_channels(self):

        url = "https://api.zoom.us/v2/chat/users/me/channels/"
        headers = {
            "Content-Type": "Application/json",
            "Authorization": f"Bearer {self.token()}"
        }

        response = requests.get(url, headers=headers)

        return(response.json())


    def chat_send(self, channel_id=None, message="Hello"):

        url = f"https://api.zoom.us/v2/chat/users/me/messages"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token()}"
        }
        data = {
            "to_channel": channel_id,
            "message": message
        }
        response = requests.post(url, data=json.dumps(data), headers=headers)

        return response.json()


    def meeting(self,meeting_id=None):

        if meeting_id:
            url = f"https://api.zoom.us/v2/meetings/{meeting_id}"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.token()}"
            }
            response = requests.get(url, headers=headers)

            return response.json()


    def meeting_list(self,type=""):

        url = f"https://api.zoom.us/v2/users/me/meetings/?type={type}"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token()}"
        }
        response = requests.get(url, headers=headers)

        return response.json()


    def meeting_metrics(self,meeting_id=None):

        if meeting_id:

            url = f"https://api.zoom.us/v2/metrics/meetings/{meeting_id}"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.token()}"
            }
            response = requests.get(url, headers=headers)

            return response.json()
 

    def meeting_messages(self, meeting_id = None):

        if not meeting_id:
            meeting_id = self.meeting_pmi()

        url = f"https://api.zoom.us/v2/live_meetings/{meeting_id}/chat/messages/"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token()}"
        }
        response = requests.get(url, headers=headers)

        return response.json()


    def meeting_pmi(self):

        url = f"https://api.zoom.us/v2/users/me"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token()}"
        }
        response = requests.get(url, headers=headers)

        if response.status_code == 200:

            return response.json()['pmi']

        else:

            return response.status_code


    def myconverter(self, o):
        if isinstance(o, datetime.datetime):
            return o.__str__()


    def token(self):

        if self.token_expired():
            self.token_refresh()

        return self.access_token_data['access_token']


    def token_data_load(self):
        with open('auth_token.tmp', 'r') as file:
            raw = file.read()
            data = json.loads(raw)

            expires = data['expires_date']
            self.access_token_expires = datetime.datetime.strptime(expires, "%Y-%m-%d %H:%M:%S.%f")
            self.access_token_data = data


    def token_expired(self):
        if not self.access_token_expires:
            if os.path.isfile('auth_token.tmp'):
                self.token_data_load()
            else:
                print('token expired, refreshing token')
                self.token_refresh()

        if self.access_token_expires < datetime.datetime.now():
            return True
        return False


    def token_refresh(self):
        url = f'https://zoom.us/oauth/token?grant_type=account_credentials&account_id={self.account_id}'
        response = requests.post(url, auth=HTTPBasicAuth(self.client_id,self.client_secret))
        self.access_token_data = response.json()
        self.access_token_expires = datetime.datetime.now() + datetime.timedelta(seconds=self.access_token_data['expires_in'])
        self.token_store()


    def token_store(self):
        with open('auth_token.tmp', 'w') as file:
            store_data = self.access_token_data
            store_data["expires_date"] = self.access_token_expires

            file.write(json.dumps(store_data, default=self.myconverter, indent=4))
