
## Rebuild image and run locally
```
docker-compose up -d
```

## Show logs
```
docker-compose logs {container name}

docker-compose logs web
```

## Useful commands
Important to note, all django commands (`manage.py`) should be run inside the web container. To get inside the django container you can run:
```
docker-compose exec web bash
```

### Create Migrations
```
python manage.py makemigrations
```

### Run Migrations
For all schemas
```
python manage.py migrate_schemas
```

For public schema only
```
python manage.py migrate_schemas --shared
```

### Update requirements dependencies
```
pip freeze > requirements.txt
```

### First Setup commands
First copy the `env.sample` file into `.env` inside `app/` folder:
```
cd app
cp env.sample .env
```

And then, inside the container, run:
```
python manage.py migrate_schemas
python manage.py create_super_user
python manage.py create_root_tenant
python manage.py create_default_client
```

And add the domain entries to `/etc/hosts`
```
127.0.0.1	construx.local
127.0.0.1	client.c.construx.local
127.0.0.1	pad.construx.local
```

### Load initial document_model fixtures (To run this command you need to create a user first)
```
python manage.py load_fixtures -s tenant_2 -- document_model/fixtures/initial.json
```

### Update initial document_model fixtures
```
python manage.py tenant_command dumpdata document_model --indent 2 -s tenant_2 > document_model/fixtures/initial.json
```

### Open Shell under a tenant
```
python manage.py tenant_command shell -s tenant_2
```

### Load Data
```
find . -type f -name 'initial.json' -exec python manage.py loaddata {}\;
```

### RabbitMQ Login
```
guest:guest
```

### Etherpad API Token Setup
To create Etherpad DB on setup:
```
docker-compose exec -u postgres db psql -c "create database etherpad;"
```

To get the API_KEY value (should be set in `ETHERPAD_API_KEY` env variable)
```
docker compose exec etherpad bash -c "cat APIKEY.txt"
```

To manually set the APIKEY.txt value:
```
docker-compose exec etherpad bash
echo -n "mysecretapikey" > APIKEY.txt
```