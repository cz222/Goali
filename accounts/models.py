import datetime
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

#USER PROFILE MODEL
class UserProfile(models.Model):
	"""
	Model for User Profile
	"""
	user = models.OneToOneField(User, related_name="profile")
	user_image = models.ImageField(upload_to='profile_images', blank=True)
	friends = models.ManyToManyField("self")
	
	def __unicode__(self):
		return u'Profile of user: %s' %self.user.username


#ONE SHOT GOAL MODELS		
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
		return self.title

def get_upload_path(instance, filename):
	"""
	Renames media upload filepath to user_username/goal_imagename
	"""
	return "user_{username}/{goal}/{file}".format(id=instance.user.username, goal=instance.name.slug, file=filename)

class OneShotImage(models.Model):
	"""
	Image for One Shot Goal
	"""
	goal = models.ForeignKey(OneShotGoal, blank=True, related_name="oneshotgoalimage")
	image_file = models.ImageField(upload_to=get_upload_path)
	
class OneShotJournal(models.Model):
	"""
	Journal entries for One Shot Goals
	"""
	goal = models.ForeignKey(OneShotGoal, blank=True, related_name="oneshotgoaljournal")
	entry = models.TextField(max_length=500)
	date = models.DateField(auto_now_add=True)
	
	def __unicode__(self):
		return self.entry

class OneShotNote(models.Model):
	"""
	Notes for One Shot Goals
	"""
	goal = models.ForeignKey(OneShotGoal, blank=True, related_name="oneshotgoalnote")
	note = models.TextField(max_length=300)
	date = models.DateField(auto_now_add=True)
	
	def __unicode__(self):
		return self.note

		
#MILESTONE GOAL OPTIONS
class MilestoneGoal(models.Model):
	"""
	Model for Milestone Goals
	"""
	#Link to a User
	owner = models.ForeignKey(User, blank=True, related_name="milestonegoal")
	
	#attributes
	title = models.CharField(max_length=75)
	description = models.TextField()
	private = models.BooleanField()
	completed = models.BooleanField()
	date_created = models.DateField(auto_now_add=True)
	date_completed = models.DateField(blank=True, null=True, editable=True)
	last_updated = models.DateField(auto_now=True)
	
	def __unicode__(self):
		return self.title

class MilestoneGoalJournal(models.Model):
	"""
	Journal entries for Milestone Goals
	"""
	#Link to Milestone Goal
	goal = models.ForeignKey(MilestoneGoal, blank=True, related_name="milestonegoaljournal")
	entry = models.TextField(max_length=500)
	date = models.DateField(auto_now_add=True)
	
	def __unicode__(self):
		return self.entry
		
class MilestoneGoalNote(models.Model):
	"""
	Notes for One Shot Goals
	"""
	goal = models.ForeignKey(MilestoneGoal, blank=True, related_name="milestonegoalnote")
	note = models.TextField(max_length=300)
	date = models.DateField(auto_now_add=True)
	
	def __unicode__(self):
		return self.note
		
class MilestoneGoalImage(models.Model):
	"""
	Image for Milestone Goal
	"""
	goal = models.ForeignKey(MilestoneGoal, blank=True, related_name="milestonegoalimage")
	image_file = models.ImageField(upload_to=get_upload_path)
	
class Milestone(models.Model):
	"""
	Model for Milestone Goals
	"""
	#Link to a Milestone Goal
	goal = models.ForeignKey(MilestoneGoal, blank=True, related_name="milestone")
	
	#attributes
	title = models.CharField(max_length=75)
	description = models.TextField()
	private = models.BooleanField()
	completed = models.BooleanField()
	date_created = models.DateField(auto_now_add=True)
	date_completed = models.DateField(blank=True, null=True, editable=True)
	last_updated = models.DateField(auto_now=True)
	
	def __unicode__(self):
		return self.title

class MilestoneNote(models.Model):
	"""
	Notes for One Shot Goals
	"""
	milestone = models.ForeignKey(Milestone, blank=True, related_name="milestonenote")
	note = models.TextField(max_length=300)
	date = models.DateField(auto_now_add=True)
	
	def __unicode__(self):
		return self.note
		
class MilestoneImage(models.Model):
	"""
	Image for Milestone Goal
	"""
	milestone = models.ForeignKey(Milestone, blank=True, related_name="milestoneimage")
	image_file = models.ImageField(upload_to=get_upload_path)
		
class SubMilestone(models.Model):
	"""
	Model for Milestone Sub Goals
	"""
	#Link to a Milestone
	milestone = models.ForeignKey(Milestone, blank=True, related_name="submilestone")
	
	#attributes
	title = models.CharField(max_length=75)
	description = models.TextField()
	private = models.BooleanField()
	completed = models.BooleanField()
	date_created = models.DateField(auto_now_add=True)
	date_completed = models.DateField(blank=True, null=True, editable=True)
	last_updated = models.DateField(auto_now=True)
	
	def __unicode__(self):
		return self.title

class SubMilestoneNote(models.Model):
	"""
	Notes for One Shot Goals
	"""
	submilestone = models.ForeignKey(SubMilestone, blank=True, related_name="submilestonenote")
	note = models.TextField(max_length=300)
	date = models.DateField(auto_now_add=True)
	
	def __unicode__(self):
		return self.note
		
class SubMilestoneImage(models.Model):
	"""
	Image for Milestone Goal
	"""
	submilestone = models.ForeignKey(SubMilestone, blank=True, related_name="submilestoneimage")
	image_file = models.ImageField(upload_to=get_upload_path)
		
class SubSubMilestone(models.Model):
	"""
	Model for Milestone Sub Goals
	"""
	#Link to a Sub Milestone
	submilestone = models.ForeignKey(SubMilestone, blank=True, related_name="subsubmilestone")
	
	#attributes
	title = models.CharField(max_length=75)
	description = models.TextField()
	private = models.BooleanField()
	completed = models.BooleanField()
	date_created = models.DateField(auto_now_add=True)
	date_completed = models.DateField(blank=True, null=True, editable=True)
	last_updated = models.DateField(auto_now=True)
	
	def __unicode__(self):
		return self.title

class SubSubMilestoneNote(models.Model):
	"""
	Notes for One Shot Goals
	"""
	subsubmilestone = models.ForeignKey(SubSubMilestone, blank=True, related_name="submilestonenote")
	note = models.TextField(max_length=300)
	date = models.DateField(auto_now_add=True)
	
	def __unicode__(self):
		return self.note
		
class SubSubMilestoneImage(models.Model):
	"""
	Image for Milestone Goal
	"""
	subsubmilestone = models.ForeignKey(SubSubMilestone, blank=True, related_name="submilestoneimage")
	image_file = models.ImageField(upload_to=get_upload_path)