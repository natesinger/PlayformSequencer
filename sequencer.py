#!/usr/bin/python3
from configure import set_config,read_config
from backend import FuckPic
from pathlib import Path
from progress.bar import Bar
import os
import argparse

'''usage: sequencer.py [-h] [-o] [-oa]

Playform image sequencer.

optional arguments:
  -h, --help         show this help message and exit
  -o, --override     rewrite current config
  -oa, --over-abort  rewrite current config but do not run sequencer'''
try:
    parser = argparse.ArgumentParser(description='Playform image sequencer.')
    parser.add_argument('-c', '--configure', dest='configure', action='store_true',
                            help='rewrite current config')
    parser.add_argument('-ca', '--conf-abort', dest='configure_abort', action='store_true',
                            help='rewrite current config but do not run sequencer')
    args = parser.parse_args()

    if (args.configure != False) or (args.configure_abort != False):
        set_config()

    if args.configure_abort: exit() #exit if abort specified

    file_template, directory_frames, save_dir, project_id, user_jwt = read_config()

    directory_frames = Path(directory_frames)
    if not directory_frames.is_dir():
        print("You suck, give me a real folder... or check permissions??")
        exit()

    files = [f for f in os.listdir(directory_frames) if not directory_frames == ".DS_STORE"] #fix for dum apple
    files.sort()

    files_input = [f"{directory_frames.resolve()}/{f}" for f in files]
    files_output = [f"{save_dir}/{f}" for f in files]

    total_file_count = len(files_input)

    with Bar("Processing frames") as bar:
        bar.max = total_file_count
        for i,f in enumerate(files_input):
            new_picture = FuckPic(f, file_template, project_id, user_jwt)

            extension_index = files_output[i].find('.')
            updated_file_name = files_output[i][:extension_index] + '.jpg'
            with open(updated_file_name, 'wb') as io:
                io.write(new_picture.image_generate)

            bar.next()

except KeyboardInterrupt:
    print('[!] Aborted by request...')
