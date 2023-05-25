import requests
import hashlib

with open('./test.png', 'rb') as f:
    img = f.read()

img_hash = hashlib.md5(img).hexdigest()
print(img_hash)

r = requests.post('http://localhost:8080/data', json={'latitude': '29.991393', 'longitude': '59.361260', 'pic': img_hash})
#print(r.status_code)
