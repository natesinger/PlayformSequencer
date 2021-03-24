#!/usr/bin/python3
import io
import json
import os
from pathlib import Path
import platform
from progress.bar import Bar
import requests
import time
from tkinter import Tk
from tkinter.filedialog import askopenfilename, askdirectory
import urllib
import warnings
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
        self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0', 'Accept': 'application/json, text/plain, */*', 'Authorization':jwt}

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
            file = {'input': open('.tmpfile.png','rb'), 'custom_style': open('/home/singern/Desktop/0109.png','rb')}
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

def get_user_input():
    #https://stackoverflow.com/questions/3579568/choosing-a-file-in-python-with-simple-dialog
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing

    print("Create a project, save the template file on your local machine...")
    input("Hit [enter] to proceed with selecting it...")
    file_template = askopenfilename() # show an "Open" dialog box and return the path to the selected file
    time.sleep(1)
    input("Hit [enter] to proceed with selecting a directory of frames...")
    directory_frame = askdirectory()
    time.sleep(1)
    input("Hit [enter] to proceed with selecting an output directory...")
    directory_output = askdirectory()
    time.sleep(1)
    project_id = input("Please provde a project ID from the URL of the project page, as an integer: ")
    time.sleep(1)
    jwt = input("Please provide the authorization header(JWT) like \"JWT eyJh...\": ")

    return file_template, directory_frame, directory_output, project_id, jwt

#INIT
try:
    file_template, directory_frame, directory_output, project_id, jwt = get_user_input()

    directory_frame = Path("/home/singern/Desktop/illegal_shit/frames")
    if not directory_frame.is_dir():
        print("You suck, give me a real folder... or check permissions??")
        exit()

    files = [f for f in os.listdir(directory_frame)]
    files.sort()

    if platform.system() == "Windows":
        files_input = [f"{directory_frame.resolve()}\{f}" for f in files]
    else: #its linux or macos
        files_input = [f"{directory_frame.resolve()}/{f}" for f in files]

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
            new_picture = FuckPic(f, project_id, jwt, True)
            with open(files_output[i], 'wb') as io:
                io.write(new_picture.image_generate)
            bar.next()

except KeyboardInterrupt:
    print("[!] Aborted by request...\n", end = "\r")
exit()
