from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from urllib.request import urlopen, Request
from time import ctime

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
        # print(name) # uncomment this statement if bad request 400 occur when uploading
        handle_uploaded_file(f)
        with open('storer/upload/file.txt', 'rb+') as f:
            content = '"{}"'.format(f.read())
            commit_message = '"Uploaded on {}"'.format(ctime())
            # print(content)
            # print(content.encode())
            data = '{"branch": "master", "content": ' + content + ', "commit_message": '+ commit_message +'}'
            # print(data.encode())
            a = Request("https://gitlab.com/api/v4/projects/"+ project_id +"/repository/files/"+ name, data=data.encode(), headers={"Private-Token": access_token, "Content-Type": "application/json"}, method="POST")
            urlopen(a)
        return render(request, 'storer/status_upd.html', {'text':'Uploaded'})
    else:
        return render(request, 'storer/upload.html')

def update(request):
    if request.method == 'POST' and request.FILES:
        f = request.FILES['file']
        name = f.name
        # print(name)
        handle_uploaded_file(f)
        with open('storer/upload/file.txt', 'rb+') as f:
            content = '"{}"'.format(f.read())
            commit_message = '"Updated on {}"'.format(ctime())
            # print(content)
            # print(content.encode())
            data = '{"branch": "master", "content": ' + content + ', "commit_message": '+ commit_message +'}'
            # print(data.encode())
            a = Request("https://gitlab.com/api/v4/projects/"+ project_id +"/repository/files/"+ name, data=data.encode(), headers={"Private-Token": access_token, "Content-Type": "application/json"}, method="PUT")
            urlopen(a)
        return render(request, 'storer/status_upd.html', {'text':'Updated'})
    else:
        return render(request,'storer/upload.html')

def files(request):
    a = Request("https://gitlab.com/api/v4/projects/"+ project_id +"/repository/tree", headers={"Private-Token": access_token}, method="GET")
    f = urlopen(a)
    import json
    file = json.loads(f.read().decode())
    # print(type(file[0]))
    file_names = []
    for fil in file:
        # print(fil['name'])
        file_names.append(fil['name'])
    commit_messages = []
    for name in file_names:
        a = Request("https://gitlab.com/api/v4/projects/"+ project_id +"/repository/files/" + name + "?ref=master", headers={"Private-Token": access_token}, method="GET")
        f = urlopen(a)
        file_details = json.loads(f.read().decode())
        # print(file_details)
        last_commit_id = file_details['last_commit_id']
        a = Request("https://gitlab.com/api/v4/projects/"+ project_id +"/repository/commits/" + last_commit_id, headers={"Private-Token": access_token}, method="GET")
        f = urlopen(a)
        commit = json.loads(f.read().decode())
        commit_messages.append(commit['message'])
    # print(commit_messages)
    number_of_files = range(len(file_names))
    return render(request, 'storer/files.html', {'file_names':file_names, 'commit_messages':commit_messages, 'number_of_files':number_of_files})

def file_details(request, filename):
    # return HttpResponse("this will show the details of {}".format(filename))
    return render(request, 'storer/details.html', {'filename':filename})

def delete(request, filename):
    commit_message = '"Deleted on {}"'.format(ctime())
    data = '{"branch": "master", "commit_message": '+ commit_message +'}'
    a = Request("https://gitlab.com/api/v4/projects/"+ project_id +"/repository/files/" + filename, data=data.encode(), headers={"Private-Token": access_token, "Content-Type": "application/json"}, method="DELETE")
    urlopen(a)
    return render(request, 'storer/status_upd.html', {'text':'Deleted'})

def download(request, filename):
    a = Request("https://gitlab.com/api/v4/projects/"+ project_id +"/repository/files/"+ filename +"/raw?ref=master", headers={"Private-Token": access_token}, method="GET")
    f = urlopen(a)
    return HttpResponse("{}".format(f.read().decode()))