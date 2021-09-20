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

from configure import set_config,read_config
from backend import Modify
from pathlib import Path
from progress.bar import Bar
from threading import Thread
from queue import Queue
import time
import os
import argparse

PROXY_ON = True

class ModifyPicWorker(Thread):
    """
    Class to handle thread queuing for the FukPic processes. Takes a queue of
    threads as a queue object passed with a tuple for each parameter of the thread.
    Track jobs done by the instantiated workers so this can be checked for progress.

    method::__init__::str|object set the project id, jobs done, attach the queue
    method::run::None start operating on the queue, save progress to jobs_done

    param::queue::object effectively a pointer with a list tuples as params
    param::project_id:str playform.io pid to use, each thread must be unique
    param::jobs_done::int the number of images finished, for checking progress
    """
    def __init__(self, project_id:str, queue:object):
        Thread.__init__(self)
        self.queue = queue
        self.project_id = project_id
        self.jobs_done = 0

    def run(self):
        while True:
            # Retrieve a job and expand the tuple
            files_input_abspath, files_output_abspath, file_template, user_jwt, genre, debug_flag = self.queue.get()

            # Instantiate ModifyPic to execute the operation
            new_picture = ModifyPic(files_input_abspath, file_template, self.project_id, user_jwt, genre, debug_flag)
            with open(files_output_abspath, 'wb') as io: io.write(new_picture.image_generate)

            # Track completion with a "public" variable
            self.jobs_done += 1
            self.queue.task_done()

"""usage: sequencer.py [-h] [-o] [-oa]

Playform image sequencer.

optional arguments:
  -h, --help         show this help message and exit
  -o, --override     rewrite current config
  -oa, --over-abort  rewrite current config but do not run sequencer"""

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

    file_template, directory_frames, save_dir, project_id_list, user_jwt, genre = read_config()
    project_id_list = [i.strip() for i in str(project_id_list).split(',')]

    directory_frames = Path(directory_frames)
    if not directory_frames.is_dir():
        print("You suck, give me a real folder... or check permissions??")
        exit()

    files = [f for f in os.listdir(directory_frames) if not directory_frames.name.upper() == ".DS_STORE"] #fix for dum apple
    files.sort()

    files_input = [f"{directory_frames.resolve()}/{f}" for f in files]
    files_output = [f"{save_dir}/{f.replace('png','jpg')}" for f in files]
    total_file_count = len(files_input)

    files_to_queue = [(files_input[i], files_output[i], file_template, user_jwt, genre, PROXY_ON) for i in range(total_file_count)]

    with Bar("Processing frames") as bar:
        bar.max = total_file_count
        bar.update()

        #queue assembled jobs
        queue = Queue()
        for file_job in files_to_queue: queue.put(file_job)

        # Build a worker for every provided project id and initiate
        workers = [ModifyPicWorker(pid, queue) for pid in project_id_list]
        for worker in workers:
            worker.daemon = True
            worker.start()

        #update the bar while the threads work
        while bar.index <= bar.max:
            #add up job completion for all workers
            total_jobs_done = 0
            for worker in workers: total_jobs_done += worker.jobs_done

            bar.index = total_jobs_done
            bar.update()
            time.sleep(0.1)

except (KeyboardInterrupt, SystemExit):
    print('[!] Aborted by request... killing daemon and children')
