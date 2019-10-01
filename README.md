# lets_store

## To run webapp:
``` 
python3 manage.py makemigrations 
python3 manage.py migrate
python3 manage.py runserver
```
This will start the localhost(127.0.0.1:8000)

## To run backup service:
* place backup.py file in /usr/bin/
* after placing backup.service file /lib/systemd/system/
```sudo systemctl daemon-reload
sudo systemctl enable backup.service
sudo systemctl start backup.service
```
