# Address keeper
### This is a simple CRUD address book application with some features:
- User authentication
- Google maps integration.
- Error handling with sentry.io implementation (ramazan.testsafiiulin@yahoo.com:LeeerojJenkins123 / email:password)
- SQL queries logging. Use `docker-compose logs -f postgres`
- Tests
- Easy deploy with docker compose
- Black formatting

### **Warning!** This app requires google maps api key! Put `GMAPS_API_KEY="<your_key>"` in the `.settings.toml`.

### Development setup
1. Open the directory you this repo to be cloned.
2. Clone the repo.
```shell
$: git clone git@github.com:HASKADOG/address_keeper.git
```
3. Open the cloned repo.
```shell
$: cd address_keeper
```
4. Initialize and join the virtual environment.
```shell
$: pipenv shell
```
5. Install requirements.
```shell
$: pipenv install
```
6. Set up the postgres credentials and postgres db_name in `docker-compose.yml`.
```
postgres:
image: postgres
volumes:
  - ./data/db:/var/lib/postgresql/data
environment:
  - POSTGRES_DB=CHANGE_ME
  - POSTGRES_USER=CHANGE_ME
  - POSTGRES_PASSWORD=CHANGE_ME
restart: always
ports:
  - "5432:5432"
```
7. Run postgres.   
8.1 Run `$: docker-compose up -d postgres` if you use linux  
8.2 Run `$: docker compose up -d postgres` if you use macos

9. Create environment variables with database credentials.
```shell
$: export POSTGRES_DB=<db>
$: export POSTGRES_USER=<db_user>
$: export POSTGRES_PASSWORD=<db_password>
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
1. Open the directory you this repo to be cloned.
2. Clone the repo.
```shell
$: git clone git@github.com:HASKADOG/address_keeper.git
```
3. Open the cloned repo.
```shell
$: cd address_keeper
```
4. Change the db credentials and superuser credentials in `.env`. The default superuser credentials are `superuser:superuser_password`.
```
POSTGRES_DB=<db>
POSTGRES_USER=<db_user>
POSTGRES_PASSWORD=<db_password>
DJANGO_SUPERUSER_USERNAME="<su_username>"
DJANGO_SUPERUSER_EMAIL="<su_email>"
DJANGO_SUPERUSER_PASSWORD="<su_password>"
```
5. Run containers.   
5.1 Run `$: docker-compose up -d --build` if you use linux  
5.2 Run `$: docker compose up -d --build` if you use macos

Now you have the app running at 0.0.0.0!

P.S.: The `.secrets.toml and .env` should be ignored by git, but I left them for demonstration purposes  
