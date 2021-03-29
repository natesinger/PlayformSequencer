
import yaml
import time
from tkinter import Tk
from tkinter.filedialog import askopenfilename, askdirectory

def set_config():
    print("Create a project, save the template file on your local machine...")
    write_config(*get_user_input())

def write_config(file_template:str, directory_frames:str, directory_output:str, project_id:str, authorization:str, CONFIG_FILE:str="config.yml"):
    users = [{'file_template': file_template},
     {'directory_frames': directory_frames},
      {'directory_output': directory_output},
       {'project_id': project_id},
        {'authorization': authorization}]

    with open(CONFIG_FILE, 'w') as f:
        data = yaml.dump(users, f)

def read_config(CONFIG_FILE:str="config.yml") -> list:
    with open(CONFIG_FILE) as f:
        for config_file in yaml.load_all(f, Loader=yaml.FullLoader):
            return(config_file[0]["file_template"], config_file[1]["directory_frames"],
            config_file[2]["directory_output"], config_file[3]["project_id"],
            config_file[4]["authorization"])

def get_user_input():
    #https://stackoverflow.com/questions/3579568/choosing-a-file-in-python-with-simple-dialog
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing

    input("Hit [enter] to proceed with selecting the template file...")
    file_template = askopenfilename() # show an "Open" dialog box and return the path to the selected file
    time.sleep(0.5)
    input("Hit [enter] to proceed with selecting a directory of frames...")
    directory_frames = askdirectory()
    time.sleep(1)
    input("Hit [enter] to proceed with selecting an output directory...")
    directory_output = askdirectory()
    time.sleep(1)
    project_id = input("Please provde a project ID from the URL of the project page, as an integer: ")
    time.sleep(1)
    jwt = input("Please provide the authorization header(JWT) like \"JWT eyJh...\": ")

    return file_template, directory_frames, directory_output, project_id, jwt
