from django.contrib import admin

# Register your models here.
# Importing the book from class
from .models import Film

# Registering with the admin - so admin can see it
# Registering the model here so that the admin site can pick it up
admin.site.register(Film)

# make migrations now -- so need to now go to Terminal and run the make migrations commands