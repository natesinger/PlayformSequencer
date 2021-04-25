#!/usr/bin/python3
from tkinter import Tk
from tkinter.filedialog import askdirectory
from PIL import Image
import PIL
import os
Tk().withdraw()

directory_stale = askdirectory()
directory_new = directory_stale + '/sequenced/'

files_stale = []

try:
    input(f"Press [enter] to create subdir, and parse [{directory_stale}] into:\n\t[{directory_new}]")

    if os.path.isdir(directory_new):
        input(f'Directory {directory_new} exists, press [enter] to continue and potentially overwrite [!!]')
    else:
        os.makedirs(directory_new)

    for file in os.listdir(directory_stale):
        file = f"{directory_stale}/{file}"
        if not os.path.isdir(file): files_stale.append(file)

    files_stale.sort()
    files_stale_loaded = [Image.open(file) for file in files_stale]

    for n, file in enumerate(files_stale_loaded): file.save(f"{directory_new}{n:04}.jpg")

except KeyboardInterrupt:
    print('[!] Aborted by request')
    exit()
