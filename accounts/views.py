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

from django.contrib.auth.models import User
from models import OneShotGoal, OneShotJournal, OneShotNote, MilestoneGoal, Milestone
from forms import OneShotGoalForm, OneShotJournalForm, OneShotNoteForm, DeleteOneShotForm, DeleteOneShotJournalForm, EditOneShotJournalForm
from forms import MilestoneGoalForm, DeleteMilestoneGoalForm, MilestoneGoalJournalForm, MilestoneGoalNoteForm, MilestoneForm, MilestoneFormSet, SubMilestoneFormSet, DeleteMilestoneForm, DeleteSubMilestoneForm, CollectMilestoneIDForm, CompletedButtonForm

import json

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
	
	editoneshotjournalform = EditOneShotJournalForm()
	
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
				return HttpResponseRedirect('/user/%s/'%request.user.username)
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
					return HttpResponseRedirect('/user/%s/'%request.user.username)
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
	editoneshotjournalform = EditOneShotJournalForm()
	
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
				return HttpResponseRedirect('/user/%s/osgoals/%s%d/'%(request.user.username, title, goal.id))
		elif 'osnoteSub' in request.POST:
			oneshotjournalform = OneShotJournalForm()
			oneshotnoteform = OneShotNoteForm(request.POST)
			editoneshotform = OneShotGoalForm(instance=goal)
			deleteoneshotform = DeleteOneShotForm()
			if oneshotnoteform.is_valid():
				osNote = oneshotnoteform.save(commit=False)
				osNote.goal = goal
				oneshotnoteform.save()
				return HttpResponseRedirect('/user/%s/osgoals/%s%d/'%(request.user.username, title, goal.id))
		elif 'editSub' in request.POST:
			oneshotjournalform = OneShotJournalForm()
			oneshotnoteform = OneShotNoteForm()
			editoneshotform = OneShotGoalForm(request.POST, instance=goal)
			deleteoneshotform = DeleteOneShotForm()
			if editoneshotform.is_valid():
				editoneshotform.save()
				return HttpResponseRedirect('/user/%s/osgoals/%s%d/'%(request.user.username, title, goal.id))
		elif 'editosjournalSub' in request.POST:
			editoneshotjournalform = EditOneShotJournalForm(request.POST)
			oneshotjournalform = OneShotJournalForm()
			oneshotnoteform = OneShotNoteForm()
			editoneshotform = OneShotGoalForm()
			deleteoneshotform = DeleteOneShotForm()
			if editoneshotjournalform.is_valid():
				edit_id = editoneshotjournalform.cleaned_data['edit_journal_id']
				edit_entry = editoneshotjournalform.cleaned_data['edit_entry']
				journal = goal.oneshotgoaljournal.get(id=edit_id)
				journalform = OneShotJournalForm({'entry': edit_entry}, instance=journal)
				if journalform.is_valid():
					journalform.save()
					return HttpResponseRedirect('/user/%s/osgoals/%s%d/'%(request.user.username, title, goal.id))
				else:
					return HttpResponseRedirect('not valid')
		elif 'deleteSub' in request.POST:
			oneshotjournalform = OneShotJournalForm()
			oneshotnoteform = OneShotNoteForm()
			editoneshotform = OneShotGoalForm(instance=goal)
			deleteoneshotform = DeleteOneShotForm(request.POST)
			
			toDelete = get_object_or_404(OneShotGoal, id=id)
			if deleteoneshotform.is_valid():
				toDelete.delete()
				return HttpResponseRedirect('/user/%s/'%request.user.username)
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
	return render(request, 'oneshotgoals.html', {'user' : user, 'title' : title, 'goal' : goal, 'oneshotjournalform' : oneshotjournalform, 'oneshotnoteform' : oneshotnoteform, 'editoneshotform' : editoneshotform, 'oneshotjournal' : oneshotjournal, 'oneshotnote' : oneshotnote, 'deleteoneshotform' : deleteoneshotform, 'editoneshotjournalform': editoneshotjournalform})

@login_required
def msgoals(request, username, title, id):
	"""
	Displays a single Milestone Goal
	"""
	
	user = request.user
	
	#goal variables
	goal = request.user.milestonegoal.get(id=id)
	tempMS = goal.milestone.all()
	milestonegoaljournal = goal.milestonegoaljournal.all()
	milestonegoalnote = goal.milestonegoalnote.all()
	
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
	
	#sort milestones
	milestones = []
	for ms in tempMS:
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
		
		obj = {"milestone_title": ms.title, "milestone_description": ms.description, "milestone_private": ms.private, "milestone_completed": ms.completed, "milestone_date_completed": ms.date_completed, "milestone_id": ms.id, "milestone_parent_id": id, "milestone_is_sub": isSub, "submilestones": []}
		for sms in ms.submilestone.all():
			obj["submilestones"].append(find_SubMilestones(sms))
		return obj
	
	test_milestones = []
	
	for ms in milestones:
		test_milestones.append(find_SubMilestones(ms))
	
	test_milestones1 = json.dumps(test_milestones)

	gl = {"goal_title": goal.title, "goal_description": goal.description, "goal_private": goal.private, "goal_completed": goal.completed, "goal_date_completed": goal.date_completed, "goal_id": goal.id}
	goal1 = json.dumps(gl)
	
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
				editmilestone_isSub = collectmilestoneidform.cleaned_data['editmilestone_isSub']
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
				deletemilestone_isSub = collectmilestoneidform.cleaned_data['deletemilestone_isSub']
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
				milestone_isSub = collectmilestoneidform.cleaned_data['milestone_isSub']
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
		else:
			oneshotgoalform = OneShotGoalForm()
			milestonegoalform = MilestoneGoalForm()
			milestoneformset = MilestoneFormSet(prefix='milestone', queryset=Milestone.objects.none())
			submilestoneformset = SubMilestoneFormSet(request.POST, request.FILES, prefix='submilestone', queryset=Milestone.objects.none())
	return render(request, 'milestonegoals.html', {'goal1': mark_safe(goal1), 'test_milestones1': mark_safe(test_milestones1), 
				'test_milestones': test_milestones, 'user' : user, 'title' : title, 'goal' : goal, 'milestonegoalnote': milestonegoalnote, 
				'milestonegoaljournal': milestonegoaljournal, 'milestones' : milestones, 'deletemilestonegoalform': deletemilestonegoalform, 
				'editmilestonegoalform': editmilestonegoalform, 'milestonegoaljournalform': milestonegoaljournalform, 
				'milestonegoalnoteform': milestonegoalnoteform, 'milestoneformset': milestoneformset, 
				'submilestoneformset': submilestoneformset, 'collectmilestoneidform': collectmilestoneidform,
				'deletemilestoneform': deletemilestoneform, 'editmilestoneform': editmilestoneform,
				'completedbuttonform': completedbuttonform})

def test_view(request):
	return render(request, 'testview.html')