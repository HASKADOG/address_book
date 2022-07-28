# address_keeper
### This is a simple CRUD address book application with some features:
- User authentication
- Google maps integration
- Error handling with sentry.io implementation (ramazan.testsafiiulin@yahoo.com:LeeerojJenkins123 / email:password)
- SQL console logging (in DEBUG mode only)


### Set up guid
```
git clone git@github.com:HASKADOG/address_keeper.git
cd address_keeper
docker-compose up -d --build
```
After that you need to process the database migration
```
docker ps
```
You'll get this output
```
CONTAINER ID   IMAGE                             COMMAND                  CREATED          STATUS          PORTS                                       NAMES
1454ee557d0a   address_keeper_nginx              "/docker-entrypoint.…"   54 seconds ago   Up 52 seconds   0.0.0.0:80->80/tcp, :::80->80/tcp           address_keeper-nginx-1
b4f98dcd0749   address_keeper_address_keeper_d   "gunicorn address_ke…"   54 seconds ago   Up 53 seconds   0.0.0.0:8000->8000/tcp, :::8000->8000/tcp   address_keeper-address_keeper_d-1
a1726cbd3e8e   postgres                          "docker-entrypoint.s…"   2 hours ago      Up 53 seconds   0.0.0.0:5432->5432/tcp, :::5432->5432/tcp   address_keeper-postgres-1
```
Choose the address_keeper_address_keeper_d container id and 
```
docker exec -t -i b4f98dcd0749 bash
python manage.py migrate
exit
```
Here we go!

Now you have the app running at 0.0.0.0!
