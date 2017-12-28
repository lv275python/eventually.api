# eventually.api

## Description
This is the source code of the service which is called "eventually". This app provides flexible and effective event management. "Eventually" helps to manage events, group people into the teams, share responsibilities, and remind about future events.

## Technologies
* Python (3.6.3)
* PostgreSQL (9.5.9)
* Django (1.11.6)
* NodeJS (6.11.4)

## Install
For the next steps of service installation, you will need setup of Ubuntu OS

### Install and configure PostgreSQL server on your local machine:
```
sudo apt-get install postgresql postgresql-contrib
sudo -u postgres psql postgres

postgres=# \password
Enter new password:
Enter it again:

postgres=# CREATE DATABASE your_custom_db_name;

postgres=# \q
```


### Go to the cloned repository and install requirement project's packages
```
pip install -r requirements.txt
```

* Go to the `eventually/eventually` project directory and create your own local_settings.py in the folder with settings.py and configure correct database connection.
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'your_custom_db_name',
        'USER': 'your_custom_db_user',
        'PASSWORD': 'your_password_for_user_above',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'example.eventually'
EMAIL_HOST_PASSWORD = '123456'
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = 'example.eventually@gmail.com'

JWT_TOKEN_KEY = 'any secret word'
JWT_ALGORITHM = 'HS256'

AWS_S3_ACCESS_KEY_ID = 'AWS_S3_ACCESS_KEY_ID'
AWS_S3_SECRET_ACCESS_KEY = 'AWS_S3_SECRET_ACCESS_KEY'
AWS_STORAGE_BUCKET_NAME = 'AWS_STORAGE_BUCKET_NAME'
```

* Create file `eventually.log` in `/var/log/` directory, And add user permissions to that file.
```
sudo touch /var/log/eventually.log

sudo chown -R $USER:$USER /var/log/eventually.log
```

* Go to the folder with `manage.py` file and run migrate files
```
python manage.py migrate
```

### For installing new npm packages in terminal and run WebPack you should be in the directory where `pacage.json` is located and type:

```
sudo apt install nvm

nvm install --lts

npm install
```

## Run Project
### WebPack
Go to the folder with `pacage.json` file
* For build
``` 
npm run build 
```
* For watch
```
npm start
```


### Django
Go to the folder with `manage.py` file, run eventually.api 
```
python manage.py runserver
```
