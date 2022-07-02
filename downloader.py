# Joseph A.
# SC file download automator

import json
import requests
import os.path
import re
import sys
from requests.structures import CaseInsensitiveDict

destination = ''
load_file = ''
#load the memories_history.json file
try:
    load_file = sys.argv[1]
    try:
        destination = sys.argv[2]
    except:
        destination = './memories'
except IndexError:
    print(f"Please input a file.\n{sys.argv[0]} usage: {sys.argv[0]} [memories_history.json] [(optional) destination='./memories']")
    exit()

#----------
if sys.platform == "win32":
    dir_destination = f'{destination}\\'
else:
    dir_destination = f'{destination}/'

#check if the final destination exists
if not os.path.isdir(dir_destination):
    os.makedirs(dir_destination)
#----------
url = "https://app.snapchat.com/dmd/memories"
headers = CaseInsensitiveDict()
headers["Content-Type"] = "application/x-www-form-urlencoded"
json_data = ''
#----------


with open(load_file, 'rb') as f:
    json_data = f.read().decode('utf-8')
# load the list of files from json file, also, keep tabs on file names to append numbers
# for duplicate files.
memories = json.loads(json_data)['Saved Media']
files = []
mem_length = len(memories) #get the total # of files, useful later for progress
current = 0

for memory in memories:
    #Splitting all data fields, just want the data
    data = memory['Download Link'].split('?')[1]
    #POST data to Snap API, recieve the file download link, then GET the file from download
    r = requests.post(url, headers=headers, data=data)
    file_raw = requests.get(r.content.decode("utf-8"))
    
    #save the file data
    ext = ''
    if memory['Media Type'] == 'Video':
        ext = 'mp4'
    else:
        ext = 'jpg'
    filename = memory['Date']
    
    #if the filename exists (no overwriting!)
    while filename in files:
        #this will probably need to be refactored :|
        try:
            #if the last part of the filename is a number, take the whole number
            #and append it by 1. we added the number
            #e.g. 2022-05-28 01:23:45 UTC 1 >> 2022-05-28 01:23:45 UTC 2
            if type(int(filename[-1])) is int:
                temp = filename.split()
                number = int(temp[-1])
                number += 1
                del temp[-1]
                filename = ' '.join(temp+list(str(number)))
                
        except ValueError:
            # Just slap on the number
            filename = filename + ' 1'
    #when it works, save the filename so we dont overwrite it.
    files.append(filename)
    #edit the filename so it has no spaces or illegal chars
    filename = re.sub('[^0-9a-zA-Z]+', '-', filename)
    #show progress
    percent = int((current/mem_length)*30)
    print(f'\rProgress: |{(percent)*"█"}{(30*"-")}| {percent}% || {dir_destination}{filename}.{ext}', end="\r")
    current += 1
    #finally, write the data from SC api to file
    with open(f'{dir_destination}{filename}.{ext}', 'wb') as f:
        f.write(file_raw.content)