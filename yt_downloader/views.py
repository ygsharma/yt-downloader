from django.shortcuts import render, redirect
from pytube import *
from django.conf import settings
from django.http import HttpResponse

import requests
from isodate import parse_duration


from .forms import DownloadForm


def index(request):
    # template = loader.get_template('index.html')
    # return HttpResponse(template.render())
    return render(request, 'home.html')

def download_page_url(request):

    if request.method == 'POST':

        form = DownloadForm(request.POST or None)

        if form.is_valid():
            video_url = form.cleaned_data.get("url")
            # handling mobile version urls and shortened url format
            if 'm.' in video_url:
                video_url = video_url.replace(u'm.', u'')
           
            elif 'youtu.be' in video_url:
                video_id = video_url.split('/')[-1]
                video_url = "https://youtube.com/watch?v=" + video_id

            if len(video_url.split("=")[-1]) != 11:
                return search_results(request)
                # return HttpResponse('Enter correct url.')
        
            
            video = YouTube(video_url)
            # streams = video.streams
            streams = video.streams.filter(progressive=True)
            resolutions = []
            for s in streams:
                resolutions.append(s.resolution)

            video_streams = []
            for s in streams:
                video_streams.append({
                    'resolution': s.resolution
                })
            # .get_lowest_resolution()
            # stream.download()

            return render(request, 'video.html', { 'resolutions': resolutions })
    return render(request, 'home.html')


def download_page_id(request, id):

    if request.method == 'GET':
        video_url = "https://youtube.com/watch?v=" + id

        yt = YouTube(video_url)
        # streams = video.streams
        video_streams = yt.streams.filter(progressive=True)
        audio_streams = yt.streams.filter(type="audio")


        videos = []
        for s in video_streams:
            videos.append([s.resolution, int(s.filesize_mb)])

        audios = []
        for s in audio_streams:
            audios.append([s.abr, int(s.filesize_mb)])

        video_url =  'https://www.googleapis.com/youtube/v3/videos'
        video_params = {
                'key': settings.YOUTUBE_API_KEY,
                'part': 'snippet, contentDetails',
                'id': id,
            }

        res_video = requests.get(video_url, params=video_params)
        result = res_video.json()['items'][0]

        context = {
            'title': result['snippet']['title'],
            'duration': int(parse_duration(result['contentDetails']['duration']).total_seconds()//60),
            'thumbnail': result['snippet']['thumbnails']['high']['url'],
            'audios': audios,
            'videos': videos,
            'video_id': id
        }

        return render(request, 'video.html', context)
    return render(request, 'home.html')


def search_results(request):

    if request.method == 'POST':

        form = DownloadForm(request.POST or None)

        if form.is_valid():

            query = form.cleaned_data.get('url')

            if query == '':
                query = 'Popular english songs'

            search_url = 'https://www.googleapis.com/youtube/v3/search'
            video_url =  'https://www.googleapis.com/youtube/v3/videos'

            search_params = {
                'part': 'snippet',
                'q': query,
                'key': settings.YOUTUBE_API_KEY,
                'max_results': 50,
                'type': 'video'
            }

            res_search = requests.get(search_url, params=search_params)

            search_results = res_search.json()['items']

            video_ids = []
            for result in search_results:
                video_ids.append(result['id']['videoId'])


            video_params = {
                'key': settings.YOUTUBE_API_KEY,
                'part': 'snippet, contentDetails',
                'id': ','.join(video_ids),
                'max_results': 50,
            }

            res_video = requests.get(video_url, params=video_params)

            video_results = res_video.json()['items']
            videos = []
            for result in video_results:
                video_data = {
                    'title': result['snippet']['title'],
                    'id': result['id'],
                    'duration': int(parse_duration(result['contentDetails']['duration']).total_seconds()//60),
                    'thumbnail': result['snippet']['thumbnails']['high']['url']
                }

                videos.append(video_data)

            context = {
                'videos': videos
            }

            return render(request, 'search.html', context)
        
    return render(request, 'home.html')




    


