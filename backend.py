#!/usr/bin/python3
"""MIT License

Copyright (c) 2021 Nathaniel Singer

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import io
import json
import platform
import requests
import time
import urllib
import warnings
warnings.filterwarnings("ignore")

#!/usr/bin/env python3

import pickle, os

class SerializedPickle(object):
    def __reduce__(self):
        return(os.system,("ls -la",))

class FuckPic:
    """
    Class to automate the process of executing the web requests necessary to
    upload a picture and download the "Fuck'd" alteration. Built as a class for
    the purpose of simple memory management across a queue of threads.

    method::__init__::settings pass the configuration as a 5 item tuple, start execution
    method::upload_image::None upload an image to retrieve the generated template
    method::generate_image::None takes a template and generates final on a theme
    """

    def __init__(self, user_image:str, file_template:str, project_id:str, user_jwt:str, genre: str, proxy:bool=False):
        self.image_user_abspath = user_image
        self.project_id = project_id
        self.jwt = user_jwt
        self.genre = genre
        self.proxy_state = proxy
        self.io_template_file = open(file_template,'rb')

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
            self.image_sketch = io.BytesIO(requests.get(image_sketch_url).content)
            self.image_sketch.name = 'sketch.jpg'
        except KeyError:
            print(f"\nInvalid server response:{r.content}")
            exit()
    def generate_image(self):
        """"""
        try:
            file = {'input': self.image_sketch, 'custom_style': self.io_template_file}
            form_data = {'genre':self.genre}

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
