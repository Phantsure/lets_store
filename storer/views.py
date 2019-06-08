from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from urllib.request import urlopen, Request

from .secret import access_key
from .functions import handle_uploaded_file

# Create your views here.
def index(request):
    if(request.GET.get('uploadButton')):
        return HttpResponseRedirect(reverse('storer:upload'))
    elif(request.GET.get('updateButton')):
        return HttpResponseRedirect(reverse('storer:update'))
    elif(request.GET.get('deleteButton')):
        return HttpResponseRedirect(reverse('storer:delete'))
    elif(request.GET.get('downloadButton')):
        return HttpResponseRedirect(reverse('storer:download'))
    else:
        return render(request, 'storer/index.html')

def upload(request):
    if request.method == 'POST' and request.FILES:
        f = request.FILES['file']
        handle_uploaded_file(f)
        with open('storer/upload/file.txt', 'rb+') as f:
            content = '"{}"'.format(f.read())
            print(content)
            print(content.encode())
            data = '{"branch": "master", "content": ' + content + ', "commit_message": "create a new test file"}'
            print(data.encode())
            a = Request("https://gitlab.com/api/v4/projects/12659010/repository/files/file%2Etxt", data=data.encode(), headers={"Authorization": access_key, "Content-Type": "application/json"}, method="POST")
            urlopen(a)
        return HttpResponse("uploaded")
    else:
        return render(request, 'storer/upload.html')

def update(request):
    if request.method == 'POST' and request.FILES:
        f = request.FILES['file']
        handle_uploaded_file(f)
        with open('storer/upload/file.txt', 'rb+') as f:
            content = '"{}"'.format(f.read())
            print(content)
            print(content.encode())
            data = '{"branch": "master", "content": ' + content + ', "commit_message": "updated file"}'
            print(data.encode())
            a = Request("https://gitlab.com/api/v4/projects/12659010/repository/files/file%2Etxt", data=data.encode(), headers={"Authorization": access_key, "Content-Type": "application/json"}, method="PUT")
            urlopen(a)
        return HttpResponse("updated")
    else:
        return render(request,'storer/upload.html')

def delete(request):
    data = b'{"branch": "master", "commit_message": "file deleted"}'
    a = Request("https://gitlab.com/api/v4/projects/12659010/repository/files/file%2Etxt", data=data, headers={"Authorization": access_key, "Content-Type": "application/json"}, method="DELETE")
    urlopen(a)
    return HttpResponse("file is deleted")

def download(request):
    a = Request("https://gitlab.com/api/v4/projects/12659010/repository/files/file%2Etxt/raw?ref=master", headers={"Authorization": access_key}, method="GET")
    f = urlopen(a)
    return HttpResponse("{}".format(f.read().decode()))