# terraform-manager

## How to run

### API
```
git clone https://github.com/tar-xzvff/terraform-manager.git
pip install -r requirements.txt
cd terraform_manager/
python manage.py migrate
python manage.py runserver
```

## Deployment
### 0. Preparation of MQ (Redis) and DB(postgres)
Please prepare MQ (Redis) and DB (postgres).

### 1. Configure settings.py
Please change the setting to your environment.
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'terraform_manager',
        'USER': '<DB_USERNAME>',
        'PASSWORD': '<DB_PASSWORD>',
        'HOST': '<YOUR_DB_SERVER_IP_ADDRESS>',
        'PORT': '<YOUR_DB_SERVER_PORT>',
    }
}

BROKER_URL = 'redis://<YOUR_REDIS_SERVER_IP_ADDRESS>:6379/0'
CELERY_RESULT_BACKEND = 'redis://<YOUR_REDIS_SERVER_IP_ADDRESS>:6379/0'
```


### 2. Creating and starting an API container

### 3. Creating and starting a worker container
Execute the following command in the project root directory.

Create
```
docker build -t terraform-manager-worker  -f docker/worker/Dockerfile .
```

Run
```
docker run -it terraform-manager-worker
```