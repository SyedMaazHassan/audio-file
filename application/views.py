from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.http import HttpResponse
from django.http import JsonResponse
import json


def add_to_playlist(request):
    output = {}
    if not request.user.is_authenticated:
        output['status'] = False
        return JsonResponse(output)

    if request.method == "GET" and request.is_ajax():
        song_id = int(request.GET.get('song_id'))
        playlist_id = int(request.GET.get('playlist_id'))

        # print(f'song_id => {song_id}')
        # print(f'playlist_id => {playlist_id}')
        
        focused_song = song.objects.get(id = song_id)
        focused_playlist = playlist.objects.get(id = playlist_id)

        focused_playlist.songs.add(focused_song)
        focused_playlist.save()

        output['status'] = True
    
        return JsonResponse(output)




def mark_as_favorite(request):
    output = {
        'status': False
    }

    if request.method == "GET" and request.is_ajax():
        song_id = int(request.GET.get('song_id'))

        if song.objects.filter(id = song_id).exists():
            focused_song = song.objects.get(id = song_id)
            focused_song.is_favorite = not focused_song.is_favorite
            focused_song.save()

            output['status'] = True
            output['song_status'] = focused_song.is_favorite
     

    return JsonResponse(output)



def play(request, song_name):
    context = {}
    if song_name != "list":
        song_id = int(song_name.split("-")[0])
    
        if song.objects.filter(id = song_id).exists():
            focused_song = song.objects.get(id = song_id)
            context['song'] = focused_song
        else:
            return redirect("index")

    all_songs = song.objects.filter(added_by = request.user)
    context['allSongs'] = all_songs

    if request.method == "POST":
        playlist_name = request.POST.get("playlistName")

        new_playlist = playlist(
            playlist_name = playlist_name,
            created_by = request.user
        )

        new_playlist.save()

    # fetching all playlists
    all_playlists = playlist.objects.filter(created_by = request.user).order_by("-id")

    context['all_playlists'] = all_playlists
    context['total_playlists'] = all_playlists.count()

    return render(request, 'play.html', context)


def add_song(request):
    if not request.user.is_authenticated:
        return redirect("login")
    
    if request.method == "POST":
        if 'targetfile' in request.FILES and request.FILES['targetfile']:
            song_file = request.FILES['targetfile']
            total_duration = request.POST['total_duration']
            my_prompts = request.POST['prompts']
            my_prompts = json.loads(my_prompts)

            new_song = song(
                song_file = song_file,
                duration = int(total_duration),
                added_by = request.user
            )

            new_song.save()


            for key, value in my_prompts.items():
                prompt_id = int(value['prompt_id'].split("-")[1])
                which_instance = value['instance']

                new_song.all_prompts.create(
                    which_prompt = prompts.objects.get(id = prompt_id),
                    instance = which_instance
                )

            new_song.save()

            messages.info(request, "Song has been added successfully!")

    return redirect("index")


# main page function

def index(request):
    if not request.user.is_authenticated:
        return redirect("login")

    all_songs = song.objects.filter(added_by = request.user).order_by("-id")

    context = {
        'allSongs': all_songs[0:3],
        'totalSongs': all_songs.count(),
        'all_playlists' : playlist.objects.filter(created_by = request.user),
        'all_prompts': prompts.objects.all()
    }
    return render(request, 'main.html', context)


# function for signup

def signup(request):
    if request.method == "POST":
        name = request.POST['name']
        l_name = request.POST['l_name']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        context = {
            "name":name,
            "l_name":l_name,
            "email":email,
            "pass1":pass1,
            "pass2":pass2,
        }
        if pass1==pass2:
            if User.objects.filter(username=email).exists():
                print("Email already taken")
                messages.info(request, "Entered email already in use!")
                context['border'] = "email" 
                return render(request, "signup.html", context)

            user = User.objects.create_user(username=email, first_name=name, password=pass1, last_name=l_name)
            user.save()
            
            return redirect("login")
        else:
            messages.info(request, "Your pasword doesn't match!")
            context['border'] = "password"
            return render(request, "signup.html", context)


    
    return render(request, "signup.html")


# function for login

def login(request):

    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        context = {
            'email': email,
            'password': password
        }
        user = auth.authenticate(username=email, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("index")
        else:
            messages.info(request, "Incorrect login details!")
            return render(request, "login.html", context)
            # return redirect("login")
    else:
        return render(request, "login.html")


# function for logout

def logout(request):
    auth.logout(request)
    return redirect("index")

