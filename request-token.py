import requests, os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.


url_auth = os.getenv('URL_AUTH')
data = {'username': 'user', 'password': 'Bob'}
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

response = requests.post(url_auth, data=json.dumps(data), headers=headers)
jsonResp = response.json()
        
print(jsonResp)