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

from django.contrib.auth.models import User
from models import OneShotGoal, OneShotJournal, OneShotNote, MilestoneGoal, Milestone
from forms import OneShotGoalForm, OneShotJournalForm, OneShotNoteForm, DeleteOneShotForm, DeleteOneShotJournalForm 
from forms import MilestoneGoalForm, MilestoneForm, MilestoneFormSet, DeleteMilestoneGoalForm, MilestoneGoalJournalForm, MilestoneGoalNoteForm


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
	milestonegoals = request.user.milestonegoal.all()
	
	#handle forms
	if request.method == 'POST':
		#handle one shot goal
		if 'osgoalSub' in request.POST:
			oneshotgoalform = OneShotGoalForm(request.POST)
			milestonegoalform = MilestoneGoalForm()
			milestoneformset = MilestoneFormSet(prefix='milestone', queryset=Milestone.objects.none())
			if oneshotgoalform.is_valid():
				osGoal = oneshotgoalform.save(commit=False)
				osGoal.owner = user
				osGoal.save()
				return HttpResponseRedirect('/%s/'%request.user.username)
		elif 'msgoalSub' in request.POST:
			oneshotgoalform = OneShotGoalForm()
			milestonegoalform = MilestoneGoalForm(request.POST)
			if milestonegoalform.is_valid():
				msGoal = milestonegoalform.save(commit=False)
				msGoal.owner = user
				msGoalObject = milestonegoalform.save()
				milestoneformset = MilestoneFormSet(request.POST, request.FILES, prefix='milestone', queryset=Milestone.objects.none(), instance=msGoalObject)
				if milestoneformset.is_valid():
					milestoneformset.save()
					return HttpResponseRedirect('/%s/'%request.user.username)
				else:
					return HttpResponseRedirect('SNAFU')
		else:
			oneshotgoalform = OneShotGoalForm()
			milestonegoalform = MilestoneGoalForm()
			milestoneformset = MilestoneFormSet(prefix='milestone', queryset=Milestone.objects.none())
	else:
		oneshotgoalform = OneShotGoalForm()
		milestonegoalform = MilestoneGoalForm()
		milestoneformset = MilestoneFormSet()
	return render(request, 'profile.html', {'user' : user, 'oneshotgoalcount': oneshotgoalcount, 'oneshotgoals': oneshotgoals, 'oneshotgoalform': oneshotgoalform, 'milestonegoals': milestonegoals, 'milestonegoalform': milestonegoalform, 'milestoneformset': milestoneformset })

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

@login_required
def msgoals(request, username, title, id):
	"""
	Displays a single Milestone Goal
	"""
	user = request.user
	
	#goal variables
	goal = request.user.milestonegoal.get(id=id)
	milestone = goal.milestone.all()
	milestonegoaljournal = goal.milestonegoaljournal.all()
	milestonegoalnote = goal.milestonegoalnote.all()
	
	#Form variables
	milestonegoaljournalform = MilestoneGoalJournalForm(request.POST)
	milestonegoalnoteform = MilestoneGoalNoteForm()
	editmilestonegoalform = MilestoneGoalForm(instance=goal)
	deletemilestonegoalform = DeleteMilestoneGoalForm()
	
	#handle forms
	if request.method == 'POST':
		if 'msgJournalSub' in request.POST:
			milestonegoaljournalform = MilestoneGoalJournalForm(request.POST)
			if milestonegoaljournalform.is_valid():
				msgJournal = milestonegoaljournalform.save(commit=False)
				msgJournal.goal = goal
				milestonegoaljournalform.save()
				return HttpResponseRedirect('/%s/msgoals/%s%d/'%(request.user.username, goal.title, goal.id))
		elif 'msgNoteSub' in request.POST:
			milestonegoalnoteform = MilestoneGoalNoteForm(request.POST)
			if milestonegoalnoteform.is_valid():
				msgNote = milestonegoalnoteform.save(commit=False)
				msgNote.goal = goal
				msgNote.save()
				return HttpResponseRedirect('/%s/msgoals/%s%d/'%(request.user.username, goal.title, goal.id))
		elif 'editMSGSub' in request.POST:
			editmilestonegoalform = MilestoneGoalForm(request.POST, instance=goal)
			if editmilestonegoalform.is_valid():
				editmilestonegoalform.save()
				return HttpResponseRedirect('/%s/msgoals/%s%d/'%(request.user.username, goal.title, goal.id))
		elif 'deleteMSGoalSub' in request.POST:
			deletemilestonegoalform = DeleteMilestoneGoalForm(request.POST)
			goalToDelete = get_object_or_404(MilestoneGoal, id=id)
			if deletemilestonegoalform.is_valid():
				goalToDelete.delete()
				return HttpResponseRedirect('/%s/'%request.user.username)
	return render(request, 'milestonegoals.html', {'user' : user, 'title' : title, 'goal' : goal, 'milestonegoalnote': milestonegoalnote, 'milestonegoaljournal': milestonegoaljournal, 'milestone' : milestone, 'deletemilestonegoalform': deletemilestonegoalform, 'editmilestonegoalform': editmilestonegoalform, 'milestonegoaljournalform': milestonegoaljournalform, 'milestonegoalnoteform': milestonegoalnoteform})

def test_view(request):
	return render(request, 'testview.html')