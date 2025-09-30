# We need a serializer to convert python objects into JSON.

from rest_framework import serializers
from .models import Film


# Build out the serializer. 
# We need a serializer to convert python objects into JSON (as per Tristan's notes).
# Here we define the model that the JSON will be using and specify which fields to look at:
class FilmSerializer(serializers.ModelSerializer):
  class Meta:
    model = Film
    # This part below converts all fields from json to sql.
    fields = '__all__'


