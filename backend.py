#!/usr/bin/python3
import io
import json
import platform
import requests
import time
import urllib
import warnings
warnings.filterwarnings("ignore")

class FuckPic:
    def __init__(self, user_image:str, file_template:str, project_id:str, user_jwt:str, proxy:bool=False):
        """"""
        self.image_user_abspath = user_image
        self.project_id = project_id
        self.jwt = user_jwt
        self.proxy_state = proxy
        self.file_template = file_template

        self.image_sketch = None
        self.image_generate = None

        self.proxy = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}
        self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0', 'Accept': 'application/json, text/plain, */*', 'Authorization':user_jwt}

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
            file = {'input': open('.tmpfile.png','rb'), 'custom_style': open(self.file_template,'rb')}
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
