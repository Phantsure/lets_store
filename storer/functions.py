def handle_uploaded_file(f):  
    with open('storer/upload/file.txt', 'wb+') as destination:
        for chunk in f.chunks():  
            destination.write(chunk)