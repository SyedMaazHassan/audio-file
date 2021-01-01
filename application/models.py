from django.db import models
from datetime import datetime
from django.contrib.auth.models import User, auth
# Create your models here.

# python manage.py makemigrations
# python manage.py migrate
# python manage.py runserver


class song(models.Model):
    song_file = models.FileField(upload_to = 'music')
    added_time = models.DateTimeField(default = datetime.now())
    added_by = models.ForeignKey(User, on_delete = models.CASCADE)

    def song_name(self):
        return str(self.song_file).split('music/')[1]