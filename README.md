# Restaurant Menu Votting App
This is a simple project to use Company needs internal service for its’ employees which helps them to make a decision on lunch place. Each restaurant will be uploading menus using the system every day over API and employees will vote for the menu before leaving for lunch.

# Technology used
Docker, Python. Django, Django Rest Framework, PostgreSQL

# Start the project
To launch the project you have to install [Docker](https://docs.docker.com/engine/install/) and [Make](https://www.gnu.org/software/make/) in your PC. Then :

1. Clone the project by `git clone https://github.com/localboy/restaurant-menu.git`
2. Go to project directory `cd restaurant-menu`
3. Run `make build`. It will install required packages.
4. Run `make test` to run the tests of the project.
5. Run `make start`. It will start the container in background.
6. Run `make superuser` to create super user.
7. Please read [Makefile](https://github.com/localboy/restaurant-menu/blob/master/Makefile) for more commands.

# Authentication
The project is used [Djoser](https://github.com/sunscrapers/djoser) for Authentication. Also used Token based authentication. 
1. To create user go to [http://127.0.0.1:8000/api/auth/users/](http://127.0.0.1:8000/api/auth/users/)
2. To get token [http://127.0.0.1:8000/api/auth/token/login/](http://127.0.0.1:8000/api/auth/token/login/)

