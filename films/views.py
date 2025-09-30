# Adding following imports from Tristan Hall's Day 1 steps of Django-Books-API and converting it for Films
from rest_framework.views import APIView # this imports rest_frameworks APIView that we'll use to extend to our custom view
from rest_framework.response import Response # Response gives us a way of sending a http response to the user making the request, passing back data and other information
from rest_framework import status # status gives us a list of official/possible response codes

from .models import Film
from .serializers import FilmSerializer


# Create your views here.
class FilmListView(APIView):

  def get(self, _request):
    films = Film.objects.all()
    serialized_films = FilmSerializer(films, many=True)
    return Response(serialized_films.data, status=status.HTTP_200_OK)

