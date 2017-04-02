from django.db import models
from django.utils.encoding import smart_text
import datetime

# Create your models here.

'''
Making Categories of Video::

# Add Category Option
# Add Video with with details
'''
class Category(models.Model):
	title = models.CharField(max_length=30)				# name of the collection of video


	def __str__(self):
		return smart_text(self.title)


class Video(models.Model):						# contains description of the video
	title = models.CharField(max_length=30)			# title of the video
	description = models.CharField(max_length=200)	# description of the video 
	duration = models.IntegerField(default='30')		# duration of video in minutes(absolute)
	url = models.CharField(max_length=200,)		# the name by which video is saved in the directory
	# image_name = models.CharField(max_length=200, defautl = name) # name of image which is the preview of the Video
	category = models.ForeignKey(Category,on_delete=models.CASCADE)
	likes = models.IntegerField(default=0)
	views = models.IntegerField(default=0)
	added_time = models.DateTimeField(default=datetime.datetime.now)


	def __str__(self):
		return smart_text(self.title)

class User(models.Model):
	username = models.CharField(max_length=50)
	password = models.CharField(max_length=30)
	email    = models.CharField(max_length=50)
	def __str__(self):
		return smart_text(self.username)
