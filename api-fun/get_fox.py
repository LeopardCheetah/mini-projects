import requests
import json


r = requests.get('https://randomfox.ca/floof/')



'''
fox = AsciiArt.from_image('moon.png') # placeholder


try:
    print(r.json()["image"], type(r.json()["image"]))
    # fox = AsciiArt.from_url(r.json()["image"])
    fox = AsciiArt.from_url('https://randomfox.ca/images/98.jpg')
    # fox = AsciiArt.from_url('https://fastly.picsum.photos/id/237/536/354.jpg?hmac=i0yVXW1ORpyCZpQ-CknuyV-jbtU7_x9EBQVhvT5aRr0')
except OSError as e:
    print(f'Could not load the image, server said: {e.code} {e.msg}')
    
fox.to_terminal(columns=80)
'''