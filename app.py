import sys
from time import ctime
from urllib.request import Request, urlopen

from storer.secret import project_id, access_key

def main():
    print(sys.argv)

    l = len(sys.argv) 
    if l == 0:
        print("use --help to get help")

    if sys.argv[1] == '--upload':
        if l == 3:
            upload(sys.argv[2])
    elif sys.argv[1] == '--update':
        if l == 3:
            update(sys.argv[2])
    elif sys.argv[1] == '--delete':
        delete()
    elif sys.argv[1] == '--download':
        if l == 3:
            download(sys.argv[2])
    elif sys.argv[1] == '--help':
        print('--upload <file-path>: to upload a file to cloud\n--update <file-path>: to update a file on cloud\n--delete : to delete the existing file on server\n--download <file-path>: to download a file locally')
    else:
        print('use --help to get help')

# https://gitlab.com/api/v4/projects/<:id>/repository/files/<filename-with-extension>
# <:id> is project id, which can be found in the settings of your gitlab repo

def upload(file):
    with open(file, 'rb+') as f:
        content = '"{}"'.format(f.read())
        commit_message = '"Uploaded on {}"'.format(ctime())
        print(content)
        print(content.encode())
        data = '{"branch": "master", "content": ' + content + ', "commit_message": '+ commit_message +'}'
        print(data.encode())
        a = Request("https://gitlab.com/api/v4/projects/"+ project_id +"/repository/files/file%2Etxt", data=data.encode(), headers={"Authorization": access_key, "Content-Type": "application/json"}, method="POST")
        urlopen(a)
    print('uploaded')
    return

def update(file):
    with open(file, 'rb+') as f:
        content = '"{}"'.format(f.read())
        commit_message = '"Updated on {}"'.format(ctime())
        print(content)
        print(content.encode())
        data = '{"branch": "master", "content": ' + content + ', "commit_message": '+ commit_message +'}'
        print(data.encode())
        a = Request("https://gitlab.com/api/v4/projects/"+ project_id +"/repository/files/file%2Etxt", data=data.encode(), headers={"Authorization": access_key, "Content-Type": "application/json"}, method="PUT")
        urlopen(a)
    print("updated")
    return

def delete():
    commit_message = '"Deleted on {}"'.format(ctime())
    data = '{"branch": "master", "commit_message": '+ commit_message +'}'
    a = Request("https://gitlab.com/api/v4/projects/"+ project_id +"/repository/files/file%2Etxt", data=data.encode(), headers={"Authorization": access_key, "Content-Type": "application/json"}, method="DELETE")
    urlopen(a)
    print("deleted")

def download(file):
    a = Request("https://gitlab.com/api/v4/projects/"+ project_id +"/repository/files/file%2Etxt/raw?ref=master", headers={"Authorization": access_key}, method="GET")
    u = urlopen(a)
    with open(file, 'wb+') as f:
        f.write(u.read())
    print("downloaded")

if __name__ == "__main__":
    main()