#!/usr/bin/python3
# place this file in /usr/bin/
# after placing .service file type
# sudo systemctl daemon-reload
# sudo systemctl enable backup.service
# sudo systemctl start backup.service

from time import ctime
from urllib.request import Request, urlopen

# setup access_key as per requirement
from storer.secret import access_token, project_id

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
                a = Request("https://gitlab.com/api/v4/projects/"+ project_id +"/repository/files/file%2Etxt", data=data.encode(), headers={"Private-Token": access_token, "Content-Type": "application/json"}, method="PUT")
                h = urlopen(a)
                print(h.code)

auto_backup()