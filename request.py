#!/usr/bin/python3
import requests
import json
import urllib
import os
import platform
import io
import warnings
from progress.bar import Bar
from pathlib import Path

warnings.filterwarnings("ignore")

class FuckPic:
    def __init__(self, user_image:str, project_id:str, user_jwt:str, proxy:bool):
        """"""
        self.image_user_abspath = user_image
        self.project_id = project_id
        self.jwt = user_jwt
        self.proxy_state = proxy

        self.image_sketch = None
        self.image_generate = None

        self.proxy = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}
        self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0', 'Accept': 'application/json, text/plain, */*', 'Authorization':jwt_auth}

        self.upload_image()
        self.generate_image()

    def upload_image(self):
        """takes an image absolute path on the local system, makes a POST request to
         the site, and returns the sketch image as a byte string using the requests
         library"""
        try:
            file = {'image': open(self.image_user_abspath,'rb')}

            if self.proxy_state:
                r = requests.post(f"https://create.playform.io/api/sketch/projects/{self.project_id}/upload/", headers=self.headers, files=file, proxies=self.proxy, verify=False)
            else:
                r = requests.post(f"https://create.playform.io/api/sketch/projects/{self.project_id}/upload/", headers=self.headers, files=file, verify=False)

            #parse the sketch image url from the response and save it to the image_sketch class variable
            image_sketch_url = (json.loads(r.content))["sketch"]["file"]
            self.image_sketch = requests.get(image_sketch_url).content
            with open('.tmpfile.png', 'wb') as io: io.write(self.image_sketch)
        except KeyError:
            print(f"\nInvalid server response:{r.content}")
            exit()
    def generate_image(self):
        """"""
        try:
            file = {'input': open('.tmpfile.png','rb')}
            form_data = {'custom_style': '', 'style':3, 'genre':1}

            if self.proxy_state:
                r = requests.post(f"https://create.playform.io/api/sketch/projects/{self.project_id}/generate/", headers=self.headers, files=file, data=form_data, proxies=self.proxy, verify=False)
            else:
                r = requests.post(f"https://create.playform.io/api/sketch/projects/{self.project_id}/generate/", headers=self.headers, files=file, data=form_data, verify=False)

            #parse the sketch image url from the response and save it to the image_sketch class variable
            image_generate_url = (json.loads(r.content))["outputs"][0]["image"]["file"]
            self.image_generate = requests.get(image_generate_url).content
        except KeyError:
            print(f"\nInvalid server response:{r.content}")
            exit()

#INIT
project_id = "12193"
jwt_auth = "JWT eyJhbGciOiJSUzI1NiIsImtpZCI6IjRlMDBlOGZlNWYyYzg4Y2YwYzcwNDRmMzA3ZjdlNzM5Nzg4ZTRmMWUiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vcGxheWZvcm0tdXNlcnMtcHJvZCIsImF1ZCI6InBsYXlmb3JtLXVzZXJzLXByb2QiLCJhdXRoX3RpbWUiOjE2MTYzODA0NzgsInVzZXJfaWQiOiJLSUVHcmROSEZ5VnoyV1ZKRzdZSkFod0R2Z28xIiwic3ViIjoiS0lFR3JkTkhGeVZ6MldWSkc3WUpBaHdEdmdvMSIsImlhdCI6MTYxNjM5NDU3OCwiZXhwIjoxNjE2Mzk4MTc4LCJlbWFpbCI6InRlZGR5amh5ZGVAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsInBob25lX251bWJlciI6IisxOTc4NTAwNTk5MyIsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsicGhvbmUiOlsiKzE5Nzg1MDA1OTkzIl0sImVtYWlsIjpbInRlZGR5amh5ZGVAZ21haWwuY29tIl19LCJzaWduX2luX3Byb3ZpZGVyIjoicGFzc3dvcmQifX0.Z_LAp2n9S9oWso9Vw31AMpjot5L6Kp9zbEwFU8EhyiL-S6VJM7ka7dEEE3KhuHHMdAcppf8pTIFJ3S72XxjgSv1aBDd4u05pm1tFNLv1ICJ2i8iIQ4PU19NprZ6jjvAExV7aFF4REXK8Jdtz44B73kIENNmoGD-nFTmSgTvPQSYM88dbQmjO0Vcy7DKLER_GRisPdGDW9cDA8IjJvIib9eOd6YURUazSupCHB4oFOSOVV60JFt-c2EFhxrtd2IHHXqvz8HU1Lku0artaTOB8C3B3q_ahO-giJITmyqYwZ45qwEYN-J2jx73KYg9pntrUn1QvBbQj9lgaUMsRtGWUHQ"

try:
    #frames_dir = Path(input("Specify an absolute path to a directory of video frames: "))
    frames_dir = Path("/home/singern/Desktop/illegal_shit/frames")
    if not frames_dir.is_dir():
        print("You suck, give me a real folder... or check permissions??")
        exit()

    files = [f for f in os.listdir(frames_dir)]
    files.sort()

    if platform.system() == "Windows":
        files_input = [f"{frames_dir.resolve()}\{f}" for f in files]
    else: #its linux or macos
        files_input = [f"{frames_dir.resolve()}/{f}" for f in files]

    save_dir = os.path.dirname(os.path.abspath(__file__)) + ""
    if platform.system() == "Windows":
        save_dir += "\\tool_output"
        files_output = [f"{save_dir}\{f}" for f in files]
    else: #its linux or macos
        save_dir += "/tool_output"
        files_output = [f"{save_dir}/{f}" for f in files]

    if not Path(save_dir).is_dir(): os.mkdir(save_dir)

    total_file_count = len(files_input)

    with Bar("Processing frames") as bar:
        bar.max = total_file_count
        for i,f in enumerate(files_input):
            new_picture = FuckPic(f, project_id, jwt_auth, True)
            with open(files_output[i], 'wb') as io:
                io.write(new_picture.image_generate)
            bar.next()

except KeyboardInterrupt:
    print("[!] Aborted by request...\n", end = "\r")
exit()
