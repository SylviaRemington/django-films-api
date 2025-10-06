# Django Films App - Using Restful Routes & Serializer <br>
**Using restful routes & serializer (React) instead of HTML Templates since it is used more widely currently in the world per Tristan Hall**

<hr>

## Setting up the Django Films Api app. (Day 1 portion of Notes)

1. Create a directory for the application in your projects directory:
   ```
   mkdir ~/code/ga/projects/django-films-api
   cd ~/code/ga/projects/django-films-api
   ```

2. Install the package by running pipenv install django. After this you should have 2 files: Pipfile and Pipfile.lock. These are essentially the same as a package.json and a package-lock.json in a node/express app.
- **pipenv install django**

3. Enter the shell by running pipenv shell
- **pipenv shell**

4. To start a project run django-admin startproject project .
- **django-admin startproject project .**
- You should see that a folder called project has been created in the project directory, along with a manage.py file.

5. Run pipenv install psycopg2-binary (this is a db-adapter which allows us to use postgresql)
- **pipenv install psycopg2-binary**
- (If you look in your Pipfile now, you should see that you have 2 dependencies: django and psycopg2-binary.)
- **pipenv install autopep8 --dev**
- (original code says -dev, but to make it work need to do --dev)
  
6. (he has 8 in lesson) Now run this to start postgres brew services start postgresql@16
- **brew services start postgresql@16**

7. THEN START YOUR VSCODE: **code .**
  
## VSCode
- Head to your project/settings.py file in the project folder
- Replace the DATABASES object with the following:

```
DATABASES = { # added this to use postgres as the database instead of the default sqlite. do this before running the initial migrations or you will need to do it again
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'films-api', **(CHANGE THE NAME YOU'D LIKE TO USE FOR YOUR DATABASE: E.G. films-api or books-api)**
        'HOST': 'localhost',
        'PORT': 5432
    }
}
```

<hr>

### Terminal
- Make a database by running: **createdb films-api**
- **(This name must match the name of the db in the settings.py file)**
- Run the server: **python3 manage.py runserver**
- (**Depending on which Python you have, use that. I'm using python3 so need to use that to run the server!**)

### If:
- If you get an error about importing Django, run this: pip install django psycopg2-binary

### If Not:
**RUNNING MIGRATIONS BELOW HERE:**
- Notice the first error that comes up and nudge students that they will need to run migrations.
- **Stop the server ctrl+c (Need to stop the server in order to run migrations.)**
- **Migrate the app: python3 manage.py migrate**
- **Run the server again: python3 manage.py runserver**
- No Errors! Boom.
**(You should now be able to see the landing page if you navigate to http://localhost:8000 in the browser)**
  
- **Stop the server ctrl+c**
- **Create superuser: python3 manage.py createsuperuser**
- (For creating superuser part we are making a very basic username, email address, and pswd so that the class can troubleshoot easily; however, for real-life situations, this is where you make a more in-depth username and password)
- **Now start a new app: django-admin startapp films**

<hr>
  
### VSCode
- In settings.py in the project folder, **add name of the app to the INSTALLED_APPS array - e.g. 'films', (at the end of the INSTALLED_APPS)**
- Move to models.py in the films folder
- Create the films model:
```
class Film(models.Model):
  def __str__(self):
    return f'{self.title} - {self.director}'
  title = models.CharField(max_length=80, unique=True)
  director = models.CharField(max_length=50)
  genre = models.CharField(max_length=60)
  year = models.FloatField()
```
- (Fields are required by default so no need to specify)

### Now:
- Go to the apps admin.py and import your model: from .models import Film
- Then register your site: admin.site.register(Film)
(Registering the model here so the admin site can pick it up)

My example here:
```
from django.contrib import admin

# Register your models here.
# Importing the film from class
from .models import Film

# Registering with the admin - so admin can see it
# Registering the model here so that the admin site can pick it up
admin.site.register(Film)
```

### Terminal
- Run: **python3 manage.py makemigrations**
- Then run: **python3 manage.py migrate**
- Restart the server: **python3 manage.py runserver**
- **Navigate to http://localhost:8000/admin and login to create some database entries**
- Add in a function to format the string to make it more readable: (if this doesn’t work, check that the function is indented into the class)
  **Question for Tristan or Luke: For the part above line 115 regarding adding a function to format the string, where are we doing this and why?**
  
## REST

### Terminal
- **Stop the server ctrl+c**
- Install the django rest framework: **pipenv install djangorestframework**
  
## VSCode
Register this in our project/settings.py INSTALLED_APPS : ’rest_framework’ above our own app

```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'films'
]
```

- Inside the films folder create a new file called **serializers.py**

- We need a serializer to convert python objects into JSON.

- In the serializers.py file add these imports:

```
from rest_framework import serializers
from .models import Film
```

- Build out the serializer. Here we define the model that the JSON will be using and specify which fields to look at.

```
class FilmSerializer(serializers.ModelSerializer):
  class Meta:
    model = Film
    fields = '__all__'
```

- Move into views.py and delete the default imports
- Add the following imports:

```
from rest_framework.views import APIView # this imports rest_frameworks APIView that we'll use to extend to our custom view
from rest_framework.response import Response # Response gives us a way of sending a http response to the user making the request, passing back data and other information
from rest_framework import status # status gives us a list of official/possible response codes

from .models import Film
from .serializers import FilmSerializer
```

- Build out views.py to return all data eg. ListView:

```
class FilmListView(APIView):

  def get(self, _request):
    films = Film.objects.all()
    serialized_films = FilmSerializer(films, many=True)
    return Response(serialized_films.data, status=status.HTTP_200_OK)
```

- Make a new file called urls.py . Add the imports for the views and the path for the index/list view:

```
from django.urls import path
from .views import FilmListView

urlpatterns = [
  path('', FilmListView.as_view()),
]
```

- inside project/urls.py add to urlpatterns :
- remember to update import to add **include** as well as path

```
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('films/', include('films.urls')),
]
```

<hr>

## Links to check code via localhost:8000, localhost:8000/admin/, and POSTMAN

- Run code at http://127.0.0.1:8000/ (once set up and doing python3 manage.py runserver) - http://localhost:8000 - you can see this landing page after setting up migrations <br>

- Run http://localhost:8000/admin/ (once fully set up) & **can add Films in Django Admin**: <br>
<img width="1045" height="368" alt="DJANGO ADMIN" src="https://github.com/user-attachments/assets/c6e5342d-ea72-4b17-b4c3-cc3295ac45e1" />

- Also after all is set up, you can go to Postman and set up a new Films Collection, create a GET request with http://localhost:8000/films and make sure it's working as per this screenshot below! Yuuuus! <br>
<img width="1022" height="858" alt="Postman Get Request for Films" src="https://github.com/user-attachments/assets/bda9da2b-028c-4cb9-a15a-c3a9165839ce" />

<hr>

## Part Two - Go to Day-Two-Steps of notes for building an api

**Follow Day Two Steps - Per Lesson in class original materials materials**

## Part Three - Go to Day-Three-Steps of notes for building an api

**Follow new notes entititled day-2(1).md in downloads**