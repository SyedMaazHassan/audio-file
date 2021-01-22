from django.db import models
from datetime import datetime
from django.contrib.auth.models import User, auth
# Create your models here.

# python manage.py makemigrations
# python manage.py migrate
# python manage.py runserver


class prompts(models.Model):
    prompts_name = models.CharField(max_length = 50)
    audio_file = models.FileField(upload_to = "prompts")
    uploaded_at = models.DateTimeField(default = datetime.now())

class prompts_time(models.Model):
    which_prompt = models.ForeignKey(prompts, on_delete = models.CASCADE)
    instance = models.IntegerField()


class song(models.Model):
    song_file = models.FileField(upload_to = 'music')
    added_time = models.DateTimeField(default = datetime.now())
    duration = models.IntegerField(default = 0)
    all_prompts = models.ManyToManyField(prompts_time, null = True, blank = True)
    added_by = models.ForeignKey(User, on_delete = models.CASCADE)
    is_favorite = models.BooleanField(default = False)

    def song_name(self):
        return str(self.song_file).split('music/')[1]

    def get_extension(self):
        song_name = self.song_name()
        return song_name.split(".")[-1]

    def get_wrapped_name(self):
        division = 30
        song_name = self.song_name()

        if len(song_name) > division:
            song_name = song_name[0: division]+" ..."
            return song_name
        else:
            return song_name

    def get_more_small_text(self):
        division = 10
        song_name = self.song_name()

        if len(song_name) > division:
            song_name = song_name[0: division]+" ..."
            return song_name
        else:
            return song_name



class playlist(models.Model):
    playlist_name = models.CharField(max_length = 255)
    songs = models.ManyToManyField(song, null = True, blank = True)
    created_at = models.DateTimeField(default = datetime.now())
    created_by = models.ForeignKey(User, on_delete = models.CASCADE, null = True, blank = True)

    def get_song_list(self):
        print(self.songs)
        return self.songs