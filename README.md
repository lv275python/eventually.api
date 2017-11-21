# eventually.api

## Description
This is the source code of the service which is called "eventually". This app provides flexible and effective event management. "Eventually" helps to manage events, group people into the teams, share responsibilities, and remind about future events.

## Technologies
* Python (3.6.3)
* PostgreSQL (9.5.9)
* Django (1.11.6)

## Install
For the next steps of service installation, you will need setup of Ubuntu OS

* Install and configure PostgreSQL server on your local machine:
```
sudo apt-get install postgresql postgresql-contrib
sudo -u postgres psql postgres
```

* Go to the cloned repository and install requirement project's packages
```
pip install -r requirements.txt
```

* Go to the eventually project directory and create your own local_settings.py in the folder with settings.py and configure correct database connection.
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

```

* Create file `eventually.log` in `/var/log/` directory, And add user permissions to that file.
```
sudo touch /var/log/eventually.log

sudo chown -R $USER:$USER /var/log/eventually.log
```

* Go to the folder with manage.py file and run eventually.api
```
python manage.py runserver
```
