# Address keeper
### This is a simple CRUD address book application with some features:
- User authentication
- Google maps integration.
- Error handling with sentry.io implementation (ramazan.testsafiiulin@yahoo.com:LeeerojJenkins123 / email:password)
- SQL queries logging. Use `docker-compose logs -f postgres`
- Tests
- Easy deploy with docker compose
- Code formatting using [black](https://pypi.org/project/black/).

### **Warning!** This app requires google maps api key! Put `GMAPS_API_KEY="<your_key>"` in the `.settings.toml`*.

### Development setup
1. Open the directory you want this repo to be cloned.
2. Clone the repo.
```shell
$: git clone git@github.com:HASKADOG/address_keeper.git
```
3. Open the cloned repo.
```shell
$: cd address_book
```
4. Install requirements.
```shell
$: pipenv install
```
5. Join the virtual environment.
```shell
$: pipenv shell
```
6. Set up the postgres credentials and postgres db_name in `.env`.
```
POSTGRES_DB=<db>
POSTGRES_USER=<db_user>
POSTGRES_PASSWORD=<db_password>
```
7. Run postgres.   
8.1 Run `$: docker-compose up -d postgres` if you use linux.  
8.2 Run `$: docker compose up -d postgres` if you use macos.

9. Create environment variables with database credentials from `.env`.
```shell
$: export $(xargs <.env)
```
10. Run migrations.
```shell
$: python manage.py migrate
``` 
11. _**Optional. You can register a new user in the app.**_ Create a superuser. You will be able to use this user to log in the app.
```shell
python manage.py createsuperuser
Username: <enter the username>
Email address: <enter the email>
Password: <enter the password>
Password (again): <enter the password again>
```
12. Start the server.
```shell
$: python manage.py runserver
```
If you see this:
```shell
Django version 4.0.6, using settings 'address_keeper.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```
You can access the app at http://127.0.0.1:8000/ !

### Deployment
1. Open the directory you want this repo to be cloned.
2. Clone the repo.
```shell
$: git clone git@github.com:HASKADOG/address_keeper.git
```
3. Open the cloned repo.
```shell
$: cd address_book
```
4. Change the db credentials and superuser credentials in `.env`. _**The default superuser credentials are `superuser:superuser_password`. You can use them to log in the app**_.
```
POSTGRES_DB=<db>
POSTGRES_USER=<db_user>
POSTGRES_PASSWORD=<db_password>
DJANGO_SUPERUSER_USERNAME="<su_username>"
DJANGO_SUPERUSER_EMAIL="<su_email>"
DJANGO_SUPERUSER_PASSWORD="<su_password>"
```
5. Run containers.   
5.1 Run `$: docker-compose up -d --build` if you use linux.  
5.2 Run `$: docker compose up -d --build` if you use macos.

Now you have the app running at http://0.0.0.0 !

*P.S.: The `.secrets.toml and .env` should be ignored by git, but I left them for demonstration purposes  
