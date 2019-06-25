import requests
import base64
import sys
import os
import os.path
import json
from time import ctime
from urllib.request import Request, urlopen

from storer.secret import project_id, access_token

def main():
    # print(sys.argv)

    l = len(sys.argv) 
    if l == 1:
        print("use --help to get help")
    elif sys.argv[1] == '--upload':
        if l == 3:
            f = []
            f.append(sys.argv[2].split('/')[-1])
            upload(sys.argv[2][:-(len(f[0]) + 1)], f)
            # print(1)
    elif sys.argv[1] == '--update':
        if l == 3:
            f = []
            f.append(sys.argv[2].split('/')[-1])
            update(sys.argv[2][:-(len(f[0]) + 1)], f)
    elif sys.argv[1] == '--delete':
        if l == 3:
            delete('', [sys.argv[2]])
    elif sys.argv[1] == '--download':
        if l == 4:
            download([sys.argv[2]], sys.argv[3])
    elif sys.argv[1] == '--help':
        print('--upload <file-path>: to upload a file to cloud\n--update <file-path>: to update a file on cloud\n--delete <file-name>: to delete the existing file on server\n--download <file-name> <file-download-directory>: to download a file locally')
    else:
        print('use --help to get help')

# https://gitlab.com/api/v4/projects/<:id>/repository/files/<filename-with-extension>
# <:id> is project id, which can be found in the settings of your gitlab repo

import mimetypes

def upload(directory, files, level=1):
    # print(directory + '/' + files[0])
    # print(files)
    for file in files:
        if os.path.isfile(directory + '/' + file):
            # print(2)
            (ext,_) = mimetypes.guess_type(file)
            e=2
            if ext == None:
                e=0
            if e == 2:
                if ext[:4] == 'text':
                    e=1
                else:
                    e=0 
            # e = 0 means not text file, e = 1 means text file
            if e == 0:
                # with open(file, encoding='utf-8', mode='r') as f:
                with open(directory + '/' + file, mode='rb+') as f:
                    name = f.name.split('/')[-level:]
                    while(len(name) != 1):
                        name[-2] = name[-2] + '%2F' + name[-1]
                        del(name[-1])
                    # print(name)
                    # content = "{}".format(f.read())
                    content = "{}".format(base64.b64encode(f.read()).decode())
                    commit_message = "Uploaded on {}".format(ctime())
                    # print(content)
                    # print(content.encode())
                    headers = {'Private-Token': access_token, 'Content-Type': 'application/json'}
                    data = {"branch": "master","content": content, "commit_message": commit_message}
                    # print(data.encode())
                    # files/<folder-name>%2F
                    r = requests.post("https://gitlab.com/api/v4/projects/"+ project_id +"/repository/files/" + name[0], headers=headers, json=data)

                if r.status_code >= 400:
                    print("Error {}".format(r.status_code))
                else:
                    print("Success with status code:{}".format(r.status_code))

            elif e == 1:
                with open(directory + '/' + file, encoding='utf-8', mode='r') as f:
                    name = f.name.split('/')[-level:]
                    while(len(name) != 1):
                        name[-2] = name[-2] + '%2F' + name[-1]
                        del(name[-1])
                    # print(name)
                    content = "{}".format(f.read())
                    # content = "{}".format(base64.b64encode(f.read()).decode())
                    commit_message = "Uploaded on {}".format(ctime())
                    # print(content)
                    # print(content.encode())
                    headers = {'Private-Token': access_token, 'Content-Type': 'application/json'}
                    data = {"branch": "master","content": content, "commit_message": commit_message}
                    # print(data.encode())
                    # files/<folder-name>%2F
                    r = requests.post("https://gitlab.com/api/v4/projects/"+ project_id +"/repository/files/" + name[0], headers=headers, json=data)

                if r.status_code >= 400:
                    print("Error {}".format(r.status_code))
                else:
                    print("Success with status code:{}".format(r.status_code))
            
        
        elif os.path.isdir(directory + '/' + file):
            upload(directory+'/'+file, os.listdir(directory + '/' + file), level=level+1)
    return

def update(directory, files, level=1):
    # print(directory + '/' + files[0])
    # print(files)
    for file in files:
        if os.path.isfile(directory + '/' + file):
            # print(2)
            (ext,_) = mimetypes.guess_type(file)
            e=2
            if ext == None:
                e=0
            if e == 2:
                if ext[:4] == 'text':
                    e=1
                else:
                    e=0 
            # e = 0 means not text file, e = 1 means text file
            if e == 0:
                # with open(file, encoding='utf-8', mode='r') as f:
                with open(directory + '/' + file, mode='rb+') as f:
                    name = f.name.split('/')[-level:]
                    while(len(name) != 1):
                        name[-2] = name[-2] + '%2F' + name[-1]
                        del(name[-1])
                    # print(name)
                    # content = "{}".format(f.read())
                    content = "{}".format(base64.b64encode(f.read()).decode())
                    commit_message = "Updated on {}".format(ctime())
                    # print(content)
                    # print(content.encode())
                    headers = {'Private-Token': access_token, 'Content-Type': 'application/json'}
                    data = {"branch": "master","content": content, "commit_message": commit_message}
                    # print(data.encode())
                    # files/<folder-name>%2F
                    r = requests.put("https://gitlab.com/api/v4/projects/"+ project_id +"/repository/files/" + name[0], headers=headers, json=data)

                if r.status_code >= 400:
                    print("Error {}".format(r.status_code))
                else:
                    print("Success with status code:{}".format(r.status_code))

            elif e == 1:
                with open(directory + '/' + file, encoding='utf-8', mode='r') as f:
                # with open(directory + '/' + file, mode='rb+') as f:
                    name = f.name.split('/')[-level:]
                    while(len(name) != 1):
                        name[-2] = name[-2] + '%2F' + name[-1]
                        del(name[-1])
                    # print(name)
                    content = "{}".format(f.read())
                    # content = "{}".format(base64.b64encode(f.read()).decode())
                    commit_message = "Updated on {}".format(ctime())
                    # print(content)
                    # print(content.encode())
                    headers = {'Private-Token': access_token, 'Content-Type': 'application/json'}
                    data = {"branch": "master","content": content, "commit_message": commit_message}
                    # print(data.encode())
                    # files/<folder-name>%2F
                    r = requests.put("https://gitlab.com/api/v4/projects/"+ project_id +"/repository/files/" + name[0], headers=headers, json=data)

                if r.status_code >= 400:
                    print("Error {}".format(r.status_code))
                else:
                    print("Success with status code:{}".format(r.status_code))


        elif os.path.isdir(directory + '/' + file):
            update(directory+'/'+file, os.listdir(directory + '/' + file), level=level+1)
    return

def delete(directory, files):
    for file in files:
        headers = {'Private-Token': access_token}
        if directory != '':
            # print(directory[3:] + '%2F' + file)
            r = requests.get("https://gitlab.com/api/v4/projects/"+ project_id +"/repository/tree?path=" + directory[3:] + '%2F' + file, headers=headers)
        else:
            r = requests.get("https://gitlab.com/api/v4/projects/"+ project_id +"/repository/tree?path=" + file, headers=headers)
        details = json.loads(r.content.decode())
        # print(details)

        if len(details) == 0:
            if directory != '':
                name = directory + '%2F' + file
            else:
                name = '%2F' + file
            commit_message = "Deleted on {}".format(ctime())
            # data = '{"branch": "master", "commit_message": '+ commit_message +'}'
            headers = {'Private-Token': access_token, 'Content-Type': 'application/json'}
            data = {"branch": "master", "commit_message": commit_message}
            # a = Request("https://gitlab.com/api/v4/projects/"+ project_id +"/repository/files/" + name, data=data.encode(), headers={"Private-Token": access_token, "Content-Type": "application/json"}, method="DELETE")
            # urlopen(a)
            # print(name)
            r = requests.delete("https://gitlab.com/api/v4/projects/"+ project_id +"/repository/files/" + name[3:], headers=headers, json=data)
            # print("deleted")
            
            if r.status_code >= 400:
                print("Error {}".format(r.status_code))
            else:
                print("Success with status code:{}".format(r.status_code))
        else:
            f = []
            for d in details:
                f.append(d['name'])
            delete(directory + '%2F' + file, f)
    return

def download(files, file_destination_directory):
    for file in files:
        headers = {'Private-Token': access_token}
        r = requests.get("https://gitlab.com/api/v4/projects/"+ project_id +"/repository/tree?path=" + file, headers=headers)
        details = json.loads(r.content.decode())
        
        (ext,_) = mimetypes.guess_type(file)
        if len(details) == 0:
            e=2
            if ext == None:
                e=0
            if e == 2:
                if ext[:4] == 'text':
                    e=1
                else:
                    e=0 
            
            headers = {'Private-Token': access_token, 'Content-Type': 'application/json'}
            r = requests.get("https://gitlab.com/api/v4/projects/"+ project_id +"/repository/files/"+ file +"/raw?ref=master", headers=headers)
            # print(r.content)
            dest = file_destination_directory+file
            desti = dest.split('%2F')
            while(len(desti) != 1):
                desti[-2] = desti[-2] + '/' + desti[-1]
                del(desti[-1])
            
            # e = 0 means not text file, e = 1 means text file
            if e == 0:
                with open(desti[0], 'wb+') as f:
                    f.write(base64.b64decode(r.content))
                # print("downloaded")
            elif e == 1:
                with open(desti[0], encoding='utf-8', mode='w') as f:
                    f.write(r.content.decode())

            if r.status_code >= 400:
                print("Error {}".format(r.status_code))
            else:
                print("Success with status code:{}".format(r.status_code))


        else:
            dest = file_destination_directory+file
            desti = dest.split('%2F')
            while(len(desti) != 1):
                desti[-2] = desti[-2] + '/' + desti[-1]
                del(desti[-1])
            os.mkdir(desti[0])
            f = []
            for d in details:
                f.append(file + '%2F' + d['name'])
            download(f, file_destination_directory)
    return

if __name__ == "__main__":
    main()