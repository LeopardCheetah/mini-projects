# api to unsplash

import os
from dotenv import load_dotenv 
import requests
import random

load_dotenv()

ACCESS_KEY = os.getenv('Access_Key')
SECRET_KEY = os.getenv('Secret_Key')



subject = input("what image would you like to search for?\n> ").strip()

link = 'https://api.unsplash.com/'
headers = {"Accept-Version": "v1", "Authorization": f'Client-ID {ACCESS_KEY}'}
parameters = {"query": subject, "page": 1, "per-page": 15}


r = requests.get(link + 'search/photos', params=parameters, headers=headers)

print()
print(r.url)
print(r.json())
print(r.status_code)
print(r.headers)


img_jsons = r.json()["results"]
image_links = []

for js in img_jsons:
    image_links.append(js["urls"]["regular"])

# open in firefox
for link in image_links:
    os.system(f'start firefox "{link}"')

