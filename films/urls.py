# Add the imports for the views and the path for the index/list view:
from django.urls import path
from .views import FilmListView

urlpatterns = [
  path('', FilmListView.as_view()),
]
