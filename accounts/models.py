import datetime
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
	"""
	Model for User Profile
	"""
	user = models.OneToOneField(User, related_name="profile")
	user_image = models.ImageField(upload_to='profile_images', blank=True)
	friends = models.ManyToManyField("self")
	
	def __unicode__(self):
		return u'Profile of user: %s' %self.user.username
		
class OneShotGoal(models.Model):
	"""
	Model for One Shot Goals
	"""
	#Link to a User
	owner = models.ForeignKey(User, blank=True, related_name="oneshotgoal")
	
	#attributes
	title = models.CharField(max_length=75)
	description = models.TextField()
	private = models.BooleanField()
	completed = models.BooleanField()
	date_created = models.DateField(auto_now_add=True)
	date_completed = models.DateField(blank=True, null=True, editable=True)
	last_updated = models.DateField(auto_now=True)
	
	def __unicode__(self):
		return self.name
		
	def get_oneshotgoalbyorder(self):
		if self.oneshotgoal.count():
			return self.oneshotgoal.order_by('order')[0]

def get_upload_path(instance, filename):
	"""
	Renames media upload filepath to user_username/goal_imagename
	"""
	return "user_{username}/{goal}/{file}".format(id=instance.user.username, goal=instance.name.slug, file=filename)

class OneShotImage(models.Model):
	"""
	Image for One Shot Goal
	"""
	goal = models.OneToOneField(OneShotGoal, related_name="oneshotgoalimage")
	image_file = models.ImageField(upload_to=get_upload_path)
	
class OneShotJournal(models.Model):
	"""
	Journal entries for One Shot Goals
	"""
	goal = models.OneToOneField(OneShotGoal, related_name="oneshotgoaljournal")
	entry = models.TextField()
	date = models.DateField(auto_now_add=True)
	
	def __unicode__(self):
		return self.date