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
from django.utils.safestring import mark_safe
from django.utils.timezone import utc

from django.contrib.auth.models import User
from models import OneShotGoal, OneShotJournal, OneShotNote, MilestoneGoal, Milestone
from forms import OneShotGoalForm, OneShotJournalForm, OneShotNoteForm, DeleteOneShotForm, DeleteOneShotJournalForm, EditOneShotJournalForm
from forms import MilestoneGoalForm, DeleteMilestoneGoalForm, MilestoneGoalJournalForm, MilestoneGoalNoteForm, MilestoneForm, MilestoneFormSet, SubMilestoneFormSet, DeleteMilestoneForm, DeleteSubMilestoneForm, CollectMilestoneIDForm, CompletedButtonForm
from forms import TimeOneShotGoalForm, DeleteTimeOneShotForm
import json

@login_required
def goals(request, username):
	"""
	Page that displays User Profile and Goals
	"""
	user = request.user
	
	#NEED TO ADD MORE PROFILE STUFF
	
	#goal variables
	oneshotgoalcount = request.user.oneshotgoal.count()
	oneshotgoals = request.user.oneshotgoal.all()
	milestonegoals = request.user.milestonegoal.all()
	timeoneshotgoals = request.user.timeoneshotgoal.all()
	
	oneshotgoalform = OneShotGoalForm()
	milestonegoalform = MilestoneGoalForm()
	milestoneformset = MilestoneFormSet(prefix='milestone', queryset=Milestone.objects.none())
	
	timeoneshotgoalform = TimeOneShotGoalForm()
	
	#handle forms
	if request.method == 'POST':
		if 'osgoalSub' in request.POST:
			oneshotgoalform = OneShotGoalForm(request.POST)
			if oneshotgoalform.is_valid():
				osGoal = oneshotgoalform.save(commit=False)
				osGoal.owner = user
				osGoal.save()
				return HttpResponseRedirect('/user/%s/'%request.user.username)
		elif 'msgoalSub' in request.POST:
			milestonegoalform = MilestoneGoalForm(request.POST)
			if milestonegoalform.is_valid():
				msGoal = milestonegoalform.save(commit=False)
				msGoal.owner = user
				msGoalObject = milestonegoalform.save()
				milestoneformset = MilestoneFormSet(request.POST, request.FILES, prefix='milestone', queryset=Milestone.objects.none(), instance=msGoalObject)
				if milestoneformset.is_valid():
					milestoneformset.save()
					return HttpResponseRedirect('/user/%s/'%request.user.username)
				else:
					return HttpResponseRedirect('SNAFU')
		elif 'tosgoalSub' in request.POST:
			timeoneshotgoalform = TimeOneShotGoalForm(request.POST)
			if timeoneshotgoalform.is_valid():
				tGoal = timeoneshotgoalform.save(commit=False)
				tGoal.owner = user
				tGoal.save()
				return HttpResponseRedirect('/user/%s/'%request.user.username)
	return render(request, 'goals.html', {'user' : user, 'oneshotgoalcount': oneshotgoalcount, 'oneshotgoals': oneshotgoals, 
				'oneshotgoalform': oneshotgoalform, 'milestonegoals': milestonegoals, 'milestonegoalform': milestonegoalform, 
				'milestoneformset': milestoneformset, 'timeoneshotgoalform': timeoneshotgoalform, 
				'timeoneshotgoals': timeoneshotgoals })

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
	
	#Form variables
	editoneshotform = OneShotGoalForm(instance=goal)
	deleteoneshotform = DeleteOneShotForm()
	completedbuttonform = CompletedButtonForm()
	oneshotjournalform = OneShotJournalForm()
	oneshotnoteform = OneShotNoteForm()
	
	#converts datetime object for forms
	def getDateTime(date):
		if date is None:
			return date
		else:
			return str(date)
	
	gl = {"goal_title": goal.title, "goal_description": goal.description, "goal_private": goal.private, "goal_completed": goal.completed, "goal_date_completed": getDateTime(goal.date_completed), "goal_last_updated": getDateTime(goal.last_updated), "goal_id": goal.id}
	goalJSON = json.dumps(gl)
	
	#handle forms
	if request.method == 'POST':
		#handle one shot goal
		if 'osjournalSub' in request.POST:
			oneshotjournalform = OneShotJournalForm(request.POST)
			if oneshotjournalform.is_valid():
				osJournal = oneshotjournalform.save(commit=False)
				osJournal.goal = goal
				oneshotjournalform.save()
				return HttpResponseRedirect('/user/%s/osgoals/%s%d/'%(request.user.username, title, goal.id))
		elif 'osnoteSub' in request.POST:
			oneshotnoteform = OneShotNoteForm(request.POST)
			if oneshotnoteform.is_valid():
				osNote = oneshotnoteform.save(commit=False)
				osNote.goal = goal
				oneshotnoteform.save()
				return HttpResponseRedirect('/user/%s/osgoals/%s%d/'%(request.user.username, title, goal.id))
		elif 'editSub' in request.POST:
			editoneshotform = OneShotGoalForm(request.POST, instance=goal)
			if editoneshotform.is_valid():
				editoneshotform.save()
				return HttpResponseRedirect('/user/%s/osgoals/%s%d/'%(request.user.username, title, goal.id))
		elif 'deleteSub' in request.POST:
			deleteoneshotform = DeleteOneShotForm(request.POST)
			toDelete = get_object_or_404(OneShotGoal, id=id)
			if deleteoneshotform.is_valid():
				toDelete.delete()
				return HttpResponseRedirect('/user/%s/'%request.user.username)
		elif 'completedOSGSub' in request.POST:
			completedbuttonform = CompletedButtonForm(request.POST)
			if completedbuttonform.is_valid():
				date = completedbuttonform.cleaned_data['date_completed']
				oneshotgoalform = OneShotGoalForm({'title':goal.title}, instance=goal)
				if oneshotgoalform.is_valid():
					oneshotgoalform = oneshotgoalform.save(commit=False)
					oneshotgoalform.completed = True
					oneshotgoalform.date_completed = date
					oneshotgoalform.save()
					return HttpResponseRedirect('/user/%s/osgoals/%s%d/'%(request.user.username, title, goal.id))
	return render(request, 'oneshotgoals.html', {'user' : user, 'title' : title, 'goalJSON': mark_safe(goalJSON), 'goal' : goal, 'oneshotjournalform' : oneshotjournalform, 
				'oneshotnoteform' : oneshotnoteform, 'editoneshotform' : editoneshotform, 'oneshotjournal' : oneshotjournal, 
				'oneshotnote' : oneshotnote, 'deleteoneshotform' : deleteoneshotform, 'completedbuttonform':completedbuttonform})

@login_required
def msgoals(request, username, title, id):
	"""
	Displays a single Milestone Goal
	"""
	
	user = request.user
	
	#goal variables
	goal = request.user.milestonegoal.get(id=id)
	allMS = goal.milestone.all()
	milestonegoaljournal = goal.milestonegoaljournal.all()
	milestonegoalnote = goal.milestonegoalnote.all()
	goaltitle = goal.title
	
	#Form variables
	milestonegoaljournalform = MilestoneGoalJournalForm(request.POST)
	milestonegoalnoteform = MilestoneGoalNoteForm()
	editmilestonegoalform = MilestoneGoalForm(instance=goal)
	deletemilestonegoalform = DeleteMilestoneGoalForm()
	milestoneform = MilestoneForm()
	editmilestoneform = MilestoneForm()
	milestoneformset = MilestoneFormSet(prefix='milestone', queryset=Milestone.objects.none())
	submilestoneform = MilestoneForm()
	submilestoneformset = SubMilestoneFormSet(prefix='submilestone', queryset=Milestone.objects.none())
	collectmilestoneidform = CollectMilestoneIDForm()
	deletemilestoneform = DeleteMilestoneForm()
	completedbuttonform = CompletedButtonForm()
	
	#complete a milestone
	def completeMS(ms, date):
		milestoneform = MilestoneForm({'title':ms.title}, instance=ms)
		if milestoneform.is_valid():
			msform = milestoneform.save(commit=False)
			msform.completed = True
			msform.date_completed = date
			msform.save()
		
	#complete milestone and all sub-milestones
	def completeMilestones(ms, date):
		if (not ms.completed):
			completeMS(ms, date)
			subs = ms.submilestone.all()
			for sms in subs:
				completeMilestones(sms, date)
	
	#converts datetime object for forms
	def getDateTime(date):
		if date is None:
			return date
		else:
			return str(date)
	
	#sort milestones
	milestones = []
	for ms in allMS:
		if ms.milestone is None:
			milestones.append(ms)
	
	#find submilestones
	def find_SubMilestones(ms):
		"""
		Recurse to build serializable object
		"""
		if ms.milestone is None:
			isSub = False
			id = ms.goal.id
		else:
			isSub = True
			id = ms.milestone.id
		
		obj = {"milestone_title": ms.title, "milestone_description": ms.description, "milestone_private": ms.private, "milestone_completed": ms.completed, "milestone_date_completed": getDateTime(ms.date_completed), "milestone_id": ms.id, "milestone_parent_id": id, "milestone_is_sub": isSub, "milestone_last_updated": getDateTime(ms.last_updated), "submilestones": []}
		for sms in ms.submilestone.all():
			obj["submilestones"].append(find_SubMilestones(sms))
		return obj
	
	test_milestones = []
	
	for ms in milestones:
		test_milestones.append(find_SubMilestones(ms))
	
	test_milestones1 = json.dumps(test_milestones)

	gl = {"goal_title": goal.title, "goal_description": goal.description, "goal_private": goal.private, "goal_completed": goal.completed, "goal_date_completed": getDateTime(goal.date_completed), "goal_last_updated": getDateTime(goal.last_updated), "goal_id": goal.id}
	goalJSON = json.dumps(gl)
	
	#handle forms
	if request.method == 'POST':
		if 'msgJournalSub' in request.POST:
			milestonegoaljournalform = MilestoneGoalJournalForm(request.POST)
			if milestonegoaljournalform.is_valid():
				msgJournal = milestonegoaljournalform.save(commit=False)
				msgJournal.goal = goal
				milestonegoaljournalform.save()
				return HttpResponseRedirect('/user/%s/msgoals/%s%d/'%(request.user.username, title, goal.id))
		elif 'msgNoteSub' in request.POST:
			milestonegoalnoteform = MilestoneGoalNoteForm(request.POST)
			if milestonegoalnoteform.is_valid():
				msgNote = milestonegoalnoteform.save(commit=False)
				msgNote.goal = goal
				msgNote.save()
				return HttpResponseRedirect('/user/%s/msgoals/%s%d/'%(request.user.username, title, goal.id))
		elif 'editMSGSub' in request.POST:
			editmilestonegoalform = MilestoneGoalForm(request.POST, instance=goal)
			if editmilestonegoalform.is_valid():
				editmilestonegoalform.save()
				return HttpResponseRedirect('/user/%s/msgoals/%s%d/'%(request.user.username, title, goal.id))
		elif 'editMSSub' in request.POST:
			collectmilestoneidform = CollectMilestoneIDForm(request.POST)
			if collectmilestoneidform.is_valid():
				editmilestone_id = collectmilestoneidform.cleaned_data['editmilestone_id']
				clean_ms = goal.milestone.get(id=editmilestone_id)
				editmilestoneform = MilestoneForm(request.POST, instance=clean_ms)
				if editmilestoneform.is_valid():
					editmilestoneform.save()
					return HttpResponseRedirect('/user/%s/msgoals/%s%d/'%(request.user.username, title, goal.id))
		elif 'deleteMSGoalSub' in request.POST:
			deletemilestonegoalform = DeleteMilestoneGoalForm(request.POST)
			goalToDelete = get_object_or_404(MilestoneGoal, id=id)
			if deletemilestonegoalform.is_valid():
				goalToDelete.delete()
				return HttpResponseRedirect('/user/%s/'%request.user.username)
		elif 'deleteMSSub' in request.POST:
			collectmilestoneidform = CollectMilestoneIDForm(request.POST)
			if collectmilestoneidform.is_valid():
				deletemilestone_id = collectmilestoneidform.cleaned_data['deletemilestone_id']
				deletemilestoneform = DeleteMilestoneForm(request.POST)
				if deletemilestoneform.is_valid():
					msToDelete = goal.milestone.get(id=deletemilestone_id)
					msToDelete.delete()
					return HttpResponseRedirect('/user/%s/msgoals/%s%d/'%(request.user.username, title, goal.id))
		elif 'msSub' in request.POST:
			milestoneformset = MilestoneFormSet(request.POST, request.FILES, prefix='milestone', queryset=Milestone.objects.none(), instance=goal)
			if milestoneformset.is_valid():
				milestoneformset.save()
				return HttpResponseRedirect('/user/%s/msgoals/%s%d/'%(request.user.username, title, goal.id))
		elif 'subMSSub' in request.POST:
			collectmilestoneidform = CollectMilestoneIDForm(request.POST)
			if collectmilestoneidform.is_valid():
				milestone_id = collectmilestoneidform.cleaned_data['milestone_id']
				clean_ms = goal.milestone.get(id=milestone_id)
				submilestoneformset = SubMilestoneFormSet(request.POST, request.FILES, prefix='submilestone', queryset=Milestone.objects.none(), instance=clean_ms)
				if submilestoneformset.is_valid():
					for form in submilestoneformset:
						if form.is_valid():
							msform = form.save(commit=False)
							msform.goal = goal
							msform.save()
					submilestoneformset.save()
					return HttpResponseRedirect('/user/%s/msgoals/%s%d/'%(request.user.username, title, goal.id))
		elif 'completedMSSub' in request.POST:
			collectmilestoneidform = CollectMilestoneIDForm(request.POST)
			if collectmilestoneidform.is_valid():
				milestone_id = collectmilestoneidform.cleaned_data['completedmilestone_id']
				milestone_isGoal = collectmilestoneidform.cleaned_data['completedmilestone_isGoal']
				completedbuttonform = CompletedButtonForm(request.POST)
				if completedbuttonform.is_valid():
					date = completedbuttonform.cleaned_data['date_completed']
					if milestone_isGoal:
						for ms in allMS:
							completeMS(ms, date)
						milestonegoalform = MilestoneGoalForm({'title':goal.title}, instance=goal)
						if milestonegoalform.is_valid():
							msgform = milestonegoalform.save(commit=False)
							msgform.completed = True
							msgform.date_completed = date
							msgform.save()
							return HttpResponseRedirect('/user/%s/msgoals/%s%d/'%(request.user.username, title, goal.id))
						else:
							return HttpResponseRedirect()
					else:
						clean_ms = goal.milestone.get(id=milestone_id)
						completeMilestones(clean_ms, date)
						return HttpResponseRedirect('/user/%s/msgoals/%s%d/'%(request.user.username, title, goal.id))
		else:
			oneshotgoalform = OneShotGoalForm()
			milestonegoalform = MilestoneGoalForm()
			milestoneformset = MilestoneFormSet(prefix='milestone', queryset=Milestone.objects.none())
			submilestoneformset = SubMilestoneFormSet(prefix='submilestone', queryset=Milestone.objects.none())
	return render(request, 'milestonegoals.html', {'goalJSON': mark_safe(goalJSON), 'test_milestones1': mark_safe(test_milestones1), 
				'test_milestones': test_milestones, 'user' : user, 'title' : title, 'goal' : goal, 'milestonegoalnote': milestonegoalnote, 
				'milestonegoaljournal': milestonegoaljournal, 'milestones' : milestones, 'deletemilestonegoalform': deletemilestonegoalform, 
				'editmilestonegoalform': editmilestonegoalform, 'milestonegoaljournalform': milestonegoaljournalform, 
				'milestonegoalnoteform': milestonegoalnoteform, 'milestoneformset': milestoneformset, 
				'submilestoneformset': submilestoneformset, 'collectmilestoneidform': collectmilestoneidform,
				'deletemilestoneform': deletemilestoneform, 'editmilestoneform': editmilestoneform,
				'completedbuttonform': completedbuttonform})

@login_required
def tosgoals(request, username, title, id):
	"""
	Displays a single Time One Shot Goal
	"""
	user = request.user
	
	#goal variables
	goal = request.user.timeoneshotgoal.get(id=id)
	
	#Form variables
	edittimeoneshotform = TimeOneShotGoalForm(instance=goal)
	deletetimeoneshotform = DeleteTimeOneShotForm()
	completedbuttonform = CompletedButtonForm()
	
	#converts datetime object for forms
	def getDateTime(date):
		if date is None:
			return date
		else:
			return str(date)
	
	gl = {"goal_title": goal.title, "goal_description": goal.description, "goal_private": goal.private, "goal_completed": goal.completed, "goal_complete_by": getDateTime(goal.complete_by), "goal_date_completed": getDateTime(goal.date_completed), "goal_last_updated": getDateTime(goal.last_updated), "goal_date_created": getDateTime(goal.date_created), "goal_id": goal.id}
	goalJSON = json.dumps(gl)
	
	#handle forms
	if request.method == 'POST':
		#handle one shot goal
		if 'editSub' in request.POST:
			edittimeoneshotform = TimeOneShotGoalForm(request.POST, instance=goal)
			if edittimeoneshotform.is_valid():
				edittimeoneshotform.save()
				return HttpResponseRedirect('/user/%s/tosgoals/%s%d/'%(request.user.username, title, goal.id))
		elif 'deleteSub' in request.POST:
			toDelete = get_object_or_404(TimeOneShotGoal, id=id)
			deletetimeoneshotform = DeleteTimeOneShotForm(request.POST, instance=toDelete)
			if deleteoneshotform.is_valid():
				toDelete.delete()
				return HttpResponseRedirect('/user/%s/'%request.user.username)
		elif 'completedTOSGSub' in request.POST:
			completedbuttonform = CompletedButtonForm(request.POST)
			if completedbuttonform.is_valid():
				date = completedbuttonform.cleaned_data['date_completed']
				timeoneshotgoalform = TimeOneShotGoalForm({'title':goal.title, 'complete_by': goal.complete_by}, instance=goal)
				if timeoneshotgoalform.is_valid():
					tosgform = timeoneshotgoalform.save(commit=False)
					tosgform.completed = True
					tosgform.date_completed = date
					tosgform.save()
					return HttpResponseRedirect('/user/%s/tosgoals/%s%d/'%(request.user.username, title, goal.id))
				else:
					return HttpResponseRedirect('fuck')
	return render(request, 'timeoneshotgoals.html', {'user' : user, 'title' : title, 'goalJSON': mark_safe(goalJSON), 'goal' : goal, 
				'edittimeoneshotform' : edittimeoneshotform, 'deletetimeoneshotform' : deletetimeoneshotform, 'completedbuttonform':completedbuttonform})				

def test_view(request):
	return render(request, 'testview.html')