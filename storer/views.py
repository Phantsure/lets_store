from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
# from urllib.request import urlopen, Request
from time import ctime
import requests
import mimetypes
import base64
import json

from .secret import access_token, project_id
from .functions import handle_uploaded_file

# Create your views here. https://gitlab.com/api/v4/projects/<:id>/repository/files/ is the path to files in the given repo
def index(request):
    if(request.GET.get('uploadButton')):
        return HttpResponseRedirect(reverse('storer:upload'))
    elif(request.GET.get('updateButton')):
        return HttpResponseRedirect(reverse('storer:update'))
    elif(request.GET.get('deleteButton')):
        return HttpResponseRedirect(reverse('storer:delete'))
    elif(request.GET.get('downloadButton')):
        return HttpResponseRedirect(reverse('storer:download'))
    elif(request.GET.get('filesButton')):
        return HttpResponseRedirect(reverse('storer:files'))
    else:
        return render(request, 'storer/index.html')


def upload(request):
    if request.method == 'POST' and request.FILES:
        f = request.FILES['file']
        name = f.name
        (ext,_) = mimetypes.guess_type(name)
        e=2
        if ext == None:
            e=0
        if e == 2:
            if ext[:4] == 'text':
                e=1
            else:
                e=0 
        print(name) # uncomment this statement if bad request 400 occur when uploading
        handle_uploaded_file(f)

        if e == 0:
            with open('storer/upload/file', 'rb+') as f:
                content = "{}".format(base64.b64encode(f.read()).decode())
                commit_message = "Uploaded on {}".format(ctime())
                # print(content)
                # print(content.encode())
                headers = {'Private-Token': access_token, 'Content-Type': 'application/json'}
                data = {"branch": "master", "content": content, "commit_message": commit_message}
                # print(data.encode())
                r = requests.post("https://gitlab.com/api/v4/projects/"+ project_id +"/repository/files/" + name, headers=headers, json=data)
            if r.status_code >= 400:
                return render(request, 'storer/status_upd.html', {'text':"Error {}".format(r.status_code)})
            else:
                return render(request, 'storer/status_upd.html', {'text':'Uploaded'})
        elif e == 1:
            with open('storer/upload/file', 'rb+') as f:
                content = "{}".format(f.read().decode())
                commit_message = "Uploaded on {}".format(ctime())
                # print(content)
                # print(content.encode())
                headers = {'Private-Token': access_token, 'Content-Type': 'application/json'}
                data = {"branch": "master", "content": content, "commit_message": commit_message}
                # print(data.encode())
                r = requests.post("https://gitlab.com/api/v4/projects/"+ project_id +"/repository/files/" + name, headers=headers, json=data)
            if r.status_code >= 400:
                return render(request, 'storer/status_upd.html', {'text':"Error {}".format(r.status_code)})
            else:
                return render(request, 'storer/status_upd.html', {'text':'Uploaded'})


    else:
        return render(request, 'storer/upload.html')


def update(request):
    if request.method == 'POST' and request.FILES:
        f = request.FILES['file']
        name = f.name
        (ext,_) = mimetypes.guess_type(name)
        e=2
        if ext == None:
            e=0
        if e == 2:
            if ext[:4] == 'text':
                e=1
            else:
                e=0 
        print(name) # uncomment this statement if bad request 400 occur when uploading
        handle_uploaded_file(f)

        if e == 0:
            with open('storer/upload/file', 'rb+') as f:
                content = "{}".format(base64.b64encode(f.read()).decode())
                commit_message = "Updated on {}".format(ctime())
                # print(content)
                # print(content.encode())
                headers = {'Private-Token': access_token, 'Content-Type': 'application/json'}
                data = {"branch": "master", "content": content, "commit_message": commit_message}
                # print(data.encode())
                r = requests.put("https://gitlab.com/api/v4/projects/"+ project_id +"/repository/files/" + name, headers=headers, json=data)
            if r.status_code >= 400:
                return render(request, 'storer/status_upd.html', {'text':"Error {}".format(r.status_code)})
            else:
                return render(request, 'storer/status_upd.html', {'text':'Updated'})
        elif e == 1:
            with open('storer/upload/file', 'rb+') as f:
                content = "{}".format(f.read().decode())
                commit_message = "Updated on {}".format(ctime())
                # print(content)
                # print(content.encode())
                headers = {'Private-Token': access_token, 'Content-Type': 'application/json'}
                data = {"branch": "master", "content": content, "commit_message": commit_message}
                # print(data.encode())
                r = requests.put("https://gitlab.com/api/v4/projects/"+ project_id +"/repository/files/" + name, headers=headers, json=data)
            if r.status_code >= 400:
                return render(request, 'storer/status_upd.html', {'text':"Error {}".format(r.status_code)})
            else:
                return render(request, 'storer/status_upd.html', {'text':'Updated'})


    else:
        return render(request, 'storer/upload.html')


def files(request, filename=''):
    headers={"Private-Token": access_token}
    if filename != '':
        r = requests.get("https://gitlab.com/api/v4/projects/"+ project_id +"/repository/tree?path=" + filename, headers=headers)
    else:
        r = requests.get("https://gitlab.com/api/v4/projects/"+ project_id +"/repository/tree", headers=headers)
    
    file = json.loads(r.content.decode())
    # print(file)
    # print(type(file[0]))
    file_names = []
    for fil in file:
        # print(fil['name'])
        if filename != '':
            file_names.append(filename + '/' + fil['name'])
        else:
            file_names.append(fil['name'])
    # print(file_names == file)
    print(file_names)
    # commit_messages = []
    # for name in file_names:
    #     r = requests.get("https://gitlab.com/api/v4/projects/"+ project_id +"/repository/files/" + name + "?ref=master", headers=headers)
    #     file_details = json.loads(r.content.decode())
    #     print(file_details)
    #     last_commit_id = file_details['last_commit_id']
    #     r = requests.get("https://gitlab.com/api/v4/projects/"+ project_id +"/repository/commits/" + last_commit_id, headers=headers)
    #     commit = json.loads(r.content.decode())
    #     print(commit)
    #     commit_messages.append(commit['message'])
    # print(commit_messages)
    number_of_files = range(len(file_names))
    # (name,_) = file_names
    return render(request, 'storer/files.html', {'file_names':file_names, 'number_of_files':number_of_files})

def file_details(request, filename):
    headers={"Private-Token": access_token}
    name = filename.split('/')
    while(len(name) != 1):
        name[-2] = name[-2] + '%2F' + name[-1]
        del(name[-1])
    r = requests.get("https://gitlab.com/api/v4/projects/"+ project_id +"/repository/tree?path=" + name[0], headers=headers)
    details = json.loads(r.content.decode())

    if len(details) == 0:
        r = requests.get("https://gitlab.com/api/v4/projects/"+ project_id +"/repository/files/" + name[0] + "?ref=master", headers=headers)
        file_details = json.loads(r.content.decode())
        print(file_details)
        last_commit_id = file_details['last_commit_id']
        r = requests.get("https://gitlab.com/api/v4/projects/"+ project_id +"/repository/commits/" + last_commit_id, headers=headers)
        commit = json.loads(r.content.decode())
        print(commit)
        commit_message = commit['message']
        return render(request, 'storer/details.html', {'filename':filename, 'commit_message': commit_message})
    else:
        return files(request, filename)

def delete(request, filename):
    commit_message = "Deleted on {}".format(ctime())
    data = {"branch": "master", "commit_message": commit_message}
    headers={"Private-Token": access_token, "Content-Type": "application/json"}
    name = filename.split('/')
    while(len(name) != 1):
        name[-2] = name[-2] + '%2F' + name[-1]
        del(name[-1])
    r = requests.delete("https://gitlab.com/api/v4/projects/"+ project_id +"/repository/files/" + name[0], json=data, headers=headers)
    if r.status_code >= 400:
        return render(request, 'storer/status_upd.html', {'text':"Error {}".format(r.status_code)})
    else:
        return render(request, 'storer/status_upd.html', {'text':'Deleted'})

def download(request, filename):
    headers={"Private-Token": access_token}
    # print(type(filename))
    name = filename.split('/')
    while(len(name) != 1):
        name[-2] = name[-2] + '%2F' + name[-1]
        del(name[-1])
    r = requests.get("https://gitlab.com/api/v4/projects/"+ project_id +"/repository/files/"+ name[0] +"/raw?ref=master", headers=headers)
    (ext,_) = mimetypes.guess_type(filename)
    e=2
    if ext == None:
        e=0
    if e == 2:
        if ext[:4] == 'text':
            e=1
        else:
            e=0
    if e == 1:
        return HttpResponse("{}".format(r.content.decode()))
    elif e == 0:
        print(r.content)
        print(r.content.decode())
        a = base64.b64decode(r.content)
        # print(base64.b64decode(r.content.decode()).decode())
        return HttpResponse(bytes(a))