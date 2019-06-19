import sys
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
            upload(sys.argv[2])
    elif sys.argv[1] == '--update':
        if l == 3:
            update(sys.argv[2])
    elif sys.argv[1] == '--delete':
        if l == 3:
            delete(sys.argv[2])
    elif sys.argv[1] == '--download':
        if l == 4:
            download(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == '--help':
        print('--upload <file-path>: to upload a file to cloud\n--update <file-path>: to update a file on cloud\n--delete <file-name>: to delete the existing file on server\n--download <file-name> <file-download-directory>: to download a file locally')
    else:
        print('use --help to get help')

# https://gitlab.com/api/v4/projects/<:id>/repository/files/<filename-with-extension>
# <:id> is project id, which can be found in the settings of your gitlab repo

def upload(file):
    with open(file, 'rb+') as f:
        name = f.name.split('/')[-1]
        print(type(name))
        content = '"{}"'.format(f.read())
        commit_message = '"Uploaded on {}"'.format(ctime())
        print(content)
        print(content.encode())
        data = '{"branch": "master", "content": ' + content + ', "commit_message": '+ commit_message +'}'
        print(data.encode())
        a = Request("https://gitlab.com/api/v4/projects/"+ project_id +"/repository/files/" + name, data=data.encode(), headers={"Private-Token": access_token, "Content-Type": "application/json"}, method="POST")
        urlopen(a)
    print('uploaded')
    return

def update(file):
    with open(file, 'rb+') as f:
        name = f.name.split('/')[-1]
        print(type(name))
        content = '"{}"'.format(f.read())
        commit_message = '"Updated on {}"'.format(ctime())
        print(content)
        print(content.encode())
        data = '{"branch": "master", "content": ' + content + ', "commit_message": '+ commit_message +'}'
        print(data.encode())
        a = Request("https://gitlab.com/api/v4/projects/"+ project_id +"/repository/files/" + name, data=data.encode(), headers={"Private-Token": access_token, "Content-Type": "application/json"}, method="PUT")
        urlopen(a)
    print("updated")
    return

def delete(file):
    try:
        name = file.split('/')[-1]
        commit_message = '"Deleted on {}"'.format(ctime())
        data = '{"branch": "master", "commit_message": '+ commit_message +'}'
        a = Request("https://gitlab.com/api/v4/projects/"+ project_id +"/repository/files/" + name, data=data.encode(), headers={"Private-Token": access_token, "Content-Type": "application/json"}, method="DELETE")
        urlopen(a)
        print("deleted")
    except:
        print("Error 404: no such file found")
    return

def download(file_source, file_destination_directory):
    try:
        a = Request("https://gitlab.com/api/v4/projects/"+ project_id +"/repository/files/"+ file_source +"/raw?ref=master", headers={"Private-Token": access_token}, method="GET")
        u = urlopen(a)
        with open(file_destination_directory+file_source, 'wb+') as f:
            f.write(u.read())
        print("downloaded")
    except:
        print("Error 404: no such file found or directory not found")
    return

if __name__ == "__main__":
    main()