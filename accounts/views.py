import datetime, random, hashlib
from django.contrib import auth
from django.core.context_processors import csrf
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response, get_object_or_404
from django.template import Template, Context
from django.template.loader import get_template
from django.contrib.sessions.models import Session
from django.contrib.auth import login, logout
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.forms.formsets import formset_factory

from django.contrib.auth.models import User
from models import OneShotGoal, OneShotJournal, OneShotNote
from forms import OneShotGoalForm, OneShotJournalForm, OneShotNoteForm, DeleteOneShotForm, DeleteOneShotJournalForm, MilestoneGoalForm, MilestoneForm, SubMilestoneForm

@login_required
def myprofile(request, username):
	"""
	Page that displays User Profile and Goals
	"""
	user = request.user
	
	#NEED TO ADD MORE PROFILE STUFF
	
	#goal variables
	oneshotgoalcount = request.user.oneshotgoal.count()
	oneshotgoals = request.user.oneshotgoal.all()
	
	#milestone goal formsets
	MilestoneFormSet = formset_factory(MilestoneForm, extra=1)
	SubMilestoneFormSet = formset_factory(SubMilestoneForm, extra=1)
	
	#handle forms
	if request.method == 'POST':
		#handle one shot goal
		if 'osgoalSub' in request.POST:
			oneshotgoalform = OneShotGoalForm(request.POST)
			milestonegoalform = MilestoneGoalForm()
			milestoneformset = MilestoneFormSet()
			if oneshotgoalform.is_valid():
				osGoal = oneshotgoalform.save(commit=False)
				osGoal.owner = user
				oneshotgoalform.save()
				return HttpResponseRedirect('/%s/'%request.user.username)
		if 'msgoalSub' in request.POST:
			oneshotgoalform = OneShotGoalForm()
			milestonegoalform = MilestoneGoalForm(request.POST)
			milestoneformset = MilestoneFormSet(request.POST, request.FILES)
		else:
			oneshotgoalform = OneShotGoalForm()
			milestonegoalform = MilestoneGoalForm()
			milestoneformset = MilestoneFormSet()
	else:
		oneshotgoalform = OneShotGoalForm()
		milestonegoalform = MilestoneGoalForm()
		milestoneformset = MilestoneFormSet()
	return render(request, 'profile.html', {'user' : user, 'oneshotgoalcount': oneshotgoalcount, 'oneshotgoals': oneshotgoals, 'oneshotgoalform': oneshotgoalform, 'milestonegoalform': milestonegoalform, 'milestoneformset': milestoneformset })

@login_required
def osgoals(request, username, title, id):
	"""
	Displays a single One Shot Goal
	"""
	user = request.user
	
	#goal variables
	goal = request.user.oneshotgoal.get(id=id)
	oneshotjournal = goal.oneshotgoaljournal.all()
	oneshotnote = goal.oneshotgoalnote.all()
	
	#handle forms
	if request.method == 'POST':
		#handle one shot goal
		if 'osjournalSub' in request.POST:
			oneshotjournalform = OneShotJournalForm(request.POST)
			oneshotnoteform = OneShotNoteForm()
			editoneshotform = OneShotGoalForm(instance=goal)
			deleteoneshotform = DeleteOneShotForm()
			if oneshotjournalform.is_valid():
				osJournal = oneshotjournalform.save(commit=False)
				osJournal.goal = goal
				oneshotjournalform.save()
				return HttpResponseRedirect('/%s/osgoals/%s%d/'%(request.user.username, goal.title, goal.id))
		elif 'osnoteSub' in request.POST:
			oneshotjournalform = OneShotJournalForm()
			oneshotnoteform = OneShotNoteForm(request.POST)
			editoneshotform = OneShotGoalForm(instance=goal)
			deleteoneshotform = DeleteOneShotForm()
			if oneshotnoteform.is_valid():
				osNote = oneshotnoteform.save(commit=False)
				osNote.goal = goal
				oneshotnoteform.save()
				return HttpResponseRedirect('/%s/osgoals/%s%d/'%(request.user.username, goal.title, goal.id))
		elif 'editSub' in request.POST:
			oneshotjournalform = OneShotJournalForm()
			oneshotnoteform = OneShotNoteForm()
			editoneshotform = OneShotGoalForm(request.POST, instance=goal)
			deleteoneshotform = DeleteOneShotForm()
			if editoneshotform.is_valid():
				editoneshotform.save()
				return HttpResponseRedirect('/%s/osgoals/%s%d/'%(request.user.username, goal.title, goal.id))
		elif 'editjournalSub' in request.POST:
			oneshotjournalform = OneShotJournalForm(request.POST, instance=goal)
			oneshotnoteform = OneShotNoteForm()
			editoneshotform = OneShotGoalForm()
			deleteoneshotform = DeleteOneShotForm()
			if editoneshotform.is_valid():
				editoneshotform.save()
				return HttpResponseRedirect('/%s/osgoals/%s%d/'%(request.user.username, goal.title, goal.id))
		elif 'deleteSub' in request.POST:
			oneshotjournalform = OneShotJournalForm()
			oneshotnoteform = OneShotNoteForm()
			editoneshotform = OneShotGoalForm(instance=goal)
			deleteoneshotform = DeleteOneShotForm(request.POST)
			
			toDelete = get_object_or_404(OneShotGoal, id=id)
			if deleteoneshotform.is_valid():
				toDelete.delete()
				return HttpResponseRedirect('/%s/'%request.user.username)
		else:
			oneshotjournalform = OneShotJournalForm()
			oneshotnoteform = OneShotNoteForm()
			editoneshotform = OneShotGoalForm(instance=goal)
			deleteoneshotform = DeleteOneShotForm()
	else:
		oneshotjournalform = OneShotJournalForm()
		oneshotnoteform = OneShotNoteForm()
		editoneshotform = OneShotGoalForm(instance=goal)
		deleteoneshotform = DeleteOneShotForm()
	return render(request, 'oneshotgoals.html', {'user' : user, 'title' : title, 'goal' : goal, 'oneshotjournalform' : oneshotjournalform, 'oneshotnoteform' : oneshotnoteform, 'editoneshotform' : editoneshotform, 'oneshotjournal' : oneshotjournal, 'oneshotnote' : oneshotnote, 'deleteoneshotform' : deleteoneshotform})
	
def test_view(request):
	return render(request, 'testview.html')