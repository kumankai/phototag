import requests, time, os
import random as r

URL = "http://10.16.49.115:9000/api"

while True:
    n = r.randint(1, 20)
    file = {f"file": open(f"{os.getcwd()}/pi/imgs/{n}.jpg", "rb")}
    response = requests.post(URL + "/image", files=file)
    print(response.json())
    time.sleep(600)
