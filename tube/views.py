from django.http import HttpResponse, HttpResponseRedirect

from django.shortcuts import render
from stream.settings import STATIC_URL, MEDIA_URL
from .models import Video, Category, User
from .forms import UploadFileForm
import random

# imports for video manipulation
from moviepy.editor import VideoFileClip
import os

# imports for user authentication

from .loginForm import UserLoginForm, UserRegisterForm
'''

user Login, Logout and Register functions

'''

def login_view(request):

	title = "Log In"

	form = UserLoginForm(request.POST or None)
	if form.is_valid():
		username = form.cleaned_data.get('username')
		request.session['username'] = username

		return HttpResponseRedirect('/index/')

	else:
		context = {

				'form'      : form.as_p(),
				'title'     : title,
			}

		return render(request, 'tube/login.html', context)


def register_view(request):
	title = "Register"
	form = UserRegisterForm(request.POST or None)
	if form.is_valid():
		username = form.cleaned_data.get('username')
		password = form.cleaned_data.get('password')
		email    = form.cleaned_data.get('email')

		user = User(username=username, password=password, email=email)
		user.save()
		return HttpResponseRedirect('/index/')

	return render(request, 'tube/login.html', {'form' : form.as_p() , 'title' : title})



def logout_handler(request):
	try:
		del request.session['username']
	except:
		pass

	return HttpResponseRedirect('/index/')

'''

Home Page 			-: Recent Uploads
					-: Login
					-: Signup (Gmail/Facebook)
					-: Popular

About Page 			-: About Me and its secrets :)

Categories Page 	-: All the Categories of videos available
'''

def home_view(request):
	'''
create 				: login
					: signup
					: common video display
					: upload
	'''	


	# try:
	# 	query = request.GET["q"]				# keyword searched by the user
	# 	results = Video.objects.filter(title = query) # match query with the name of the videos in the database	

	# 	context = {

	# 			'range' 	 : list(range(1,4)),
	# 			'STATIC_URL' : STATIC_URL,
	# 			"videos"	 : results,
	# 			'results'    : results 
	# 	}										# variables passed to the index.html


	# 	return render(request, 'tube/index.html',context)
	# except:
	# 	videos = list(Video.objects.filter())
	# 	max_likes = max(list(x.likes for x in videos ))
	# 	context = {

	# 			'range' 	 : list(range(1,4)),
	# 			'STATIC_URL' : STATIC_URL,
	# 			"videos"	 : videos,
	# 			"most_popular": Video.objects.filter(likes= max_likes),
	# 	}										# variables passed to the index.html


	recent_videos = Video.objects.filter().order_by('-added_time')[:3]  # get top 3 videos
	tv_series     = Video.objects.filter(category = Category.objects.get(title='TV Series'))
	educational   = Video.objects.filter(category = Category.objects.get(title='Education'))



	animes = Video.objects.filter(category = Category.objects.get(title='Anime'))
	animes = [x for x in animes]

	# categories = Category.objects.filter() 

	try:
		username = request.session.get('username')
	except:
		username = None

	context = {

			'STATIC_URL' : STATIC_URL,
			'animes'	 : animes[-4:],
			'MEDIA_URL'  : MEDIA_URL,
			'username'   : username,
	   'recent_videos'   : recent_videos,
	       'tv_series'   : tv_series,
	       'educational' : educational,
	}

	return render(request, 'tube/index.html',context)	# display index.html in tube/templates/tube


# open upload.html when run

def upload_view(request, *args, **kwargs):

	form = UploadFileForm()
	
	success = False

	if args:
		success = args[0]



	categories = Category.objects.filter() 

	try:
		username = request.session.get('username')
	except:
		username = None


	context = {

			'STATIC_URL' : STATIC_URL,
			'form'		 : form.as_ul(),
			'success'	 : success,
			'categories' : categories,
			'username'   : username,
	}	


	return render(request, 'tube/upload.html', context)

def handle_uploaded_file(file,title, extension_less_url, extension):

	with open(extension_less_url+extension, 'wb+' ) as destination:
		for chunk in file.chunks():
			destination.write(chunk)
	# for getting  duration of the video file :

	import subprocess
	subprocess.call(['ffmpeg', '-i', extension_less_url + extension, extension_less_url + '.mkv'])



	BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	x = (os.path.join(BASE_DIR,'uploads/'+title+'.mkv'))
	clip = VideoFileClip(x)

	clip.save_frame('uploads/thumbnails/' + title + '.jpg',t=1.00)

	os.remove((os.path.join(BASE_DIR,'uploads/'+title+ extension)))
	return int(clip.duration/60)		# returning duration of video in muinutes


def hadel_uploaded_file_2(file, title):
	pass

def upload_video(request, *args, **kwargs):


	'''
	print(request.POST,request.FILES)

	output:

	request.POST:

		<QueryDict: {
		'description': ['Naruto Episode 1'], 
		'csrfmiddlewaretoken': ['TGpdDeW09rwgi8JJylLbiorpSaaBchMlmN0p8qD6JHeCCoeyZd0kBdzrfsdlf0z8'], '
		title': ['Naruto'], 
		'category': ['Anime']}>

	request.FILES:

		<MultiValueDict: {
		'file': [<TemporaryUploadedFile: <filename>.<extension> (video/x-matroska)>]}>
	'''

	title = request.POST['title']
	videos = [x.title for x in Video.objects.filter()]
	

	while title in videos:
		title = title + random.choice('abcdefghijklimnopqrstuvwxyz123456789')

	file = request.FILES['file']
	import os.path
	filename = file.name
	extension = os.path.splitext(filename)[1]

	extension_less_url = './uploads/' + request.POST['title']

	duration = handle_uploaded_file(file, title, extension_less_url, extension)

	video = Video(title=title,
		    description=request.POST['description'],
			   category=Category.objects.get(title = request.POST['category']),
			        url= extension_less_url + '.mkv',
			  duration = duration
			   )
	video.save()
	

	return upload_view(request,True)






	
def video_play(request, *args, **kwargs):				# page for playing individual videos
	'''
    create					: video playing
							: like
							: share
							: download
	'''

	
	video       = Video.objects.get(title=kwargs['title'])
	next_videos = Video.objects.filter(category = Category.objects.get(title= video.category))
	video.views += 1
	video.save()

	try:
		username = request.session.get('username')
	except:
		username = None

	context = {

			'STATIC_URL' : STATIC_URL,
			 'video'	 : video,
			'MEDIA_URL'  : MEDIA_URL,
			'username'   : username,
			'next_videos': next_videos,
	}	




	return render(request, 'tube/single.html', context)


def about_view(request):	


	context = {

			'STATIC_URL' : STATIC_URL,
	}	

						# about me
	return render(request, 'tube/about.html', context)


def categories_view(request):


	categories = Category.objects.filter() 

	context = {

			'STATIC_URL' : STATIC_URL,
			'categories' : categories,
	}	


	return render(request, 'tube/categories.html', context)



def increase_like(request,*args,**kwargs):

	v = Video.objects.get(pk = kwargs['video_id'])
	v.likes += 1
	v.save()

	return home_view(request)




def search_view(request):
	query = request.POST['q']

	result = Video.objects.filter(title__icontains=query) 

	try:
		username = request.session.get('username')
	except:
		username = None

	context = {

			'STATIC_URL' : STATIC_URL,
			'MEDIA_URL'  : MEDIA_URL,
			'username'   : username,
			'result'     : result,
	}


	return render(request, 'tube/search.html', context)



def category_view(request, **kwargs):
	videos   = Video.objects.filter(category = Category.objects.get(title= kwargs['category']))

	try:
		username = request.session.get('username')
	except:
		username = None

	context = {

			'STATIC_URL' : STATIC_URL,
			'MEDIA_URL'  : MEDIA_URL,
			'username'   : username,
			'category'   :  kwargs['category'],
			'videos'     : videos,
	}

	return render(request, 'tube/category.html', context)
