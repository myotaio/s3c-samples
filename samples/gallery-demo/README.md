# Myota S3C Gallery App Sample

## Pre-requisitions

### Install Dependent Packages

```Bash
root %> yum groupinstall "Development tools"
root %> yum install postgresql-server
root %> yum install python3-devel
root %> yum install postgresql-devel
```

### Postgresqal Configuration

Init database

```Bash
root %> postgresql-setup initdb
root %> systemctl start postgresql
```

Setup Postgres Admin and Role Creation

```Bash
root %> passwd postgres
Changing password for user postgres.
New password: 
Retype new password: 
passwd: all authentication tokens updated successfully.

root %> su - postgres

postgres %> createuser -s YOUR_USERNAME

postgres %> createdb YOUR_DBNAME

postgres %> psql

postgres=# alter user "YOUR_USERNAME" with password 'xxxxxxxxxxxxx';
ALTER ROLE

postgres=# \dg
List of roles
Role name |                   Attributes                   | Member of 
-----------+------------------------------------------------+-----------
YOUR_USERNAME  | Superuser, Create role, Create DB              | {}
postgres  | Superuser, Create role, Create DB, Replication | {}

postgres=# \q

postgres %> exit
```

### Config Password Auth to Postgres

Change authentication method from ident to trust

```Conf
# /var/lib/pgsql/data/pg_hba.conf
...
# TYPE  DATABASE        USER            ADDRESS                 METHOD

# "local" is for Unix domain socket connections only
local   all             all                                     peer
# IPv4 local connections:
host    all             all             127.0.0.1/32            trust
# IPv6 local connections:
host    all             all             ::1/128                 trust
```

## Django Setup

Assume this project code is located at DJANGO_PROJECT_PATH.

Change params in DJANGO_PROJECT_PATH/s3cgallery/settings.py

```Python
# DJANGO_PROJECT_PATH/s3cgallery/settings.py

…
ALLOWED_HOSTS = ['https://gallery-demo.qa.myota.cloud/']

…
# Database
$ https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'YOUR_DBNAME',
        'USER': 'YOUR_USERNAME',
        'PASSWORD': 'YOUR_PASSWORD',
        'HOST': 'localhost',
        'PORT': '',
    }
}

…

S3_CREDENTIAL = {
    'AccessKeyId': 'S3_ACCESS_KEY_ID',
    'SecretAccessKey': 'S3_SECRET_ACCESS_KEY'
}
S3_BUCKET_NAME = "S3_BUCKET_NAME"
 
S3C_CREDENTIAL = {
    'AccessKeyId': 'MYOTA_ACCESS_KEY_ID',
    'SecretAccessKey': 'MYOTA_SECRET_ACCESS_KEY'
}
S3C_BUCKET_NAME = "MYOTA_BUCKET_NAME"
S3C_ENDPOINT_URL = "YOUR_S3C_ENDPOINT_URL"
```

Install pip packages.
Assume you are already in DJANGO_PROJECT_PATH

```Bash
%> python3 -m venv ./venv
%> . venv/bin/activate
venv %> pip install -r requirements.txt
```

Create tables and add django super user

```Bash
venv %> ./manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, imagestore, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying auth.0012_alter_user_first_name_max_length... OK
  Applying imagestore.0001_initial... OK
  Applying sessions.0001_initial... OK

venv %> ./manage.py createsuperuser
Username (leave blank to use 'DJANGO_ADMIN_USERNAME'): 
Email address: 
Password: 
Password (again): 
Superuser created successfully.
```

### Run Django Development Server

```Bash
venv %> ./manage.py runserver
```
