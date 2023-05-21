import base64
import requests

with open('./test.png', 'rb') as f:
    img = f.read()

img = base64.b64encode(img)
img = img.decode('UTF-8')

r = requests.post('http://localhost:18080/data', json={'latitude': '29.991393', 'longitude': '59.361260', 'pic': img})
print(r.status_code)