from time import ctime
from urllib.request import Request, urlopen

from secret import access_key

def auto_backup():
    while True:
        # backup every 30sec if the there is any update
        if (int(ctime()[17:19]) % 30 == 0):
            # address of the file to backup
            with open('<LOCATION>', 'rb+') as f:
                content = '"{}"'.format(f.read())
                commit_message = '"Updated on {}"'.format(ctime())
                print(content)
                print(content.encode())
                data = '{"branch": "master", "content": ' + content + ', "commit_message": '+ commit_message +'}'
                print(data.encode())
                a = Request("https://gitlab.com/api/v4/projects/12659010/repository/files/file%2Etxt", data=data.encode(), headers={"Authorization": access_key, "Content-Type": "application/json"}, method="PUT")
                h = urlopen(a)
                print(h.code)

auto_backup()