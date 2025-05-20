import requests
import json
from ascii_magic import AsciiArt
# https://github.com/LeandroBarone/python-ascii_magic



r = requests.get('https://randomfox.ca/floof/')

AsciiArt.quick_test()
quit()




fox = AsciiArt.from_image('sushi.png')


try:
    fox = AsciiArt.from_url(r.json()["image"])
except OSError as e:
    print(f'Could not load the image, server said: {e.code} {e.msg}')
    
fox.to_terminal(columns=80)