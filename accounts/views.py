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
from models import OneShotGoal, OneShotJournal, OneShotNote
from forms import OneShotGoalForm, OneShotJournalForm, OneShotNoteForm

@login_required
def myprofile(request, username):
	"""
	Page that displays User Profile and Goals
	"""
	user = request.user
	
	#NEED TO ADD MORE PROFILE SHIT
	
	#goal variables
	oneshotgoalcount = request.user.oneshotgoal.count()
	oneshotgoals = request.user.oneshotgoal.all()
	
	#handle forms
	if request.method == 'POST':
		#handle one shot goal
		if 'osgoalSub' in request.POST:
			oneshotgoalform = OneShotGoalForm(request.POST)
			if oneshotgoalform.is_valid():
				osGoal = oneshotgoalform.save(commit=False)
				osGoal.owner = user
				oneshotgoalform.save()
				return HttpResponseRedirect('/%s/'%request.user.username)
		else:
			oneshotgoalform = OneShotGoalForm()
	else:
		oneshotgoalform = OneShotGoalForm()
	return render(request, 'profile.html', {'user' : user, 'oneshotgoalcount': oneshotgoalcount, 'oneshotgoals': oneshotgoals, 'oneshotgoalform': oneshotgoalform })

@login_required
def osgoals(request, username, title):
	"""
	Displays a single One Shot Goal
	"""
	user = request.user
	
	#goal variables
	goal = request.user.oneshotgoal.get(title=title)
	oneshotjournal = goal.oneshotgoaljournal.all()
	oneshotnote = goal.oneshotgoalnote.all()
	
	#handle forms
	if request.method == 'POST':
		#handle one shot goal
		if 'osjournalSub' in request.POST:
			oneshotjournalform = OneShotJournalForm(request.POST)
			oneshotnoteform = OneShotNoteForm()
			oneshotgoalform = OneShotGoalForm()
			if oneshotjournalform.is_valid():
				osJournal = oneshotjournalform.save(commit=False)
				osJournal.goal = goal
				oneshotjournalform.save()
				return HttpResponseRedirect('/%s/osgoals/%s/'%(request.user.username, goal.title))
		elif 'osnoteSub' in request.POST:
			oneshotjournalform = OneShotJournalForm()
			oneshotnoteform = OneShotNoteForm(request.POST)
			oneshotgoalform = OneShotGoalForm()
			if oneshotnoteform.is_valid():
				osNote = oneshotnoteform.save(commit=False)
				osNote.goal = goal
				oneshotnoteform.save()
				return HttpResponseRedirect('/%s/osgoals/%s/'%(request.user.username, goal.title))
		else:
			oneshotjournalform = OneShotJournalForm()
			oneshotnoteform = OneShotNoteForm()
			oneshotgoalform = OneShotGoalForm()
	else:
		oneshotjournalform = OneShotJournalForm()
		oneshotnoteform = OneShotNoteForm()
		oneshotgoalform = OneShotGoalForm()
	return render(request, 'oneshotgoals.html', {'user' : user, 'title' : title, 'goal' : goal, 'oneshotjournalform' : oneshotjournalform, 'oneshotnoteform' : oneshotnoteform, 'oneshotgoalform' : oneshotgoalform, 'oneshotjournal' : oneshotjournal, 'oneshotnote' : oneshotnote })

	
def test_view(request):
	return render(request, 'testview.html')