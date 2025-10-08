### Need to update sections (after Day 1 portion of Notes of this README) to reflect films-api and not books-api
**Currently working on both books-api and films-api to get more practice building Django backend api.**

<hr>

# Django Films App - Using Restful Routes & Serializer <br>
**Using restful routes & serializer (React) instead of HTML Templates since it is used more widely currently in the world per Tristan Hall**

<hr>

## Setting up the Django Films Api app. (Day 1 portion of Notes)

1. Create a directory for the application in your projects directory:

   ```py
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

```py
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

```py
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

```py
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

```py
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

```py
from rest_framework import serializers
from .models import Film
```

- Build out the serializer. Here we define the model that the JSON will be using and specify which fields to look at.

```py
class FilmSerializer(serializers.ModelSerializer):
  class Meta:
    model = Film
    fields = '__all__'
```

- Move into views.py and delete the default imports
- Add the following imports:

```py
from rest_framework.views import APIView # this imports rest_frameworks APIView that we'll use to extend to our custom view
from rest_framework.response import Response # Response gives us a way of sending a http response to the user making the request, passing back data and other information
from rest_framework import status # status gives us a list of official/possible response codes

from .models import Film
from .serializers import FilmSerializer
```

- Build out views.py to return all data eg. ListView:

```py
class FilmListView(APIView):

  def get(self, _request):
    films = Film.objects.all()
    serialized_films = FilmSerializer(films, many=True)
    return Response(serialized_films.data, status=status.HTTP_200_OK)
```

- Make a new file called urls.py . Add the imports for the views and the path for the index/list view:

```py
from django.urls import path
from .views import FilmListView

urlpatterns = [
  path('', FilmListView.as_view()),
]
```

- inside project/urls.py add to urlpatterns :
- remember to update import to add **include** as well as path

```py
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
<hr>



## Part Two - Go to Day Two Steps of notes for building an api

**Follow Day Two Steps - Per Lesson in class original materials materials** <br><br>
**This part below is using the django-books-api code and needs to be transformed into django-films-api code. Just fyi.**

## DJANGO API - CREATE & SHOW

1. In `books/views.py`, let's add another method to the BookListView class which will handle POST requests.

Add this under the get function:

```py
    def post(self, request):
        book_to_add = BookSerializer(data=request.data)
        try:
            book_to_add.is_valid()
            book_to_add.save()
            return Response(book_to_add.data, status=status.HTTP_201_CREATED)
        # exceptions are like a catch in js, but if we specify an exception like we do below then the exception thrown has to match to fall into it
        # For example the below is the exception thrown when we miss a required field
        # link: (this documentation entry is empty but shows it exists) https://docs.djangoproject.com/en/4.0/ref/exceptions/#django.db.IntegrityError
        except Exception as e:
            print('ERROR')
            # the below is necessary because two different formats of errors are possible. string or object format.
            # if it's string then e.__dict__ returns an empty dict {}
            # so we'll check it's a dict first, and if it's empty (falsey) then we'll use str() to convert to a string
            return Response(e.__dict__ if e.__dict__ else str(e), status=status.HTTP_422_UNPROCESSABLE_ENTITY)
```

At this point, the whole books/views.py should look like this:

```py
from rest_framework.views import APIView # this imports rest_frameworks APIView that we'll use to extend to our custom view
from rest_framework.response import Response # Response gives us a way of sending a http response to the user making the request, passing back data and other information
from rest_framework import status # status gives us a list of possible response codes


from .models import Book
from .serializers import BookSerializer

class BookListView(APIView):

  def get(self, _request):
    books = Book.objects.all()
    serialized_books = BookSerializer(books, many=True)
    return Response(serialized_books.data, status=status.HTTP_200_OK)

  def post(self, request):
    book_to_add = BookSerializer(data=request.data)
    try:
        book_to_add.is_valid()
        book_to_add.save()
        return Response(book_to_add.data, status=status.HTTP_201_CREATED)
    # exceptions are like a catch in js, but if we specify an exception like we do below then the exception thrown has to match to fall into it
    # For example the below is the exception thrown when we miss a required field
    # link: (this documentation entry is empty but shows it exists) https://docs.djangoproject.com/en/4.0/ref/exceptions/#django.db.IntegrityError
    except Exception as e:
        print('ERROR')
        # the below is necessary because two different formats of errors are possible. string or object format.
        # if it's string then e.__dict__ returns an empty dict {}
        # so we'll check it's a dict first, and if it's empty (falsey) then we'll use str() to convert to a string
        return Response(e.__dict__ if e.__dict__ else str(e), status=status.HTTP_422_UNPROCESSABLE_ENTITY)
```

Because the BookListView is associated with the /books endpoint, simply adding the post function to the BookListView is enough to be able to now create new books through our API. Try it in postman.

2. Now let's work on the "Show" page. We will call it `BookDetailView`.

Let's add the new BookDetailView class underneath the BookListView.
We are also going to need another import at the top of the file. Add this to the imports section at the top of books/views.py:

```py
from rest_framework.exceptions import NotFound # This provides a default response for a not found
```

and then add the serializer underneath the BookListView:

```py
class BookDetailView(APIView):
    def get(self, _request, pk):
        try:
            # different API methods https://docs.djangoproject.com/en/4.0/ref/models/querysets/#methods-that-do-not-return-querysets
            book = Book.objects.get(pk=pk)
            serialized_book = BookSerializer(book)
            return Response(serialized_book.data, status=status.HTTP_200_OK)
        except Book.DoesNotExist:
            raise NotFound(detail="🆘 Can't find that book!")
```

At this point, the whole file should look like this:

```py
from rest_framework.views import APIView # this imports rest_frameworks APIView that we'll use to extend to our custom view
from rest_framework.response import Response # Response gives us a way of sending a http response to the user making the request, passing back data and other information
from rest_framework import status # status gives us a list of possible response codes
from rest_framework.exceptions import NotFound # This provides a default response for a not found

from .models import Book
from .serializers import BookSerializer

class BookListView(APIView):

  def get(self, _request):
    books = Book.objects.all()
    serialized_books = BookSerializer(books, many=True)
    return Response(serialized_books.data, status=status.HTTP_200_OK)

  def post(self, request):
    book_to_add = BookSerializer(data=request.data)
    try:
        book_to_add.is_valid()
        book_to_add.save()
        return Response(book_to_add.data, status=status.HTTP_201_CREATED)
    # exceptions are like a catch in js, but if we specify an exception like we do below then the exception thrown has to match to fall into it
    # For example the below is the exception thrown when we miss a required field
    # link: (this documentation entry is empty but shows it exists) https://docs.djangoproject.com/en/4.0/ref/exceptions/#django.db.IntegrityError
    except Exception as e:
        print('ERROR')
        # the below is necessary because two different formats of errors are possible. string or object format.
        # if it's string then e.__dict__ returns an empty dict {}
        # so we'll check it's a dict first, and if it's empty (falsey) then we'll use str() to convert to a string
        return Response(e.__dict__ if e.__dict__ else str(e), status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class BookDetailView(APIView):
    def get(self, _request, pk):
        try:
            # different API methods https://docs.djangoproject.com/en/4.0/ref/models/querysets/#methods-that-do-not-return-querysets
            book = Book.objects.get(pk=pk)
            serialized_book = BookSerializer(book)
            return Response(serialized_book.data, status=status.HTTP_200_OK)
        except Book.DoesNotExist:
            raise NotFound(detail="🆘 Can't find that book!")
```

2. We need to add a route so that we can specify the book ID that we want to retrieve (that pk=pk is talking about the primary key/id). But let's have a look at how Django handles things if we make a request to a url that doesn't exist yet. Try to make a get request to `/books/1` and see what happens.

3. Let's add the url to the books/urls.py so that it can use the BookDetailView to handle this endpoint. Go to books/urls.py and add the BookDetailView to the the imports and then add the following path to the urlpatterns list:

```py
path('<int:pk>/', BookDetailView.as_view()),
```

so the whole urls.py file should look like this:

```py
from django.urls import path
from .views import BookListView, BookDetailView

urlpatterns = [
  path('', BookListView.as_view()),
  path('<int:pk>/', BookDetailView.as_view()),
  # the above <int:pk> is known as a captured value - it works the same as a placeholder in react/express: ":id"
  # It's made up of two parts:
  # on the left is the path converter - in this case we've specified an integer or "int"
  # on the right is the placeholder - in this case pk but could be anything
  # the path converter is optional, but you should use it to ensure it's the type you expect
  # without it, the captured value would be written like: <pk>
]
```

4. Try testing the endpoint again with a valid book id and you should see the data returned in postman/insomnia. Try it with an invalid book ID and you'll see that our error handling is working!

5. So far, everything is working, BUT - there's something in our code that isn't great. In our BookDetailView get function, we get a book from the database, serialise it and return it. We also handle the errors if we can't find the book. All of these steps are just the FIRST PARTS of what needs to happen with other actions. For example - if we were going to update a book, we would need to get it, serialise it, return it and handle errors if that book didn't exist, and only then would we be able to update the book and save it back to the database. So in the interest in making our code DRY and not repeating ourselves, let's move some of these steps into a reusable function.

We are going to end up creating a new function inside our BookDetailView which will be called get_book and then we will use this function inside the existing get function. Then we can use get_book inside our update and delete functions too.

Let's create our new get_book function as the first function in the BookDetialView:

```py
    # This will be used by all of the routes
    def get_book(self, pk):
        try:
            return Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            raise NotFound(detail="🆘 Can't find that book!")
```

And then let's update our get function to use the get_show function:

```py
    def get(self, _request, pk):
        book = self.get_book(pk=pk) # using key word arguments here
        # querying using a primary key is always going to return a single result.
        # this will never be a list, so no need to add many=True on the serializer
        serialized_book = BookSerializer(book)
        return Response(serialized_book.data, status=status.HTTP_200_OK)
```


<hr>
<hr>

## Part Three - Go to Day Three Steps of notes for building an api

**Follow new notes entititled day-2(1).md in downloads**
- Updating notes for myself and correcting them from class notes as much as possible:

1. From the root of the project, run the startapp command to start a new "author" app

```sh
django-admin startapp authors
```

2. Register the authors app in the project/settings.py file in the "INSTALLED_APPS" list.

```py

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'books',
    'authors'
]
```

3. Now let's create the author model.

```py
from django.db import models

class Author(models.Model):
    def __str__(self):
        return f'{self.name}'

    name = models.TextField(max_length=300)
```

4. And now let's update the book model to have an author from the authors table, rather than free text.

```py
from django.db import models

# Create your models here.
class Book(models.Model):
    def __str__(self):
        return f'{self.title} - {self.author}'

    # models.CharField is the data type and means "string"
    title = models.CharField(max_length=80, unique=True)
    author = models.ForeignKey(
      "authors.Author",
      related_name = "books",
      on_delete = models.CASCADE
    )
    genre = models.CharField(max_length=60)
    year = models.FloatField()
```

5. Drop and re-create the database the database.

```sh
dropdb books-api
createdb books-api
```

6. python manage.py makemigrations && python manage.py migrate.

7. Create superuser - python manage.py createsuperuser

8. Register the model in authors/admin.py

```py
from django.contrib import admin
# Register your models here.
from .models import Author
admin.site.register(Author)
```

```py
from django.contrib import admin
from .models import Author

# Register your models here.
admin.site.register(Author)
```

9. python manage.py runserver - go into the admin site and you can make a book and an author

10. Make and serializers.py file in the authors folder and put this in it:
So in authors folder, create file serialisers.py first. Then this is the code:

```py
from rest_framework import serializers
from .models import Author

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'
```

11. Now let's create a PopulatedBookSerializer underneath the BookSerializer:
(This is in the books app in serializer.py under BookSerializer.)

```py
from rest_framework import serializers
from .models import Book
from authors.serializers import AuthorSerializer

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class PopulatedBookSerializer(BookSerializer):
    author = AuthorSerializer()
```

12. And finally, let's update the books views so that when we fetch all books, we use the BookSerializer, but when we get a single book, we use the PopulatedBookSerializer, so we get more information (in this case, the info about the author)

- SO NOW NEED TO GO IN BOOKS TO VIEWS.PY AND IMPORT POPULATEDBOOKSERIALIZER & ADD serialized_book = PopulatedBookSerializer(book) second to last line change BookSerializer to PopulatedBookSerializer.



```py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound # This provides a default response for a not found

from .models import Book
from .serializers import BookSerializer, PopulatedBookSerializer #add this here

# Create your views here.

class BookListView(APIView):

    # handle a GET request in the BookListView
    def get(self, _request):
        # go to the database and get all the books
        books = Book.objects.all()
        # translate the books from the database to a usable form
        serialized_books = BookSerializer(books, many=True)
        # return the serialized data and a 200 status code
        return Response(serialized_books.data, status=status.HTTP_200_OK)

    def post(self, request):
        book_to_add = BookSerializer(data=request.data)
        try:
           book_to_add.is_valid()
           book_to_add.save()
           return Response(book_to_add.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print("Error")
            # the below is necessary because two different formats of errors are possible. string or object format.
            # if it's string then e.__dict__ returns an empty dict {}
            # so we'll check it's a dict first, and if it's empty (falsey) then we'll use str() to convert to a string
            return Response(e.__dict__ if e.__dict__ else str(e), status=status.HTTP_422_UNPROCESSABLE_ENTITY)

class BookDetailView(APIView):

    # custom method to retrieve a book from the DB and error if it's not found
    def get_book(self, pk):
        try:
            return Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            raise NotFound(detail="Can't find that book")

    def get(self, _request, pk):
        try:
            book = Book.objects.get(pk=pk)
            serialized_book = PopulatedBookSerializer(book) #just change this here to PopulatedBookSerializer
            return Response(serialized_book.data, status=status.HTTP_200_OK)
        except Book.DoesNotExist:
            raise NotFound(detail="Can't find that book")
```

Try it out in postman - call all books and you should see the author is a number, but when you call a single book, the author is populated.

## Comments

```sh
django-admin startapp comments
```

2. Register the authors app in the project/settings.py file in the "INSTALLED_APPS" list.

```py
'comments',
```

## Application definition

```py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'books',
    'authors',
    'comments
]
```

3. Create the Comment model

```py
from django.db import models

# Create your models here.

class Comment(models.Model):
    def __str__(self):
        return f'{self.text} - {self.book}'
    text = models.TextField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    book = models.ForeignKey(
        "books.Book",
        related_name = "comments",
        on_delete=models.CASCADE
    )
```

4. Register the Comment model in the admin app

```py
from django.contrib import admin

# Register your models here.
from .models import Comment
admin.site.register(Comment)
```

5. GOOD PRACTICE TO MAKE MIGRATIONS AFTER CREATE MODEL; HOWEVER, CAN MAKE MIGRATIONS LATER DOWN THIS LIST AS PER #7
- Makemigrations and migrate, then runserver and make sure you can see/create comments in the admin app (browser)

6. Create a comments serializer:
Create serializer.py in comments app. Then add the below code: 

```py
from rest_framework import serializers
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
```

6. Update the PopulatedBookSerializer to add the comments:
DO THIS BY GOING TO THE BOOKS APP AND THE SERIALIZER FILE IN serializers.py and add the following:

```py
from rest_framework import serializers
from .models import Book
from authors.serializers import AuthorSerializer
from comments.serializers import CommentSerializer #ADD THIS HERE

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class PopulatedBookSerializer(BookSerializer):
    author = AuthorSerializer()
    comments = CommentSerializer(many=True) #ADD THIS HERE
```

7. Make your migrations.
- python manage.py makemigrations 
- python manage.py migrate
- python3 manage.py runserver


8. Migrate (see 7 above)

9. start the app with runserver (see 7 above)

## Adding the URLs

Let's start with the authors app.
- Create a file urls.py - and add this info:

```py
from django.urls import path
from .views import AuthorListView

urlpatterns = [
    path('', AuthorListView.as_view()),
]
```

1. Views - create an authors list view:

```py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound # This provides a default response for a not found

from .models import Author
from .serializers import AuthorSerializer

# Create your views here.

class AuthorListView(APIView):

    # handle a GET request in the BookListView
    def get(self, _request):
        # go to the database and get all the authors
        authors = Author.objects.all()
        # translate the books from the database to a usable form
        serialized_authors = AuthorSerializer(authors, many=True)
        # return the serialized data and a 200 status code
        return Response(serialized_authors.data, status=status.HTTP_200_OK)

    def post(self, request):
        author_to_add = AuthorSerializer(data=request.data)
        try:
           author_to_add.is_valid()
           author_to_add.save()
           return Response(author_to_add.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print("Error")
            # the below is necessary because two different formats of errors are possible. string or object format.
            # if it's string then e.__dict__ returns an empty dict {}
            # so we'll check it's a dict first, and if it's empty (falsey) then we'll use str() to convert to a string
            return Response(e.__dict__ if e.__dict__ else str(e), status=status.HTTP_422_UNPROCESSABLE_ENTITY)
```

2. Create the authors/urls.py file and populate it:

```py
from django.urls import path
from .views import AuthorListView

# http://localhost:8000/authors/
urlpatterns = [
    path('', AuthorListView.as_view()),
]
```

3. Now add the authors routes to the prject urls:

```py
"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('books/', include('books.urls')),
    path('authors/', include('authors.urls')),
]
```

4. You should be able to now test getting all the authors and creating an author in Postman.


<hr>

```py
ADDTL INFO TRISTAN DIDN'T TYPE OUT:

A COMMENT NEEDS TO BE ASSOCIATED WITH A USER SO...
STOPPING HERE AND WILL LEARN AUTHORIZATION AND THEN COME BACK TO THIS.
(as of October 2nd, 2025 lecture)
```
**STILL NEED TO DO:**
- Implement the comments
- Authentication so that users can register/login
- Handle tokens & all the JOT stuff
- Circular dependencies & how to structure my code to avoid this
- Build a simple front end so we can get back to React land, to have a working full-stack application to then work off for your project.

<hr>
<hr>
# Authentication
# Adding Authentication With a Custom User

We want to use jwt token for auth again but django isn't set up for this as defualt.
We also want to add secure route functionality like we've done before.
We want to register and login.

1. Start a new app called jwt_auth

```sh
django-admin startapp jwt_auth
```

2. Add the app the in INSTALLED_APPS in `project/settings.py`

```py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'books',
    'authors',
    'comments',
    'jwt_auth',
]
```

3. Django already has a user model, it's how we add a superuser. In `project/settings.py`, add the below to specifiy which model we intend to use:

- **PUT THIS UNDERNEATH INSTALLED APPS.**

```py
AUTH_USER_MODEL = 'jwt_auth.User'
```

**ADDING OUR NEW MODEL NEXT AS PER BELOW**

4. in `jwt_auth/models.py` we'll add our new model.

django already has password, password confirmation & username so we don't need to add them. It doesnt make email required so want to change that. By defining these fields we make them required.

By default, django already has a user model (the one for superusers etc) and it's called the AbstractUser
we want to build on top of that.

```py
from django.db import models
from django.contrib.auth.models import AbstractUser # user model that already exists in django

class User(AbstractUser): # we extend the AbstractUser and add the fields that we want for our users
    email = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    profile_image = models.CharField(max_length=300)
```

5. makemigrations and migrate
- python manage.py makemigrations
- python manage.py migrate  

There will be an error on migrate because django is confused here because a user exists but we've just created a new model. The migration history at this point is a little bit all over the place so let's reset so no migrations exist. We only have to do this as we're doing auth last. Usually, you would build authentication first, so we wouldn't need to do this bit in the real world.

<br>
**Because learning this through General Assembly, they are having us do the Authentication later. In real world scenarios, we will be doing Authentication first so we won't run into this problem. However, next couple steps are required for this project and how we are learning.**


6. Create backups:
- (After you do #6 below, there will be a seeds.json file in your folder with the backups. It will be a seed json file with all of my books from my database.)

```sh
python manage.py dumpdata books --output books/seeds.json --indent=2
python manage.py dumpdata authors --output authors/seeds.json --indent=2
python manage.py dumpdata comments --output comments/seeds.json --indent=2
```

7. Drop database:

```sh
dropdb books-api
```

8. Delete migration files: - in each app, open the migrations folder and delete everything except the `__init__.py` files . In each app there is a trace of all migrations of anything you've ever created. So what we want to do it reset all the migrations.

- **So for this you have to go into the migrations files for authors, books, comments and... AND delete the 001_ 002_ files that are there.**

9. Recreate db:

```sh
create books-api
```

10. Then can Make migrations and migrate (after created new database)
- python manage.py makemigrations
- python manage.py migrate 


11. Create superuser:

```sh
python manage.py createsuperuser
```

12. Register User model on the admin app. get_user_model is a method that when invoked returns whatever model that our app is set up to use. In settings.py we specified that we will use our own custom model 'jwt_auth.User' so this is what will be returned.

- GO TO admin.py in folder of jwt_auth and do the following:

Put this in the `jwt_auth/admin.py` file:

```py
from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()
admin.site.register(User) # then we'll register this to the admin as usual

```

13. NOW GOING TO INSTALL SOME JWT PACKAGES

13. Users to be created through the API

```sh
pipenv install pyjwt
```

# going to deal with token before login/register

14. Create a new file in the jwt_auth folder called authentication.py
- **In jwt_auth, create authentication.py and add the following code:

fill out auth file with:

```py
from rest_framework.authentication import BasicAuthentication
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from django.conf import settings  # show secret key in settings.py
import jwt

User = get_user_model()

# BasicAuthentication has stuff built in like password & email validation


# assertain users permissions # requests come through here # assign a permission level # if valid token -> given permission to see secure things
class JWTAuthentication(BasicAuthentication):
    def authenticate(self, request):  # check requets has token and return if so

        header = request.headers.get('Authorization')

        # if no headers, just return to end the request
        if not header:
            return None

        # if token is wrong format, throw error
        if not header.startswith('Bearer'):
            raise PermissionDenied(detail='Invalid Auth token')

        # pass all checks, store token in variable
        token = header.replace('Bearer ', '')

        # get payload with users id from token & algorithms
        try:
            # can show https://jwt.io again so they can see the alg and the secret
            # HS256 is default, it will be this unless we specify a different alg when we sign the token
            payload = jwt.decode(token, settings.SECRET_KEY,
                                 algorithms=['HS256'])

            # find user with that id in db
            user = User.objects.get(pk=payload.get('sub'))
            print('USER ->', user)
            # issue with the token

            # if we get an error when decoding it will fall into the below exception
        except jwt.exceptions.InvalidTokenError:
            raise PermissionDenied(detail='Invalid Token')

        # If the user does not exist it will fall into the below
        except User.DoesNotExist:
            raise PermissionDenied(detail='User Not Found')

        # if all good, return user and the token
        return (user, token)
```
**IF WANT MORE INFORMATION, SEE NOTES IN JWT AUTHENTICATION.PY.**


14. We now need to add REST_FRAMEWORK intothe `project/settings.py`:

The first part is telling Django to render in JSON, although the serializers are doing this for us we can confirm here.
Second part is telling rest_framework and django that we are using the JWTAuthentication class we just created as the default
- ADD THE BELOW CODE UNDER LINE OF: ROOT_URLCONF = 'project.urls'

```py
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],

    'DEFAULT_AUTHENTICATION_CLASSES': [
        'jwt_auth.authentication.JWTAuthentication'
        ],
}
```
**Explanation of rest framework in settings.py (above) in django-books-api page notes.**

15. Next we'll control who see's what:

- In `books/views.py` add imports for permissions from rest_frameworks.permissions.
- IsAuthenticatedOrReadOnly has method that enforces every method except GET to throw a permissions error
- there's another one too, IsAuthenticated, that applies to all methods

add this import the the books/views.py file: <br>
**!!! BUT NOTE: # This means the user needs to be signed in to do something and use IsAuthenticated - for safety-tracker/ But if you want the ability for anyone to see books, can use this one.**


```py
from rest_framework.permissions import IsAuthenticatedOrReadOnly # IsAuthenticatedOrReadOnly specifies that a view is secure on all methods except get requests
```


16. inside BooksListView, as the first line inside the class, add:

```py
# If you want this to be only for authenticated uses... then do IsAuthenticated instead.
permission_classes = (IsAuthenticatedOrReadOnly, ) # tuple, requires trailing comma
```
SO IT WILL LOOK LIKE THIS:
```py
class BookListView(APIView):
  # If you want this to be only for authenticated uses... then do IsAuthenticated instead.
  permission_classes = (IsAuthenticatedOrReadOnly)
```



17. Let's create the serializer for a user.

Here we'll create our serializer but add a new function called validate to run our validation checks

```py
from rest_framework import serializers
from django.contrib.auth import get_user_model, password_validation # function runs when creating superuser
from django.contrib.auth.hashers import make_password # hashes password for us
from django.core.exceptions import ValidationError

User = get_user_model()

class UserSerializer(serializers.ModelSerializer): # never converted to json and returned in response
    password = serializers.CharField(write_only=True) # write_only=True ensures never sent back in JSON
    password_confirmation = serializers.CharField(write_only=True)

    # validate function is going to:
    # check our passwords match
    # hash our passwords
    # add back to database
    def validate(self, data): # data comes from the request body
        print('DATA',data)
        # remove fields from request body and save to vars
        password = data.pop('password')
        password_confirmation = data.pop('password_confirmation')

        # check if they match
        if password != password_confirmation:
            raise ValidationError({'password_confirmation': 'do not match'})

        # checks if password is valid, comment this out so it works
        try:
            password_validation.validate_password(password=password)
        except ValidationError as err:
            print('VALIDATION ERROR')
            raise ValidationError({ 'password': err.messages })

        # hash the password, reassigning value on dict
        data['password'] = make_password(password)

        print('DATA ->', data)
        return data

    class Meta:
        model = User
        fields = '__all__'
```

**FOR MORE INFO ABOUT THE ABOVE FUNCTION, PLEASE SEE DJANGO-BOOKS-API IN JWT FILE UNDER SERIALIZER FOR MORE NOTES**

