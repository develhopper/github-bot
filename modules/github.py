import requests
import json
import os
import math
from time import sleep

class Github:
    def __init__(self,client_id):
        self.client_id = client_id
        self.base_url = 'https://api.github.com'
        self.headers = {'Accept':'application/vnd.github.v3+json', 'User-Agent': 'Mybot/0.1'}
        self._auth = {}

        if os.path.exists('auth.json'):
            with open('auth.json', 'r') as f:
                self._auth = json.load(f)

    def auth(self):
        if os.path.exists('auth.json'):
            if self.save_auth_token() == True:
                print('Authenticated')
                return

        url = 'https://github.com/login/device/code'
        data = {'client_id':self.client_id, 'scope':'user:follow'}
        r = requests.post(url, data=data, headers = self.headers)
        
        if r.status_code == 200:
            resp = r.json()
            
            export = {'device_code': resp["device_code"]}

            with open('auth.json', 'w') as authfile:
                json.dump(export, authfile)

            print("Please Authenticate the client using blow link and code \n")
            print(f'Link: {resp["verification_uri"]} \n')
            print(f'Code: {resp["user_code"]} \n')
            
            print('Then run auth command again')


    def save_auth_token(self):
        url = 'https://github.com/login/oauth/access_token'

        with open('auth.json', 'r') as file:
            js = json.load(file)

            device_code = js['device_code']
            data = {
                'client_id': self.client_id,
                'device_code': device_code,
                'grant_type': 'urn:ietf:params:oauth:grant-type:device_code'
            }

            r = requests.post(url, data = data, headers = self.headers)

            resp = r.json()
            if 'error' in resp:
                print(resp['error'])
                return False;

            js['token'] = resp['access_token']
            
            with open('auth.json', 'w') as authfile:
                json.dump(js, authfile)
            
            return True

    def send_request(self, route, method = 'get', data = None, params = None):
        headers = self.headers
        
        headers['Authorization'] = "Bearer "+self._auth['token']
        url = self.base_url+route;

        if method == 'get':
            r = requests.get(url, headers = headers, params = params)

        if method == 'post':
            r = request.post(url, headers = headers, data = data)

        if method == 'delete':
            r = requests.delete(url, headers = headers, data = data)

        if method == 'put':
            r = requests.delete(url, headers = headers, data = data)

        return r

    def unfollow(self): 
        if 'token' not in self._auth:
            print('Not Authenticated')

        print("Get user data")

        user_data = self.send_request('/user').json()

        following_count = user_data ['following']
        followers_count = user_data ['followers']

        print("Get Following list")
        following = self.get_list('following', following_count)
        
        print("Get Followers list")
        followers = self.get_list('followers', followers_count)

        print("Calculate Differents")

        diff = list(set(following) - set(followers))

        print("unfollow ...")

        self.unfollow_list(diff)

    
    def get_list(self, mode, count):
        if mode == 'following':
            url = "/user/following"
        if mode == 'followers':
            url =  "/user/followers"

        pages = math.ceil(count / 100)

        result = []

        for i in range(pages):
            params = {'per_page': 100, 'page':i+1}

            resp = self.send_request(route=url,params=params).json()

            result = result + self.get_usernames(resp)

        return result

    def get_usernames(self, arr):
        result = []
        for item in arr:
            result.append(item['login'])
        
        return result

    def unfollow_list(self, arr):
        for user in arr:
            print(f'unfollowing {user} : ', end='')
            r = self.send_request(f'/user/following/{user}','delete')
            print(r.status_code)
            sleep(1)

