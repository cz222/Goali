import datetime
from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

import json

#USER PROFILE MODEL
class UserProfile(models.Model):
    """Model for User Profile"""
    
    user = models.OneToOneField(User, related_name="profile")
    user_image = models.ImageField(upload_to='profile_images', blank=True)
    friends = models.ManyToManyField("self")
    
    def __unicode__(self):
        return u'Profile of user: %s' %self.user.username

#USER FORUM MODEL
class Forum(models.Model):
    title = models.CharField(max_length=70)
    
    def __unicode__(self):
        return self.title
    
    def num_posts(self):
        return sum([t.num_posts() for t in self.thread_set.all()])
    
    def last_post(self):
        if self.thread_set.count():
            last = None
            for t in self.thread_set.all():
                lst = t.last_post()
                if lst:
                    if not last: last = lst
                    elif lst.created > last.created: last = lst
            return last
        
class Thread(models.Model):
    title = models.CharField(max_length=70)
    created = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, blank=True, null=True)
    forum = models.ForeignKey(Forum, related_name="thread")
    
    def __unicode__(self):
        return unicode(self.creator)+" - "+self.title
    
    def num_posts(self):
        return self.post_set.count()
    
    def num_replies(self):
        return self.post_set.count()-10
    
    def last_post(self):
        if self.post_set.count():
            return self.post_set.order_by("created")[0]

class Post(models.Model):
    title = models.CharField(max_length=60)
    created = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, blank=True, null=True, related_name="post_creator")
    thread = models.ForeignKey(Thread)
    body = models.TextField(max_length=10000)
    
    def __unicode__(self):
        return u"%s - %s - %s" %(self.creator, self.thread, self.title)
    
    def short(self):
        return u"%s - %s\n%s" %(self.creator, self.title, self.created.strftime("%b %d, %I:%M %p"))
    short.allow_tags = True
    
#ADMIN FORUM MODEL
class ForumAdmin(admin.ModelAdmin):
    pass

class ThreadAdmin(admin.ModelAdmin):
    list_display = ["title", "forum", "creator", "created"]
    list_filter = ["forum", "creator"]
    
class PostAdmin(admin.ModelAdmin):
    search_fields = ["title", "creator"]
    list_display = ["title", "thread", "creator", "created"]


#######################One Shot Goal#######################
class OneShotGoal(models.Model):
    """Model for One Shot Goals"""
    
    #Link to a User
    owner = models.ForeignKey(User, blank=True, related_name="oneshotgoal")
    
    #attributes
    title = models.CharField(max_length=75)
    description = models.TextField()
    private = models.BooleanField()
    completed = models.BooleanField()
    date_created = models.DateField(auto_now_add=True)
    date_completed = models.DateTimeField(blank=True, null=True, editable=True)
    last_updated = models.DateField(auto_now=True)
    visual = models.CharField(max_length=70);
    
    def __unicode__(self):
        return self.title

###############################################################################
def get_upload_path(instance, filename):
    """Renames media upload filepath to user_username/goal_imagename"""
    
    return "user_{username}/{goal}/{file}".format(id=instance.user.username, 
        goal=instance.name.slug, file=filename)

    
class OneShotImage(models.Model):
    """Image for One Shot Goal"""
    
    goal = models.ForeignKey(OneShotGoal, blank=True, related_name="oneshotgoalimage")
    image_file = models.ImageField(upload_to=get_upload_path)
    
    
class OneShotJournal(models.Model):
    """Journal entries for One Shot Goals"""
    
    goal = models.ForeignKey(OneShotGoal, blank=True, related_name="oneshotgoaljournal")
    entry = models.TextField(max_length=500)
    title = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    
    def __unicode__(self):
        return self.entry

class OneShotNote(models.Model):
    """Notes for One Shot Goals"""
    
    goal = models.ForeignKey(OneShotGoal, blank=True, related_name="oneshotgoalnote")
    note = models.TextField(max_length=300)
    date = models.DateField(auto_now_add=True)
    
    def __unicode__(self):
        return self.note

#######################Milestone Goal#######################
#Milestone Goal
class MilestoneGoal(models.Model):
    """Model for Milestone Goals"""
    
    #Link to a User
    owner = models.ForeignKey(User, blank=True, related_name="milestonegoal")
    
    #attributes
    title = models.CharField(max_length=75)
    description = models.TextField()
    private = models.BooleanField()
    completed = models.BooleanField()
    date_created = models.DateField(auto_now_add=True)
    date_completed = models.DateTimeField(blank=True, null=True, editable=True)
    last_updated = models.DateField(auto_now=True)
    visual = models.CharField(max_length=70);
    
    def __unicode__(self):
        return self.title

class MilestoneGoalJournal(models.Model):
    goal = models.ForeignKey(MilestoneGoal, blank=True, related_name="milestonegoaljournal")
    entry = models.TextField(max_length=500)
    title = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    
    def __unicode__(self):
        return self.entry

class MilestoneGoalNote(models.Model):
    goal = models.ForeignKey(MilestoneGoal, blank=True, related_name="milestonegoalnote")
    note = models.TextField(max_length=300)
    date = models.DateField(auto_now_add=True)
    
    def __unicode__(self):
        return self.note

#Milestone
class Milestone(models.Model):
    """Model for Milestones"""
    
    #Link to a Milestone Goal
    goal = models.ForeignKey(MilestoneGoal, blank=True, null=True, related_name="milestone")
    milestone = models.ForeignKey('self', blank=True, null=True, related_name="submilestone")
    
    #attributes
    title = models.CharField(max_length=75)
    description = models.TextField()
    private = models.BooleanField()
    completed = models.BooleanField()
    date_created = models.DateField(auto_now_add=True)
    date_completed = models.DateTimeField(blank=True, null=True, editable=True)
    last_updated = models.DateField(auto_now=True)
    parent_id = models.IntegerField(blank=True, null=True, editable=True)
    
    def __unicode__(self):
        return self.title

class MilestoneJournal(models.Model):
    milestone = models.ForeignKey(Milestone, blank=True, related_name="milestonejournal")
    entry = models.TextField(max_length=500)
    title = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    
    def __unicode__(self):
        return self.entry

class MilestoneNote(models.Model):
    milestone = models.ForeignKey(Milestone, blank=True, related_name="milestonenote")
    note = models.TextField(max_length=300)
    date = models.DateField(auto_now_add=True)
    
    def __unicode__(self):
        return self.note

#######################Time One Shot Goal#######################
class TimeOneShotGoal(models.Model):
    """One Shot Goal with a Time Limit"""
    
    #Link to a User
    owner = models.ForeignKey(User, blank=True, related_name="timeoneshotgoal")
    
    #attributes
    title = models.CharField(max_length=75)
    description = models.TextField()
    private = models.BooleanField()
    complete_by = models.DateTimeField(blank=True, null=True, editable=True)
    completed = models.BooleanField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_completed = models.DateTimeField(blank=True, null=True, editable=True)
    last_updated = models.DateField(auto_now=True)
    visual = models.CharField(max_length=70);
    
    def __unicode__(self):
        return self.title

class TimeOneShotJournal(models.Model):
    """Journal entries for Time One Shot Goals"""
    
    goal = models.ForeignKey(TimeOneShotGoal, blank=True, related_name="timeoneshotgoaljournal")
    entry = models.TextField(max_length=500)
    title = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    
    def __unicode__(self):
        return self.entry

class TimeOneShotNote(models.Model):
    """Notes for Time One Shot Goals"""
    
    goal = models.ForeignKey(TimeOneShotGoal, blank=True, related_name="timeoneshotgoalnote")
    note = models.TextField(max_length=300)
    date = models.DateField(auto_now_add=True)
    
    def __unicode__(self):
        return self.note

#######################Time Milestone Goal#######################
#Time Milestone Goal
class TimeMilestoneGoal(models.Model):
    """Main Milestone Goal with a Time Limit."""
    
    #Link to a User
    owner = models.ForeignKey(User, blank=True, related_name="timemilestonegoal")
    
    #attributes
    title = models.CharField(max_length=75)
    description = models.TextField()
    private = models.BooleanField()
    complete_by = models.DateTimeField(blank=True, null=True, editable=True)
    completed = models.BooleanField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_completed = models.DateTimeField(blank=True, null=True, editable=True)
    last_updated = models.DateField(auto_now=True)
    visual = models.CharField(max_length=70);
    
    def __unicode__(self):
        return self.title

class TimeMilestoneGoalJournal(models.Model):
    goal = models.ForeignKey(TimeMilestoneGoal, blank=True, related_name="timemilestonegoaljournal")
    entry = models.TextField(max_length=500)
    title = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    
    def __unicode__(self):
        return self.entry

class TimeMilestoneGoalNote(models.Model):
    goal = models.ForeignKey(TimeMilestoneGoal, blank=True, related_name="timemilestonegoalnote")
    note = models.TextField(max_length=300)
    date = models.DateField(auto_now_add=True)
    
    def __unicode__(self):
        return self.note

#Time Milestone
class TimeMilestone(models.Model):
    """Model for Time Milestones."""
    
    #Link to a Milestone Goal
    goal = models.ForeignKey(TimeMilestoneGoal, blank=True, null=True, related_name="timemilestone")
    milestone = models.ForeignKey('self', blank=True, null=True, related_name="timesubmilestone")
    
    #attributes
    title = models.CharField(max_length=75)
    description = models.TextField()
    private = models.BooleanField()
    complete_by = models.DateTimeField(blank=True, null=True, editable=True)
    completed = models.BooleanField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_completed = models.DateTimeField(blank=True, null=True, editable=True)
    last_updated = models.DateField(auto_now=True)
    
    def __unicode__(self):
        return self.title

class TimeMilestoneJournal(models.Model):
    milestone = models.ForeignKey(TimeMilestone, blank=True, related_name="timemilestonejournal")
    entry = models.TextField(max_length=500)
    title = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    
    def __unicode__(self):
        return self.entry

class TimeMilestoneNote(models.Model):
    milestone = models.ForeignKey(TimeMilestone, blank=True, related_name="timemilestonenote")
    note = models.TextField(max_length=300)
    date = models.DateField(auto_now_add=True)
    
    def __unicode__(self):
        return self.note

#######################Value Goal#######################
class ValueGoal(models.Model):
    """Model for Value Goals. Keeps track of a value over time. Unlike a progress goal, 
       users input a new increase or decrease."""
    
    #Link to a User
    owner = models.ForeignKey(User, blank=True, related_name="valuegoal")
    
    #attributes
    title = models.CharField(max_length=75)
    description = models.TextField()
    determinate = models.BooleanField()
    valueType = models.CharField(max_length=20)
    startValue = models.DecimalField(max_digits = 22, decimal_places=10)
    endValue = models.DecimalField(blank=True, null=True, max_digits = 22, decimal_places=10)
    private = models.BooleanField()
    complete_by = models.DateTimeField(blank=True, null=True, editable=True)
    completed = models.BooleanField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_completed = models.DateTimeField(blank=True, null=True, editable=True)
    last_updated = models.DateTimeField(auto_now=True)
    visual = models.CharField(max_length=70)
    
    def __unicode__(self):
        return self.title

class ValueUpdate(models.Model):
    """Update for value goal."""
    
    #Link to a User
    goal = models.ForeignKey(ValueGoal, blank=True, related_name="valueupdate")
    
    #attributes
    value = models.DecimalField(max_digits = 22, decimal_places=10)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.date_created

class ValueJournal(models.Model):
    """Journal entries for Value Goals"""
    
    goal = models.ForeignKey(ValueGoal, blank=True, related_name="valuejournal")
    entry = models.TextField(max_length=500)
    title = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    
    def __unicode__(self):
        return self.entry

class ValueNote(models.Model):
    """Notes for Value Goals"""
    
    goal = models.ForeignKey(ValueGoal, blank=True, related_name="valuenote")
    note = models.TextField(max_length=300)
    date = models.DateField(auto_now_add=True)
    
    def __unicode__(self):
        return self.note

#######################Progress Goal#######################
class ProgressGoal(models.Model):
    """Model for Progress Goals. Keeps track of a value over time. Unlike value goals, users input a new
       value which overrides the old value."""
    
    #Link to a User
    owner = models.ForeignKey(User, blank=True, related_name="progressgoal")
    
    #attributes
    title = models.CharField(max_length=75)
    description = models.TextField()
    determinate = models.BooleanField()
    valueType = models.CharField(max_length=20)
    startValue = models.DecimalField(max_digits = 22, decimal_places=10)
    endValue = models.DecimalField(blank=True, null=True, max_digits = 22, decimal_places=10)
    private = models.BooleanField()
    complete_by = models.DateTimeField(blank=True, null=True, editable=True)
    completed = models.BooleanField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_completed = models.DateTimeField(blank=True, null=True, editable=True)
    last_updated = models.DateTimeField(auto_now=True)
    visual = models.CharField(max_length=70)
    
    def __unicode__(self):
        return self.title

class ProgressUpdate(models.Model):
    """Update for value goal."""
    
    #Link to a User
    goal = models.ForeignKey(ProgressGoal, blank=True, related_name="progressupdate")
    
    #attributes
    value = models.DecimalField(max_digits = 22, decimal_places=10)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.date_created

class ProgressJournal(models.Model):
    """Journal entries for Progress Goals"""
    
    goal = models.ForeignKey(ProgressGoal, blank=True, related_name="progressjournal")
    entry = models.TextField(max_length=500)
    title = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    
    def __unicode__(self):
        return self.entry

class ProgressNote(models.Model):
    """Notes for Progress Goals"""
    
    goal = models.ForeignKey(ProgressGoal, blank=True, related_name="progressnote")
    note = models.TextField(max_length=300)
    date = models.DateField(auto_now_add=True)
    
    def __unicode__(self):
        return self.note

#######################Recurrent Goals#######################

#######################Special Goals#######################
######Fitness Goals######
class Fitness(models.Model):
    """Model for Fitness Goal"""
    
    #Link to a User
    owner = models.ForeignKey(User, blank=True, related_name="fitness")
    
    #attributes
    title = models.CharField(max_length=75)
    private = models.BooleanField()
    last_updated = models.DateField(auto_now=True)
    visual = models.CharField(max_length=70)
    
    def __unicode__(self):
        return self.title

class FitnessJournal(models.Model):
    goal = models.ForeignKey(Fitness, blank=True, related_name="fitnessjournal")
    entry = models.TextField(max_length=500)
    title = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    
    def __unicode__(self):
        return self.entry

class FitnessNote(models.Model):
    goal = models.ForeignKey(Fitness, blank=True, related_name="fitnessnote")
    note = models.TextField(max_length=300)
    date = models.DateField(auto_now_add=True)
    
    def __unicode__(self):
        return self.note

#Cardio Endurance
class CardioEndurance(models.Model):
    """Model for Cardio Endurance exercises"""
    
    #Link to a User
    goal = models.ForeignKey(Fitness, blank=True, related_name="cardioendurance")
    #attributes
    exercise = models.CharField(max_length=75)
    description = models.TextField()
    durationType = models.CharField(max_length=20)
    distanceType = models.CharField(max_length=20)
    speedType = models.CharField(max_length=20)
    private = models.BooleanField()
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    visual = models.CharField(max_length=70)
    
    def __unicode__(self):
        return self.title

class CardioEnduranceNote(models.Model):
    goal = models.ForeignKey(Fitness, blank=True, related_name="cardioendurancenote")
    note = models.TextField(max_length=300)
    date = models.DateField(auto_now_add=True)
    
    def __unicode__(self):
        return self.note

class CardioEnduranceUpdate(models.Model):
    #Link to a Goal
    goal = models.ForeignKey(CardioEndurance, blank=True, related_name="cardioenduranceupdate")
    #attributes
    duration = models.DecimalField(max_digits = 22, decimal_places=10)
    distance = models.DecimalField(max_digits = 22, decimal_places=10)
    speed = models.DecimalField(max_digits = 22, decimal_places=10)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.date_created
    
class StrengthEndurance(models.Model):
    """Model for Strength Endurance exercises"""
    
    #Link to a User
    goal = models.ForeignKey(Fitness, blank=True, related_name="strengthendurance")
    #attributes
    exercise = models.CharField(max_length=75)
    description = models.TextField()
    resType = models.CharField(max_length=20)
    durType = models.CharField(max_length=20)
    private = models.BooleanField()
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    visual = models.CharField(max_length=70)
    
    def __unicode__(self):
        return self.title

class StrengthEnduranceNote(models.Model):
    goal = models.ForeignKey(Fitness, blank=True, related_name="strengthendurancenote")
    note = models.TextField(max_length=300)
    date = models.DateField(auto_now_add=True)
    
    def __unicode__(self):
        return self.note

class StrengthEnduranceUpdate(models.Model):
    #Link to a Goal
    goal = models.ForeignKey(StrengthEndurance, blank=True, related_name="strengthenduranceupdate")
    #attributes
    duration = models.DecimalField(max_digits = 22, decimal_places=10)
    resistance = models.DecimalField(max_digits = 22, decimal_places=10)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

class Strength(models.Model):
    """Model for Strength exercises"""
    
    #Link to a User
    goal = models.ForeignKey(Fitness, blank=True, related_name="strength")
    
    exercise = models.CharField(max_length=75)
    description = models.TextField()
    resType = models.CharField(max_length=20)
    private = models.BooleanField()
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    visual = models.CharField(max_length=70)
    
    def __unicode__(self):
        return self.title

class StrengthNote(models.Model):
    goal = models.ForeignKey(Fitness, blank=True, related_name="strengthnote")
    note = models.TextField(max_length=300)
    date = models.DateField(auto_now_add=True)
    
    def __unicode__(self):
        return self.note

class StrengthUpdate(models.Model):
    #Link to a Goal
    goal = models.ForeignKey(Strength, blank=True, related_name="strengthupdate")
    #attributes
    sets = models.DecimalField(max_digits = 22, decimal_places=10)
    reps = models.DecimalField(max_digits = 22, decimal_places=10)
    res = models.DecimalField(max_digits = 22, decimal_places=10)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    
class Speed(models.Model):
    """Model for Speed exercises"""
    
    #Link to a User
    goal = models.ForeignKey(Fitness, blank=True, related_name="speed")
    #Attributes
    exercise = models.CharField(max_length=75)
    description = models.TextField()
    distanceType = models.CharField(max_length=20)
    timeType = models.CharField(max_length=20)
    constantDist = models.BooleanField()
    baseDist = models.BooleanField()
    private = models.BooleanField()
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    visual = models.CharField(max_length=70)
    
    def __unicode__(self):
        return self.title

class SpeedNote(models.Model):
    goal = models.ForeignKey(Fitness, blank=True, related_name="speednote")
    note = models.TextField(max_length=300)
    date = models.DateField(auto_now_add=True)
    
    def __unicode__(self):
        return self.note

class SpeedUpdate(models.Model):
    #Link to a Goal
    goal = models.ForeignKey(Speed, blank=True, related_name="speedupdate")
    #attributes
    dist = models.DecimalField(max_digits = 22, decimal_places=10)
    time = models.DecimalField(max_digits = 22, decimal_places=10)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

#Destroy these later
class FitnessValue(models.Model):
    #Link to a Goal
    goal = models.ForeignKey(Fitness, blank=True, related_name="fitnessvalue")
    
    #attributes
    title = models.CharField(max_length=75)
    description = models.TextField()
    determinate = models.BooleanField()
    valueType = models.CharField(max_length=20)
    startValue = models.DecimalField(max_digits = 22, decimal_places=10)
    endValue = models.DecimalField(blank=True, null=True, max_digits = 22, decimal_places=10)
    private = models.BooleanField()
    complete_by = models.DateTimeField(blank=True, null=True, editable=True)
    completed = models.BooleanField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_completed = models.DateTimeField(blank=True, null=True, editable=True)
    last_updated = models.DateTimeField(auto_now=True)
    visual = models.CharField(max_length=70)
    
    def __unicode__(self):
        return self.title

class FitnessVUpdate(models.Model):
    #Link to a Goal
    goal = models.ForeignKey(FitnessValue, blank=True, related_name="fitnessvupdate")
    
    #attributes
    value = models.DecimalField(max_digits = 22, decimal_places=10)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.date_created

class FitnessProgress(models.Model):
    #Link to a Goal
    goal = models.ForeignKey(Fitness, blank=True, related_name="fitnessprogress")
    
    #attributes
    title = models.CharField(max_length=75)
    description = models.TextField()
    determinate = models.BooleanField()
    valueType = models.CharField(max_length=20)
    startValue = models.DecimalField(max_digits = 22, decimal_places=10)
    endValue = models.DecimalField(blank=True, null=True, max_digits = 22, decimal_places=10)
    private = models.BooleanField()
    complete_by = models.DateTimeField(blank=True, null=True, editable=True)
    completed = models.BooleanField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_completed = models.DateTimeField(blank=True, null=True, editable=True)
    last_updated = models.DateTimeField(auto_now=True)
    visual = models.CharField(max_length=70)
    
    def __unicode__(self):
        return self.title

class FitnessPUpdate(models.Model):
    #Link to a Goal
    goal = models.ForeignKey(FitnessProgress, blank=True, related_name="fitnesspupdate")
    
    #attributes
    value = models.DecimalField(max_digits = 22, decimal_places=10)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.date_created