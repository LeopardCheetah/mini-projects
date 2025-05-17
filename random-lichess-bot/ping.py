# ping an endpoint


import requests
import json
import time

from dotenv import dotenv_values

bot_key = dotenv_values(".env")["LICHESS_API_KEY"]

link = ''

#############33
############
# "If you receive an HTTP response with a 429 status, please wait a full minute before resuming API usage"

def is429():
    return "no"


########################




def getRequest(r):
    headers = {'Authorization': f'Bearer {bot_key}'}
    response = requests.get('https://lichess.org/api/' + r, headers=headers)
    return response


def getStream(s):
    start_time = time.time()
    timeout = 60

    headers = {'Authorization': f'Bearer {bot_key}'}
    while True: 
        response = requests.get('https://lichess.org/api/' + s, headers=headers)
        print(f'time: {time.time()} | event:', response.text)
        time.sleep(3)
        print(time.time())

        if time.time() - start_time > timeout:
            break
        continue 
    

    return 


some_rt = getRequest('account')
print(some_rt.status_code)
print(some_rt.json())
'''
some_r = getStream('stream/event')


print(some_r.text)
print()
print(some_r.json())
print()
print(some_r.status_code)
'''



