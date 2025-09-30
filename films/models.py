from django.db import models

# Create your models here.
# As per Tristan's notes: Fields are required by default so no need to specify.
# Changed Book to Film, and changed author to director (for most ease in coding along)
class Film(models.Model):
  def __str__(self):
    return f'{self.title} - {self.director}'
  title = models.CharField(max_length=80, unique=True)
  director = models.CharField(max_length=50)
  genre = models.CharField(max_length=60)
  year = models.FloatField()