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
from models import OneShotGoal, OneShotJournal, OneShotNote, MilestoneGoal, Milestone, TimeOneShotGoal, TimeMilestoneGoal, TimeMilestone, ValueGoal, ValueUpdate
from forms import CollectMilestoneIDForm, CompletedButtonForm, CollectNoteJournalID, MilestoneCollectNoteJournalID
from forms import OneShotGoalForm, DeleteOneShotForm
from forms import OneShotNoteForm, DeleteOneShotNoteForm, OneShotJournalForm, DeleteOneShotJournalForm
from forms import MilestoneGoalForm, DeleteMilestoneGoalForm, MilestoneForm, MilestoneFormSet, SubMilestoneFormSet, DeleteMilestoneForm
from forms import MilestoneGoalNoteForm, DeleteMilestoneGoalNoteForm, MilestoneGoalJournalForm, DeleteMilestoneGoalJournalForm, MilestoneNoteForm, DeleteMilestoneNoteForm, MilestoneJournalForm, DeleteMilestoneJournalForm
from forms import TimeOneShotGoalForm, DeleteTimeOneShotForm
from forms import TimeOneShotNoteForm, DeleteTimeOneShotNoteForm, TimeOneShotJournalForm, DeleteTimeOneShotJournalForm
from forms import TimeMilestoneGoalForm, TimeMilestoneForm, TimeMilestoneFormSet, TimeSubMilestoneFormSet, DeleteTimeMilestoneGoalForm, DeleteTimeMilestoneForm
from forms import TimeMilestoneGoalNoteForm, DeleteTimeMilestoneGoalNoteForm, TimeMilestoneGoalJournalForm, DeleteTimeMilestoneGoalJournalForm, TimeMilestoneNoteForm, DeleteTimeMilestoneNoteForm, TimeMilestoneJournalForm, DeleteTimeMilestoneJournalForm
from forms import ValueGoalForm, ValueUpdateForm, DeleteValueGoalForm, CollectUpdateIDForm
from forms import ValueJournalForm, DeleteValueJournalForm, ValueNoteForm, DeleteValueNoteForm
from forms import ProgressGoalForm, ProgressUpdateForm, ProgressGoalForm, DeleteProgressGoalForm
from forms import ProgressJournalForm, DeleteProgressJournalForm, ProgressNoteForm, DeleteProgressNoteForm
import json

#view pages
@login_required
def profile(request, username):
	"""
	Page that displays profile
	"""
	user = request.user
	
	
	
	return render(request, 'profile.html', {'user' : user})


@login_required
def goals(request, username):
	"""
	Page that displays user goals
	"""
	user = request.user
	
	#goal variables
	oneshotgoalcount = request.user.oneshotgoal.count()
	oneshotgoals = request.user.oneshotgoal.all()
	milestonegoals = request.user.milestonegoal.all()
	timeoneshotgoals = request.user.timeoneshotgoal.all()
	timemilestonegoals = request.user.timemilestonegoal.all()
	valuegoals = request.user.valuegoal.all()
	progressgoals = request.user.progressgoal.all()
	
	oneshotgoalform = OneShotGoalForm()
	milestonegoalform = MilestoneGoalForm()
	milestoneformset = MilestoneFormSet(prefix='milestone', queryset=Milestone.objects.none())
	
	timeoneshotgoalform = TimeOneShotGoalForm()
	timemilestonegoalform = TimeMilestoneGoalForm()
	timemilestoneformset = TimeMilestoneFormSet(prefix='timemilestone', queryset=TimeMilestone.objects.none())
	
	valuegoalform = ValueGoalForm()
	
	progressgoalform = ProgressGoalForm()
	
	#handle forms
	if request.method == 'POST':
		if 'osgoalSub' in request.POST:
			oneshotgoalform = OneShotGoalForm(request.POST)
			if oneshotgoalform.is_valid():
				osGoal = oneshotgoalform.save(commit=False)
				osGoal.owner = user
				osGoal.visual = 'Circle'
				osGoal.save()
				return HttpResponseRedirect('/user/%s/'%request.user.username)
		elif 'msgoalSub' in request.POST:
			milestonegoalform = MilestoneGoalForm(request.POST)
			if milestonegoalform.is_valid():
				msGoal = milestonegoalform.save(commit=False)
				msGoal.owner = user
				msGoal.visual = 'DonutChart'
				msGoalObject = milestonegoalform.save()
				milestoneformset = MilestoneFormSet(request.POST, request.FILES, prefix='milestone', queryset=Milestone.objects.none(), instance=msGoalObject)
				if milestoneformset.is_valid():
					milestoneformset.save()
					return HttpResponseRedirect('/user/%s/'%request.user.username)
		elif 'tosgoalSub' in request.POST:
			timeoneshotgoalform = TimeOneShotGoalForm(request.POST)
			if timeoneshotgoalform.is_valid():
				tGoal = timeoneshotgoalform.save(commit=False)
				tGoal.owner = user
				tGoal.visual = 'Circle'
				tGoal.save()
				return HttpResponseRedirect('/user/%s/'%request.user.username)
		elif 'tmsgoalSub' in request.POST:
			timemilestonegoalform = TimeMilestoneGoalForm(request.POST)
			if timemilestonegoalform.is_valid():
				tmsGoal = timemilestonegoalform.save(commit=False)
				tmsGoal.owner = user
				tmsGoal.visual = 'DonutChart'
				tmsGoalObject = timemilestonegoalform.save()
				timemilestoneformset = TimeMilestoneFormSet(request.POST, request.FILES, prefix='timemilestone', queryset=TimeMilestone.objects.none(), instance=tmsGoalObject)
				if timemilestoneformset.is_valid():
					timemilestoneformset.save()
					return HttpResponseRedirect('/user/%s/'%request.user.username)
		elif 'vgoalSub' in request.POST:
			valuegoalform = ValueGoalForm(request.POST)
			if valuegoalform.is_valid():
				vGoal = valuegoalform.save(commit=False)
				vGoal.owner = user
				vGoal.visual = 'LineGraph'
				vGoal.save()
				return HttpResponseRedirect('/user/%s/'%request.user.username)
		elif 'pgoalSub' in request.POST:
			progressgoalform = ProgressGoalForm(request.POST)
			if progressgoalform.is_valid():
				pGoal = progressgoalform.save(commit=False)
				pGoal.owner = user
				pGoal.visual = 'LineGraph'
				pGoal.save()
				return HttpResponseRedirect('/user/%s/'%request.user.username)
	return render(request, 'goals/goals.html', {'user' : user, 'oneshotgoalcount': oneshotgoalcount, 'oneshotgoals': oneshotgoals, 
				'oneshotgoalform': oneshotgoalform, 'milestonegoals': milestonegoals, 'milestonegoalform': milestonegoalform, 
				'milestoneformset': milestoneformset, 'timeoneshotgoalform': timeoneshotgoalform, 'timeoneshotgoals': timeoneshotgoals, 
				'timemilestonegoalform': timemilestonegoalform, 'timemilestoneformset': timemilestoneformset, 'timemilestonegoals': timemilestonegoals,
				'valuegoals': valuegoals, 'valuegoalform': valuegoalform, 'progressgoalform': progressgoalform, 'progressgoals': progressgoals})

@login_required
def osgoals(request, username, title, id):
	"""
	Displays a single One Shot Goal
	"""
	user = request.user
	
	#goal variables
	goal = request.user.oneshotgoal.get(id=id)
	oneshotnotes = goal.oneshotgoalnote.all()
	oneshotjournal = goal.oneshotgoaljournal.all().order_by("date")
	
	#visual and link
	visual = goal.visual
	link = ('/user/%s/osgoals/%s%d/'%(request.user.username, title, goal.id))
	
	#Form variables
	editoneshotform = OneShotGoalForm(instance=goal)
	deleteoneshotform = DeleteOneShotForm()
	uncompleteoneshotform = DeleteOneShotForm()
	completedbuttonform = CompletedButtonForm()
	
	#display forms
	oneshotnoteform = OneShotNoteForm()
	editoneshotnoteform = OneShotNoteForm()
	collectnotejournalid = CollectNoteJournalID()
	deleteoneshotnoteform = DeleteOneShotNoteForm()
	oneshotjournalform = OneShotJournalForm()
	editoneshotjournalform = OneShotJournalForm()
	deleteoneshotjournalform = DeleteOneShotJournalForm()
	
	#converts datetime object for forms
	def getDateTime(date):
		if date is None:
			return date
		else:
			return str(date)
	
	#get goal in JSON
	gl = {"goal_title": goal.title, "goal_description": goal.description, "goal_private": goal.private, "goal_completed": goal.completed, 
		"goal_date_created": getDateTime(goal.date_created), "goal_date_completed": getDateTime(goal.date_completed), 
		"goal_last_updated": getDateTime(goal.last_updated), "goal_id": goal.id}
	goalJSON = json.dumps(gl)
	
	#get notes in JSON
	def notesProcess(nt):
		nt = {'note_id': nt.id, 'note_note': nt.note}
		return nt
	notes = []
	for note in oneshotnotes:
		notes.append(notesProcess(note))
	noteJSON = json.dumps(notes)
	
	#get journal in JSON
	def journalProcess(jnl):
		jnl = {'journal_entry': jnl.entry, 'journal_title': jnl.title, 'journal_date': getDateTime(jnl.date), 'journal_id': jnl.id}
		return jnl
	journals = []
	for journal in oneshotjournal:
		journals.append(journalProcess(journal))
	journalJSON = json.dumps(journals)
	
	#handle forms
	if request.method == 'POST':
		#handle one shot goal
		if 'osjournalSub' in request.POST:
			oneshotjournalform = OneShotJournalForm(request.POST)
			if oneshotjournalform.is_valid():
				osJournal = oneshotjournalform.save(commit=False)
				osJournal.goal = goal
				oneshotjournalform.save()
				return HttpResponseRedirect(link)
		elif 'osnoteSub' in request.POST:
			oneshotnoteform = OneShotNoteForm(request.POST)
			if oneshotnoteform.is_valid():
				osNote = oneshotnoteform.save(commit=False)
				osNote.goal = goal
				oneshotnoteform.save()
				return HttpResponseRedirect(link)
		elif 'editSub' in request.POST:
			editoneshotform = OneShotGoalForm(request.POST, instance=goal)
			if editoneshotform.is_valid():
				editoneshotform.save()
				return HttpResponseRedirect(link)
		elif 'deleteSub' in request.POST:
			toDelete = get_object_or_404(OneShotGoal, id=id)
			deleteoneshotform = DeleteOneShotForm(request.POST, instance=toDelete)
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
					return HttpResponseRedirect(link)
		elif 'uncompleteOSGSub' in request.POST:
			uncompleteoneshotform = DeleteOneShotForm(request.POST, instance=goal)
			if uncompleteoneshotform.is_valid():
				goal.completed = False
				goal.date_completed = None
				goal.save()
				return HttpResponseRedirect(link)
		#Display subs
		elif 'noteSub' in request.POST:
			oneshotnoteform = OneShotNoteForm(request.POST)
			if oneshotnoteform.is_valid():
				osnote = oneshotnoteform.save(commit=False)
				osnote.goal = goal
				osnote.save()
				return HttpResponseRedirect(link)
		elif 'enoteSub' in request.POST:
			collectnotejournalid = CollectNoteJournalID(request.POST)
			if collectnotejournalid.is_valid():
				note_id = collectnotejournalid.cleaned_data['note_id']
				noteObj = goal.oneshotgoalnote.get(id=note_id)
				editoneshotnoteform = OneShotNoteForm(request.POST, instance=noteObj)
				if editoneshotnoteform.is_valid():
					editoneshotnoteform.save()
					return HttpResponseRedirect(link)
		elif 'dnoteSub' in request.POST:
			collectnotejournalid = CollectNoteJournalID(request.POST)
			if collectnotejournalid.is_valid():
				note_id = collectnotejournalid.cleaned_data['note_id']
				noteToDelete = goal.oneshotgoalnote.get(id=note_id)
				deleteoneshotnoteform = DeleteOneShotNoteForm(request.POST, instance=noteToDelete)
				if deleteoneshotnoteform.is_valid():
					noteToDelete.delete()
					return HttpResponseRedirect(link)
		elif 'journalSub' in request.POST:
			oneshotjournalform = OneShotJournalForm(request.POST)
			if oneshotjournalform.is_valid():
				osjrnl = oneshotjournalform.save(commit=False)
				osjrnl.goal = goal
				osjrnl.save()
				return HttpResponseRedirect(link)
		elif 'ejournalSub' in request.POST:
			collectnotejournalid = CollectNoteJournalID(request.POST)
			if collectnotejournalid.is_valid():
				journal_id = collectnotejournalid.cleaned_data['journal_id']
				journalObj = goal.oneshotgoaljournal.get(id=journal_id)
				editoneshotjournalform = OneShotJournalForm(request.POST, instance=journalObj)
				if editoneshotjournalform.is_valid():
					editoneshotjournalform.save()
					return HttpResponseRedirect(link)
		elif 'djournalSub' in request.POST:
			collectnotejournalid = CollectNoteJournalID(request.POST)
			if collectnotejournalid.is_valid():
				journal_id = collectnotejournalid.cleaned_data['journal_id']
				journalToDelete = goal.oneshotgoaljournal.get(id=journal_id)
				deleteoneshotjournalform = DeleteOneShotJournalForm(request.POST, instance=journalToDelete)
				if deleteoneshotjournalform.is_valid():
					journalToDelete.delete()
					return HttpResponseRedirect(link)
	return render(request, 'goals/oneshotgoals.html', {'user' : user, 'title' : title, 'goalJSON': mark_safe(goalJSON), 'goal' : goal, 'oneshotjournalform' : oneshotjournalform, 
				'oneshotnoteform' : oneshotnoteform, 'editoneshotform' : editoneshotform, 'oneshotjournal' : oneshotjournal, 
				'noteJSON' : mark_safe(noteJSON), 'deleteoneshotform' : deleteoneshotform, 'completedbuttonform':completedbuttonform,
				'visual': visual, 'uncompleteoneshotform': uncompleteoneshotform, 'link': str(link), 'editoneshotnoteform': editoneshotnoteform,
				'collectnotejournalid': collectnotejournalid, 'deleteoneshotnoteform': deleteoneshotnoteform, 'deleteoneshotjournalform': deleteoneshotjournalform,
				'editoneshotjournalform': editoneshotjournalform, 'journalJSON': mark_safe(journalJSON)})
				
@login_required
def msgoals(request, username, title, id):
	"""
	Displays a single Milestone Goal
	"""
	user = request.user
	
	#goal variables
	goal = request.user.milestonegoal.get(id=id)
	allMS = goal.milestone.all()
	allJournals=[]
	
	#visual
	visual = goal.visual
	link = ('/user/%s/msgoals/%s%d/'%(request.user.username, title, goal.id))
	
	#Form variables
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
	
	#notes and journals
	milestonegoalnoteform = MilestoneGoalNoteForm()
	editmilestonegoalnoteform = MilestoneGoalNoteForm()
	deletemilestonegoalnoteform = DeleteMilestoneGoalNoteForm()
	milestonegoaljournalform = MilestoneGoalJournalForm()
	editmilestonegoaljournalform = MilestoneGoalJournalForm()
	deletemilestonegoaljournalform = DeleteMilestoneJournalForm()
	milestonenoteform = MilestoneNoteForm()
	editmilestonenoteform = MilestoneNoteForm()
	deletemilestonenoteform = DeleteMilestoneNoteForm()
	milestonejournalform = MilestoneJournalForm()
	editmilestonejournalform = MilestoneJournalForm()
	deletemilestonejournalform = DeleteMilestoneJournalForm()	
	milestonecollectnotejournalid = MilestoneCollectNoteJournalID()

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
	
	#uncomplete milestones
	def uncompleteParents(ms):
		"""
		Complete all parents in the milestone, including the goal
		"""
		if ms.milestone is None:
			ms.completed = False
			ms.save()
			goal.completed = False
			goal.save()
		else:
			ms.completed = False
			ms.save()
			uncompleteParents(ms.milestone)
	
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
	
	#get journal entries in JSON
	def journalProcess(jnl, isGoal, msID):
		jnl = {'journal_entry': jnl.entry, 'journal_title': jnl.title, 'journal_date': getDateTime(jnl.date), 'journal_id': jnl.id, 
			'journal_isGoal': isGoal, 'journal_msID': msID}
		return jnl
	
	#get notes in JSON
	def notesProcess(nt):
		nt = {'note_id': nt.id, 'note_note': nt.note}
		return nt
	
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
		
		obj = {"milestone_title": ms.title, "milestone_description": ms.description, "milestone_private": ms.private, "milestone_completed": ms.completed, 
			"milestone_date_completed": getDateTime(ms.date_completed), "milestone_id": ms.id, "milestone_parent_id": id, "milestone_is_sub": isSub, 
			"milestone_last_updated": getDateTime(ms.last_updated), "milestone_date_created": getDateTime(ms.date_created), "submilestones": [], 
			'milestone_journal': [], 'milestone_notes': []}
		for sms in ms.submilestone.all():
			obj["submilestones"].append(find_SubMilestones(sms))
		for nte in ms.milestonenote.all():
			obj["milestone_notes"].append(notesProcess(nte))
		for jnl in ms.milestonejournal.all():
			journal = journalProcess(jnl, False, ms.id)
			obj["milestone_journal"].append(journal)
			allJournals.append(journal)
		return obj

	test_milestones = []
	
	for ms in milestones:
		test_milestones.append(find_SubMilestones(ms))
	test_milestones1 = json.dumps(test_milestones)
	
	gl = {"goal_title": goal.title, "goal_description": goal.description, "goal_private": goal.private, "goal_completed": goal.completed, 
		"goal_date_completed": getDateTime(goal.date_completed), "goal_date_created": getDateTime(goal.date_created), 
		"goal_last_updated": getDateTime(goal.last_updated), "goal_id": goal.id, "goal_notes": [], "goal_journal": []}
	for nte in goal.milestonegoalnote.all():
		gl["goal_notes"].append(notesProcess(nte))
	for jnl in goal.milestonegoaljournal.all():
		journal = journalProcess(jnl, True, -15)
		gl["goal_journal"].append(journal)
		allJournals.append(journal)
	goalJSON = json.dumps(gl)
	
	allJournals.sort(key=lambda item:item['journal_date'], reverse=True)
	alljournalsJSON = json.dumps(allJournals)
	
	#handle forms
	if request.method == 'POST':
		if 'editMSGSub' in request.POST:
			editmilestonegoalform = MilestoneGoalForm(request.POST, instance=goal)
			if editmilestonegoalform.is_valid():
				editmilestonegoalform.save()
				return HttpResponseRedirect(link)
		elif 'editMSSub' in request.POST:
			collectmilestoneidform = CollectMilestoneIDForm(request.POST)
			if collectmilestoneidform.is_valid():
				editmilestone_id = collectmilestoneidform.cleaned_data['editmilestone_id']
				clean_ms = goal.milestone.get(id=editmilestone_id)
				editmilestoneform = MilestoneForm(request.POST, instance=clean_ms)
				if editmilestoneform.is_valid():
					ems = editmilestoneform.save()
					if (ems.completed):
						return HttpResponseRedirect(link)
					else:
						uncompleteParents(ems)
						return HttpResponseRedirect(link)
		elif 'deleteMSGoalSub' in request.POST:
			goalToDelete = get_object_or_404(MilestoneGoal, id=id)
			deletemilestonegoalform = DeleteMilestoneGoalForm(request.POST, instance=goalToDelete)
			if deletemilestonegoalform.is_valid():
				goalToDelete.delete()
				return HttpResponseRedirect('/user/%s/'%request.user.username)
		elif 'deleteMSSub' in request.POST:
			collectmilestoneidform = CollectMilestoneIDForm(request.POST)
			if collectmilestoneidform.is_valid():
				deletemilestone_id = collectmilestoneidform.cleaned_data['deletemilestone_id']
				msToDelete = goal.milestone.get(id=deletemilestone_id)
				deletemilestoneform = DeleteMilestoneForm(request.POST, instance=msToDelete)
				if deletemilestoneform.is_valid():
					msToDelete.delete()
					return HttpResponseRedirect(link)
		elif 'msSub' in request.POST:
			milestoneformset = MilestoneFormSet(request.POST, request.FILES, prefix='milestone', queryset=Milestone.objects.none(), instance=goal)
			if milestoneformset.is_valid():
				newobj = milestoneformset.save()
				incomplete = True
				for form in newobj:
					incomplete = incomplete and (form.completed)
				if incomplete:
					return HttpResponseRedirect(link)
				else:
					goal.completed = False
					goal.save()
					return HttpResponseRedirect(link)
		elif 'subMSSub' in request.POST:
			collectmilestoneidform = CollectMilestoneIDForm(request.POST)
			if collectmilestoneidform.is_valid():
				milestone_id = collectmilestoneidform.cleaned_data['milestone_id']
				clean_ms = goal.milestone.get(id=milestone_id)
				submilestoneformset = SubMilestoneFormSet(request.POST, request.FILES, prefix='submilestone', queryset=Milestone.objects.none(), instance=clean_ms)
				if submilestoneformset.is_valid():
					incomplete = True
					subfm = submilestoneformset.save()
					for form in subfm:
						incomplete = incomplete and (form.completed)
						form.goal = goal
						form.save()
					if incomplete:
						return HttpResponseRedirect(link)
					else:
						uncompleteParents(clean_ms)
						return HttpResponseRedirect(link)
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
							return HttpResponseRedirect(link)
					else:
						clean_ms = goal.milestone.get(id=milestone_id)
						completeMilestones(clean_ms, date)
						return HttpResponseRedirect(link)		
		#goal notes and journal
		elif 'gnoteSub' in request.POST:
			milestonegoalnoteform = MilestoneGoalNoteForm(request.POST)
			if milestonegoalnoteform.is_valid():
				msgnote = milestonegoalnoteform.save(commit=False)
				msgnote.goal = goal
				msgnote.save()
				return HttpResponseRedirect(link)
		elif 'egnoteSub' in request.POST:
			milestonecollectnotejournalid = MilestoneCollectNoteJournalID(request.POST)
			if milestonecollectnotejournalid.is_valid():
				note_id = milestonecollectnotejournalid.cleaned_data['note_id']
				noteObj = goal.milestonegoalnote.get(id=note_id)
				editmilestonegoalnoteform = MilestoneGoalNoteForm(request.POST, instance=noteObj)
				if editmilestonegoalnoteform.is_valid():
					editmilestonegoalnoteform.save()
					return HttpResponseRedirect(link)
		elif 'dgnoteSub' in request.POST:
			milestonecollectnotejournalid = MilestoneCollectNoteJournalID(request.POST)
			if milestonecollectnotejournalid.is_valid():
				note_id = milestonecollectnotejournalid.cleaned_data['note_id']
				noteToDelete = goal.milestonegoalnote.get(id=note_id)
				deletemilestonegoalnoteform = DeleteMilestoneGoalNoteForm(request.POST, instance=noteToDelete)
				if deletemilestonegoalnoteform.is_valid():
					noteToDelete.delete()
					return HttpResponseRedirect(link)
		elif 'gjournalSub' in request.POST:
			milestonegoaljournalform = MilestoneGoalJournalForm(request.POST)
			if milestonegoaljournalform.is_valid():
				msgjrnl = milestonegoaljournalform.save(commit=False)
				msgjrnl.goal = goal
				msgjrnl.save()
				return HttpResponseRedirect(link)
		elif 'egjournalSub' in request.POST:
			milestonecollectnotejournalid = MilestoneCollectNoteJournalID(request.POST)
			if milestonecollectnotejournalid.is_valid():
				journal_id = milestonecollectnotejournalid.cleaned_data['journal_id']
				journalObj = goal.milestonegoaljournal.get(id=journal_id)
				editmilestonegoaljournalform = MilestoneGoalJournalForm(request.POST, instance=journalObj)
				if editmilestonegoaljournalform.is_valid():
					editmilestonegoaljournalform.save()
					return HttpResponseRedirect(link)
		elif 'dgjournalSub' in request.POST:
			milestonecollectnotejournalid = MilestoneCollectNoteJournalID(request.POST)
			if milestonecollectnotejournalid.is_valid():
				journal_id = milestonecollectnotejournalid.cleaned_data['journal_id']
				journalToDelete = goal.milestonegoaljournal.get(id=journal_id)
				deletemilestonegoaljournalform = DeleteMilestoneJournalForm(request.POST, instance=journalToDelete)
				if deletemilestonegoaljournalform.is_valid():
					journalToDelete.delete()
					return HttpResponseRedirect(link)
		#milestone journal and notes
		elif 'noteSub' in request.POST:
			milestonecollectnotejournalid = MilestoneCollectNoteJournalID(request.POST)
			if milestonecollectnotejournalid.is_valid():
				milestone_id = milestonecollectnotejournalid.cleaned_data['milestone_id']
				clean_ms = goal.milestone.get(id=milestone_id)
				milestonenoteform = MilestoneNoteForm(request.POST)
				if milestonenoteform.is_valid():
					msnote = milestonenoteform.save(commit=False)
					msnote.milestone = clean_ms
					msnote.save()
					return HttpResponseRedirect(link)
		elif 'enoteSub' in request.POST:
			milestonecollectnotejournalid = MilestoneCollectNoteJournalID(request.POST)
			if milestonecollectnotejournalid.is_valid():
				milestone_id = milestonecollectnotejournalid.cleaned_data['milestone_id']
				clean_ms = goal.milestone.get(id=milestone_id)
				note_id = milestonecollectnotejournalid.cleaned_data['milestone_note_id']
				noteObj = clean_ms.milestonenote.get(id=note_id)
				editmilestonenoteform = MilestoneNoteForm(request.POST, instance=noteObj)
				if editmilestonenoteform.is_valid():
					editmilestonenoteform.save()
					return HttpResponseRedirect(link)
		elif 'dnoteSub' in request.POST:
			milestonecollectnotejournalid = MilestoneCollectNoteJournalID(request.POST)
			if milestonecollectnotejournalid.is_valid():
				milestone_id = milestonecollectnotejournalid.cleaned_data['milestone_id']
				clean_ms = goal.milestone.get(id=milestone_id)
				note_id = milestonecollectnotejournalid.cleaned_data['milestone_note_id']
				noteToDelete = clean_ms.milestonenote.get(id=note_id)
				deletemilestonenoteform = DeleteMilestoneNoteForm(request.POST, instance=noteToDelete)
				if deletemilestonenoteform.is_valid():
					noteToDelete.delete()
					return HttpResponseRedirect(link)
		elif 'journalSub' in request.POST:
			milestonecollectnotejournalid = MilestoneCollectNoteJournalID(request.POST)
			if milestonecollectnotejournalid.is_valid():
				milestone_id = milestonecollectnotejournalid.cleaned_data['milestone_id']
				clean_ms = goal.milestone.get(id=milestone_id)
				milestonejournalform = MilestoneJournalForm(request.POST)
				if milestonejournalform.is_valid():
					msjrnl = milestonejournalform.save(commit=False)
					msjrnl.milestone = clean_ms
					msjrnl.save()
					return HttpResponseRedirect(link)
		elif 'ejournalSub' in request.POST:
			milestonecollectnotejournalid = MilestoneCollectNoteJournalID(request.POST)
			if milestonecollectnotejournalid.is_valid():
				milestone_id = milestonecollectnotejournalid.cleaned_data['milestone_id']
				clean_ms = goal.milestone.get(id=milestone_id)
				journal_id = milestonecollectnotejournalid.cleaned_data['milestone_journal_id']
				journalObj = clean_ms.milestonejournal.get(id=journal_id)
				editmilestonejournalform = MilestoneJournalForm(request.POST, instance=journalObj)
				if editmilestonejournalform.is_valid():
					editmilestonejournalform.save()
					return HttpResponseRedirect(link)
		elif 'djournalSub' in request.POST:
			milestonecollectnotejournalid = MilestoneCollectNoteJournalID(request.POST)
			if milestonecollectnotejournalid.is_valid():
				milestone_id = milestonecollectnotejournalid.cleaned_data['milestone_id']
				clean_ms = goal.milestone.get(id=milestone_id)
				journal_id = milestonecollectnotejournalid.cleaned_data['milestone_journal_id']
				journalToDelete = clean_ms.milestonejournal.get(id=journal_id)
				deletemilestonejournalform = DeleteMilestoneJournalForm(request.POST, instance=journalToDelete)
				if deletemilestonejournalform.is_valid():
					journalToDelete.delete()
					return HttpResponseRedirect(link)
	return render(request, 'goals/milestonegoals.html', {'goalJSON': mark_safe(goalJSON), 'test_milestones1': mark_safe(test_milestones1), 
				'test_milestones': test_milestones, 'user' : user, 'title' : title, 'goal' : goal,
				'milestones' : milestones, 'deletemilestonegoalform': deletemilestonegoalform, 
				'editmilestonegoalform': editmilestonegoalform, 'milestoneformset': milestoneformset, 
				'submilestoneformset': submilestoneformset, 'collectmilestoneidform': collectmilestoneidform,
				'deletemilestoneform': deletemilestoneform, 'editmilestoneform': editmilestoneform,
				'completedbuttonform': completedbuttonform, 'visual': visual, 'alljournalsJSON': mark_safe(alljournalsJSON),
				'milestonegoalnoteform': milestonegoalnoteform, 'editmilestonegoalnoteform': editmilestonegoalnoteform,
				'deletemilestonegoalnoteform': deletemilestonegoalnoteform, 'milestonegoaljournalform': milestonegoaljournalform,
				'editmilestonegoaljournalform': editmilestonegoaljournalform, 'deletemilestonegoaljournalform': deletemilestonegoaljournalform,
				'milestonenoteform': milestonenoteform, 'editmilestonenoteform': editmilestonenoteform, 'deletemilestonenoteform': deletemilestonenoteform,
				'milestonejournalform': milestonejournalform, 'editmilestonejournalform': editmilestonejournalform,
				'deletemilestonejournalform': deletemilestonejournalform, 'milestonecollectnotejournalid': milestonecollectnotejournalid})

@login_required
def tosgoals(request, username, title, id):
	"""
	Displays a single Time One Shot Goal
	"""
	user = request.user
	
	#goal variables
	goal = request.user.timeoneshotgoal.get(id=id)
	timeoneshotnotes = goal.timeoneshotgoalnote.all()
	timeoneshotjournal = goal.timeoneshotgoaljournal.all().order_by("date")
	
	#visual and link
	visual = goal.visual
	link = ('/user/%s/tosgoals/%s%d/'%(request.user.username, title, goal.id))
	
	#Form variables
	edittimeoneshotform = TimeOneShotGoalForm(instance=goal)
	deletetimeoneshotform = DeleteTimeOneShotForm()
	completedbuttonform = CompletedButtonForm()
	
	#display forms
	timeoneshotnoteform = TimeOneShotNoteForm()
	edittimeoneshotnoteform = TimeOneShotNoteForm()
	deletetimeoneshotnoteform = DeleteTimeOneShotNoteForm()
	timeoneshotjournalform = TimeOneShotJournalForm()
	edittimeoneshotjournalform = TimeOneShotJournalForm()
	deletetimeoneshotjournalform = DeleteTimeOneShotJournalForm()
	collectnotejournalid = CollectNoteJournalID()
	
	#converts datetime object for forms
	def getDateTime(date):
		if date is None:
			return date
		else:
			return str(date)
	
	#get goal in JSON
	gl = {"goal_title": goal.title, "goal_description": goal.description, "goal_private": goal.private, "goal_completed": goal.completed, "goal_complete_by": getDateTime(goal.complete_by), "goal_date_created": getDateTime(goal.date_created), "goal_date_completed": getDateTime(goal.date_completed), "goal_last_updated": getDateTime(goal.last_updated), "goal_id": goal.id}
	goalJSON = json.dumps(gl)
	
	#get notes in JSON
	def notesProcess(nt):
		nt = {'note_id': nt.id, 'note_note': nt.note}
		return nt
	notes = []
	for note in timeoneshotnotes:
		notes.append(notesProcess(note))
	noteJSON = json.dumps(notes)
	
	#get journal in JSON
	def journalProcess(jnl):
		jnl = {'journal_entry': jnl.entry, 'journal_title': jnl.title, 'journal_date': getDateTime(jnl.date), 'journal_id': jnl.id}
		return jnl
	journals = []
	for journal in timeoneshotjournal:
		journals.append(journalProcess(journal))
	journalJSON = json.dumps(journals)
	
	#handle forms
	if request.method == 'POST':
		#handle one shot goal
		if 'editSub' in request.POST:
			edittimeoneshotform = TimeOneShotGoalForm(request.POST, instance=goal)
			if edittimeoneshotform.is_valid():
				edittimeoneshotform.save()
				return HttpResponseRedirect(link)
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
					return HttpResponseRedirect(link)
		#Display subs
		elif 'noteSub' in request.POST:
			timeoneshotnoteform = TimeOneShotNoteForm(request.POST)
			if timeoneshotnoteform.is_valid():
				tosnote = timeoneshotnoteform.save(commit=False)
				tosnote.goal = goal
				tosnote.save()
				return HttpResponseRedirect(link)
		elif 'enoteSub' in request.POST:
			collectnotejournalid = CollectNoteJournalID(request.POST)
			if collectnotejournalid.is_valid():
				note_id = collectnotejournalid.cleaned_data['note_id']
				noteObj = goal.timeoneshotgoalnote.get(id=note_id)
				edittimeoneshotnoteform = TimeOneShotNoteForm(request.POST, instance=noteObj)
				if edittimeoneshotnoteform.is_valid():
					edittimeoneshotnoteform.save()
					return HttpResponseRedirect(link)
		elif 'dnoteSub' in request.POST:
			collectnotejournalid = CollectNoteJournalID(request.POST)
			if collectnotejournalid.is_valid():
				note_id = collectnotejournalid.cleaned_data['note_id']
				noteToDelete = goal.timeoneshotgoalnote.get(id=note_id)
				deletetimeoneshotnoteform = DeleteTimeOneShotNoteForm(request.POST, instance=noteToDelete)
				if deletetimeoneshotnoteform.is_valid():
					noteToDelete.delete()
					return HttpResponseRedirect(link)
		elif 'journalSub' in request.POST:
			timeoneshotjournalform = TimeOneShotJournalForm(request.POST)
			if timeoneshotjournalform.is_valid():
				tosjrnl = timeoneshotjournalform.save(commit=False)
				tosjrnl.goal = goal
				tosjrnl.save()
				return HttpResponseRedirect(link)
		elif 'ejournalSub' in request.POST:
			collectnotejournalid = CollectNoteJournalID(request.POST)
			if collectnotejournalid.is_valid():
				journal_id = collectnotejournalid.cleaned_data['journal_id']
				journalObj = goal.timeoneshotgoaljournal.get(id=journal_id)
				edittimeoneshotjournalform = TimeOneShotJournalForm(request.POST, instance=journalObj)
				if edittimeoneshotjournalform.is_valid():
					edittimeoneshotjournalform.save()
					return HttpResponseRedirect(link)
		elif 'djournalSub' in request.POST:
			collectnotejournalid = CollectNoteJournalID(request.POST)
			if collectnotejournalid.is_valid():
				journal_id = collectnotejournalid.cleaned_data['journal_id']
				journalToDelete = goal.timeoneshotgoaljournal.get(id=journal_id)
				deletetimeoneshotjournalform = DeleteTimeOneShotJournalForm(request.POST, instance=journalToDelete)
				if deletetimeoneshotjournalform.is_valid():
					journalToDelete.delete()
					return HttpResponseRedirect(link)
	return render(request, 'goals/timeoneshotgoals.html', {'user' : user, 'title' : title, 'goalJSON': mark_safe(goalJSON), 'goal' : goal, 
				'edittimeoneshotform' : edittimeoneshotform, 'deletetimeoneshotform' : deletetimeoneshotform, 
				'completedbuttonform':completedbuttonform, 'visual': visual, 'noteJSON' : mark_safe(noteJSON), 
				'journalJSON': mark_safe(journalJSON), 'timeoneshotnoteform': timeoneshotnoteform, 
				'edittimeoneshotnoteform': edittimeoneshotnoteform, 'deletetimeoneshotnoteform': deletetimeoneshotnoteform, 
				'timeoneshotjournalform': timeoneshotjournalform, 'edittimeoneshotjournalform': edittimeoneshotjournalform,
				'deletetimeoneshotjournalform': deletetimeoneshotjournalform, 'collectnotejournalid': collectnotejournalid})				

@login_required
def tmsgoals(request, username, title, id):
	"""
	Displays a single Time Milestone Goal
	"""
	user = request.user
	
	#goal variables
	goal = request.user.timemilestonegoal.get(id=id)
	allMS = goal.timemilestone.all()
	allJournals=[]
	
	#visual
	visual = goal.visual
	link = ('/user/%s/tmsgoals/%s%d/'%(request.user.username, title, goal.id))
	
	#Form variables
	editmilestonegoalform = TimeMilestoneGoalForm(instance=goal)
	deletemilestonegoalform = DeleteTimeMilestoneGoalForm()
	milestoneform = TimeMilestoneForm()
	editmilestoneform = TimeMilestoneForm()
	milestoneformset = TimeMilestoneFormSet(prefix='timemilestone', queryset=TimeMilestone.objects.none())
	submilestoneform = TimeMilestoneForm()
	submilestoneformset = TimeSubMilestoneFormSet(prefix='timesubmilestone', queryset=TimeMilestone.objects.none())
	collectmilestoneidform = CollectMilestoneIDForm()
	deletemilestoneform = DeleteTimeMilestoneForm()
	completedbuttonform = CompletedButtonForm()

	#notes and journals
	timemilestonegoalnoteform = TimeMilestoneGoalNoteForm()
	edittimemilestonegoalnoteform = TimeMilestoneGoalNoteForm()
	deletetimemilestonegoalnoteform = DeleteTimeMilestoneGoalNoteForm()
	timemilestonegoaljournalform = TimeMilestoneGoalJournalForm()
	edittimemilestonegoaljournalform = TimeMilestoneGoalJournalForm()
	deletetimemilestonegoaljournalform = DeleteTimeMilestoneJournalForm()
	timemilestonenoteform = TimeMilestoneNoteForm()
	edittimemilestonenoteform = TimeMilestoneNoteForm()
	deletetimemilestonenoteform = DeleteTimeMilestoneNoteForm()
	timemilestonejournalform = TimeMilestoneJournalForm()
	edittimemilestonejournalform = TimeMilestoneJournalForm()
	deletetimemilestonejournalform = DeleteTimeMilestoneJournalForm()	
	milestonecollectnotejournalid = MilestoneCollectNoteJournalID()
	
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
	
	#uncomplete milestones
	def uncompleteParents(ms):
		"""
		Complete all parents in the milestone, including the goal
		"""
		if ms.milestone is None:
			ms.completed = False
			ms.save()
			goal.completed = False
			goal.save()
		else:
			ms.completed = False
			ms.save()
			uncompleteParents(ms.milestone)
	
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
	
	#get journal entries in JSON
	def journalProcess(jnl, isGoal, msID):
		jnl = {'journal_entry': jnl.entry, 'journal_title': jnl.title, 'journal_date': getDateTime(jnl.date), 'journal_id': jnl.id, 
			'journal_isGoal': isGoal, 'journal_msID': msID}
		return jnl
	
	#get notes in JSON
	def notesProcess(nt):
		nt = {'note_id': nt.id, 'note_note': nt.note}
		return nt
	
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
		
		obj = {"milestone_title": ms.title, "milestone_description": ms.description, "milestone_private": ms.private, "milestone_completed": ms.completed, 
			"milestone_date_completed": getDateTime(ms.date_completed), "milestone_complete_by": getDateTime(ms.complete_by), "milestone_id": ms.id, 
			"milestone_parent_id": id, "milestone_is_sub": isSub, "milestone_last_updated": getDateTime(ms.last_updated), 
			"milestone_date_created": getDateTime(ms.date_created), "submilestones": [], 'milestone_journal': [], 'milestone_notes': []}
		for sms in ms.timesubmilestone.all():
			obj["submilestones"].append(find_SubMilestones(sms))
		for nte in ms.timemilestonenote.all():
			obj["milestone_notes"].append(notesProcess(nte))
		for jnl in ms.timemilestonejournal.all():
			journal = journalProcess(jnl, False, ms.id)
			obj["milestone_journal"].append(journal)
			allJournals.append(journal)
		return obj

	test_milestones = []
	
	for ms in milestones:
		test_milestones.append(find_SubMilestones(ms))
	test_milestones1 = json.dumps(test_milestones)
	
	gl = {"goal_title": goal.title, "goal_description": goal.description, "goal_private": goal.private, "goal_completed": goal.completed, 
		"goal_date_completed": getDateTime(goal.date_completed), "goal_complete_by": getDateTime(goal.complete_by),
		"goal_last_updated": getDateTime(goal.last_updated), "goal_date_created": getDateTime(goal.date_created), "goal_id": goal.id, 
		"goal_notes": [], "goal_journal": []}
	for nte in goal.timemilestonegoalnote.all():
		gl["goal_notes"].append(notesProcess(nte))
	for jnl in goal.timemilestonegoaljournal.all():
		journal = journalProcess(jnl, True, -15)
		gl["goal_journal"].append(journal)
		allJournals.append(journal)
	goalJSON = json.dumps(gl)
	
	allJournals.sort(key=lambda item:item['journal_date'], reverse=True)
	alljournalsJSON = json.dumps(allJournals)
	
	#handle forms
	if request.method == 'POST':
		if 'editMSGSub' in request.POST:
			editmilestonegoalform = TimeMilestoneGoalForm(request.POST, instance=goal)
			if editmilestonegoalform.is_valid():
				editmilestonegoalform.save()
				return HttpResponseRedirect(link)
		elif 'editMSSub' in request.POST:
			collectmilestoneidform = CollectMilestoneIDForm(request.POST)
			if collectmilestoneidform.is_valid():
				editmilestone_id = collectmilestoneidform.cleaned_data['editmilestone_id']
				clean_ms = goal.timemilestone.get(id=editmilestone_id)
				editmilestoneform = TimeMilestoneForm(request.POST, instance=clean_ms)
				if editmilestoneform.is_valid():
					ems = editmilestoneform.save()
					if (ems.completed):
						return HttpResponseRedirect(link)
					else:
						uncompleteParents(ems)
						return HttpResponseRedirect(link)
		elif 'deleteMSGoalSub' in request.POST:
			goalToDelete = get_object_or_404(TimeMilestoneGoal, id=id)
			deletemilestonegoalform = DeleteTimeMilestoneGoalForm(request.POST, instance=goalToDelete)
			if deletemilestonegoalform.is_valid():
				goalToDelete.delete()
				return HttpResponseRedirect('/user/%s/'%request.user.username)
		elif 'deleteMSSub' in request.POST:
			collectmilestoneidform = CollectMilestoneIDForm(request.POST)
			if collectmilestoneidform.is_valid():
				deletemilestone_id = collectmilestoneidform.cleaned_data['deletemilestone_id']
				msToDelete = goal.timemilestone.get(id=deletemilestone_id)
				deletemilestoneform = DeleteTimeMilestoneForm(request.POST, instance=msToDelete)
				if deletemilestoneform.is_valid():
					msToDelete.delete()
					return HttpResponseRedirect(link)
		elif 'msSub' in request.POST:
			milestoneformset = TimeMilestoneFormSet(request.POST, request.FILES, prefix='timemilestone', queryset=TimeMilestone.objects.none(), instance=goal)
			if milestoneformset.is_valid():
				newobj = milestoneformset.save()
				incomplete = True
				for form in newobj:
					incomplete = incomplete and (form.completed)
				if incomplete:
					return HttpResponseRedirect(link)
				else:
					goal.completed = False
					goal.save()
					return HttpResponseRedirect(link)
		elif 'subMSSub' in request.POST:
			collectmilestoneidform = CollectMilestoneIDForm(request.POST)
			if collectmilestoneidform.is_valid():
				milestone_id = collectmilestoneidform.cleaned_data['milestone_id']
				clean_ms = goal.timemilestone.get(id=milestone_id)
				submilestoneformset = TimeSubMilestoneFormSet(request.POST, request.FILES, prefix='timesubmilestone', queryset=TimeMilestone.objects.none(), instance=clean_ms)
				if submilestoneformset.is_valid():
					incomplete = True
					subfm = submilestoneformset.save()
					for form in subfm:
						incomplete = incomplete and (form.completed)
						form.goal = goal
						form.save()
					if incomplete:
						return HttpResponseRedirect(link)
					else:
						uncompleteParents(clean_ms)
						return HttpResponseRedirect(link)
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
						milestonegoalform = TimeMilestoneGoalForm({'title':goal.title, 'complete_by':goal.complete_by}, instance=goal)
						if milestonegoalform.is_valid():
							msgform = milestonegoalform.save(commit=False)
							msgform.completed = True
							msgform.date_completed = date
							msgform.save()
							return HttpResponseRedirect(link)
					else:
						clean_ms = goal.timemilestone.get(id=milestone_id)
						completeMilestones(clean_ms, date)
						return HttpResponseRedirect(link)
		#goal notes and journal
		elif 'gnoteSub' in request.POST:
			timemilestonegoalnoteform = TimeMilestoneGoalNoteForm(request.POST)
			if timemilestonegoalnoteform.is_valid():
				tmsgnote = timemilestonegoalnoteform.save(commit=False)
				tmsgnote.goal = goal
				tmsgnote.save()
				return HttpResponseRedirect(link)
		elif 'egnoteSub' in request.POST:
			milestonecollectnotejournalid = MilestoneCollectNoteJournalID(request.POST)
			if milestonecollectnotejournalid.is_valid():
				note_id = milestonecollectnotejournalid.cleaned_data['note_id']
				noteObj = goal.timemilestonegoalnote.get(id=note_id)
				edittimemilestonegoalnoteform = TimeMilestoneGoalNoteForm(request.POST, instance=noteObj)
				if edittimemilestonegoalnoteform.is_valid():
					edittimemilestonegoalnoteform.save()
					return HttpResponseRedirect(link)
		elif 'dgnoteSub' in request.POST:
			milestonecollectnotejournalid = MilestoneCollectNoteJournalID(request.POST)
			if milestonecollectnotejournalid.is_valid():
				note_id = milestonecollectnotejournalid.cleaned_data['note_id']
				noteToDelete = goal.timemilestonegoalnote.get(id=note_id)
				deletetimemilestonegoalnoteform = DeleteTimeMilestoneGoalNoteForm(request.POST, instance=noteToDelete)
				if deletetimemilestonegoalnoteform.is_valid():
					noteToDelete.delete()
					return HttpResponseRedirect(link)
		elif 'gjournalSub' in request.POST:
			timemilestonegoaljournalform = TimeMilestoneGoalJournalForm(request.POST)
			if timemilestonegoaljournalform.is_valid():
				tmsgjrnl = timemilestonegoaljournalform.save(commit=False)
				tmsgjrnl.goal = goal
				tmsgjrnl.save()
				return HttpResponseRedirect(link)
		elif 'egjournalSub' in request.POST:
			milestonecollectnotejournalid = MilestoneCollectNoteJournalID(request.POST)
			if milestonecollectnotejournalid.is_valid():
				journal_id = milestonecollectnotejournalid.cleaned_data['journal_id']
				journalObj = goal.timemilestonegoaljournal.get(id=journal_id)
				edittimemilestonegoaljournalform = TimeMilestoneGoalJournalForm(request.POST, instance=journalObj)
				if edittimemilestonegoaljournalform.is_valid():
					edittimemilestonegoaljournalform.save()
					return HttpResponseRedirect(link)
		elif 'dgjournalSub' in request.POST:
			milestonecollectnotejournalid = MilestoneCollectNoteJournalID(request.POST)
			if milestonecollectnotejournalid.is_valid():
				journal_id = milestonecollectnotejournalid.cleaned_data['journal_id']
				journalToDelete = goal.timemilestonegoaljournal.get(id=journal_id)
				deletetimemilestonegoaljournalform = DeleteTimeMilestoneJournalForm(request.POST, instance=journalToDelete)
				if deletetimemilestonegoaljournalform.is_valid():
					journalToDelete.delete()
					return HttpResponseRedirect(link)
		#milestone journal and notes
		elif 'noteSub' in request.POST:
			milestonecollectnotejournalid = MilestoneCollectNoteJournalID(request.POST)
			if milestonecollectnotejournalid.is_valid():
				milestone_id = milestonecollectnotejournalid.cleaned_data['milestone_id']
				clean_ms = goal.timemilestone.get(id=milestone_id)
				timemilestonenoteform = TimeMilestoneNoteForm(request.POST)
				if timemilestonenoteform.is_valid():
					tmsnote = timemilestonenoteform.save(commit=False)
					tmsnote.milestone = clean_ms
					tmsnote.save()
					return HttpResponseRedirect(link)
		elif 'enoteSub' in request.POST:
			milestonecollectnotejournalid = MilestoneCollectNoteJournalID(request.POST)
			if milestonecollectnotejournalid.is_valid():
				milestone_id = milestonecollectnotejournalid.cleaned_data['milestone_id']
				clean_ms = goal.timemilestone.get(id=milestone_id)
				note_id = milestonecollectnotejournalid.cleaned_data['milestone_note_id']
				noteObj = clean_ms.milestonenote.get(id=note_id)
				edittimemilestonenoteform = TimeMilestoneNoteForm(request.POST, instance=noteObj)
				if edittimemilestonenoteform.is_valid():
					edittimemilestonenoteform.save()
					return HttpResponseRedirect(link)
		elif 'dnoteSub' in request.POST:
			milestonecollectnotejournalid = MilestoneCollectNoteJournalID(request.POST)
			if milestonecollectnotejournalid.is_valid():
				milestone_id = milestonecollectnotejournalid.cleaned_data['milestone_id']
				clean_ms = goal.timemilestone.get(id=milestone_id)
				note_id = milestonecollectnotejournalid.cleaned_data['milestone_note_id']
				noteToDelete = clean_ms.timemilestonenote.get(id=note_id)
				deletetimemilestonenoteform = DeleteTimeMilestoneNoteForm(request.POST, instance=noteToDelete)
				if deletetimemilestonenoteform.is_valid():
					noteToDelete.delete()
					return HttpResponseRedirect(link)
		elif 'journalSub' in request.POST:
			milestonecollectnotejournalid = MilestoneCollectNoteJournalID(request.POST)
			if milestonecollectnotejournalid.is_valid():
				milestone_id = milestonecollectnotejournalid.cleaned_data['milestone_id']
				clean_ms = goal.timemilestone.get(id=milestone_id)
				timemilestonejournalform = TimeMilestoneJournalForm(request.POST)
				if timemilestonejournalform.is_valid():
					msjrnl = timemilestonejournalform.save(commit=False)
					msjrnl.milestone = clean_ms
					msjrnl.save()
					return HttpResponseRedirect(link)
		elif 'ejournalSub' in request.POST:
			milestonecollectnotejournalid = MilestoneCollectNoteJournalID(request.POST)
			if milestonecollectnotejournalid.is_valid():
				milestone_id = milestonecollectnotejournalid.cleaned_data['milestone_id']
				clean_ms = goal.timemilestone.get(id=milestone_id)
				journal_id = milestonecollectnotejournalid.cleaned_data['milestone_journal_id']
				journalObj = clean_ms.timemilestonejournal.get(id=journal_id)
				edittimemilestonejournalform = TimeMilestoneJournalForm(request.POST, instance=journalObj)
				if edittimemilestonejournalform.is_valid():
					edittimemilestonejournalform.save()
					return HttpResponseRedirect(link)
		elif 'djournalSub' in request.POST:
			milestonecollectnotejournalid = MilestoneCollectNoteJournalID(request.POST)
			if milestonecollectnotejournalid.is_valid():
				milestone_id = milestonecollectnotejournalid.cleaned_data['milestone_id']
				clean_ms = goal.timemilestone.get(id=milestone_id)
				journal_id = milestonecollectnotejournalid.cleaned_data['milestone_journal_id']
				journalToDelete = clean_ms.timemilestonejournal.get(id=journal_id)
				deletetimemilestonejournalform = DeleteTimeMilestoneJournalForm(request.POST, instance=journalToDelete)
				if deletetimemilestonejournalform.is_valid():
					journalToDelete.delete()
					return HttpResponseRedirect(link)
	return render(request, 'goals/timemilestonegoals.html', {'goalJSON': mark_safe(goalJSON), 'test_milestones1': mark_safe(test_milestones1), 
				'test_milestones': test_milestones, 'user' : user, 'title' : title, 'goal' : goal, 'milestones' : milestones, 
				'deletemilestonegoalform': deletemilestonegoalform, 'editmilestonegoalform': editmilestonegoalform, 
				'milestoneformset': milestoneformset, 'submilestoneformset': submilestoneformset, 
				'collectmilestoneidform': collectmilestoneidform,'deletemilestoneform': deletemilestoneform, 'editmilestoneform': editmilestoneform,
				'completedbuttonform': completedbuttonform, 'visual': visual, 'alljournalsJSON': mark_safe(alljournalsJSON),
				'timemilestonegoalnoteform': timemilestonegoalnoteform, 'edittimemilestonegoalnoteform': edittimemilestonegoalnoteform,
				'deletetimemilestonegoalnoteform': deletetimemilestonegoalnoteform, 'timemilestonegoaljournalform': timemilestonegoaljournalform,
				'edittimemilestonegoaljournalform': edittimemilestonegoaljournalform, 'deletetimemilestonegoaljournalform': deletetimemilestonegoaljournalform,
				'timemilestonenoteform': timemilestonenoteform, 'edittimemilestonenoteform': edittimemilestonenoteform, 
				'deletetimemilestonenoteform': deletetimemilestonenoteform, 'timemilestonejournalform': timemilestonejournalform, 
				'edittimemilestonejournalform': edittimemilestonejournalform, 'deletetimemilestonejournalform': deletetimemilestonejournalform, 
				'milestonecollectnotejournalid': milestonecollectnotejournalid})

@login_required
def vgoals(request, username, title, id):
	"""
	Displays a value goal
	"""
	user = request.user
	
	#goal variables
	goal = request.user.valuegoal.get(id=id)
	valueupdates = goal.valueupdate.all()
	valuenotes = goal.valuenote.all()
	valuejournal = goal.valuejournal.all().order_by("date")
	
	#visual
	visual = goal.visual
	link = ('/user/%s/vgoals/%s%d/'%(request.user.username, title, goal.id))
	
	#Form variables
	editvaluegoalform = ValueGoalForm(instance=goal)
	cmplvaluegoalform = ValueGoalForm(instance=goal)
	deletevaluegoalform = DeleteValueGoalForm()
	valueupdateform = ValueUpdateForm()
	editupdateform = ValueUpdateForm()
	collectupdateidform = CollectUpdateIDForm()
	
	#display forms
	valuenoteform = ValueNoteForm()
	editvaluenoteform = ValueNoteForm()
	deletevaluenoteform = DeleteValueNoteForm()
	valuejournalform = ValueJournalForm()
	editvaluejournalform = ValueJournalForm()
	deletevaluejournalform = DeleteValueJournalForm()
	collectnotejournalid = CollectNoteJournalID()
	
	#JSON encoder upgrade for decimals
	class DecimalEncoder(json.JSONEncoder):
		def _iterencode(self, o, markers=None):
			if isinstance(o, decimal.Decimal):
				return (str(o) for o in [o])
			return super(DecimalEncoder, self)._iterencode(o, markers)
	
	#converts datetime object for forms
	def getDateTime(date):
		if date is None:
			return date
		else:
			return str(date)

	#remove trailing zeros
	def zeroOut(val):
		newval = val.rstrip("0")
		last = len(newval)-1
		if (newval[last] == "."):
			return newval.rstrip(".")
		else:
			return newval
			
	#calculate totals and process 
	def processUpdate(up, total):
		tempArray = []
		temp = total+up.value
		upda = {"update_value": str(up.value), "update_description": up.description, 
			"update_date_created": getDateTime(up.date_created), "update_id": up.id,
			"update_last_updated": getDateTime(up.last_updated), "update_total": str(temp),
			"update_nozero": (zeroOut(str(temp))), "update_value_nozero": (zeroOut(str(up.value)))}
		tempArray.append(upda)
		tempArray.append(temp)
		return tempArray
	
	updates = []
	total = goal.startValue
	for upd in valueupdates:
		temparray = processUpdate(upd,total)
		updates.append(temparray[0])
		total = temparray[1]
	
	presentValue = total
	
	updates = json.dumps(updates)

	gl = {"goal_title": goal.title, "goal_description": goal.description, "goal_determinate": goal.determinate, 
		"goal_valueType": goal.valueType, "goal_startValue": str(goal.startValue), 
		"goal_endValue": str(goal.endValue), "goal_private": goal.private, "goal_completed": goal.completed, 
		"goal_complete_by": getDateTime(goal.complete_by), "goal_date_completed": getDateTime(goal.date_completed), 
		"goal_last_updated": getDateTime(goal.last_updated), "goal_date_created": getDateTime(goal.date_created), 
		"goal_id": goal.id, "goal_nozero": (zeroOut(str(goal.startValue))), "goal_endNoZero": (zeroOut(str(goal.endValue))),
		"goal_currentNoZero": (zeroOut(str(presentValue)))}
	goalJSON = json.dumps(gl, cls=DecimalEncoder)
	
	#get journal in JSON
	def journalProcess(jnl):
		jnl = {'journal_entry': jnl.entry, 'journal_title': jnl.title, 'journal_date': getDateTime(jnl.date), 'journal_id': jnl.id}
		return jnl
	journals = []
	for journal in valuejournal:
		journals.append(journalProcess(journal))
	journalJSON = json.dumps(journals)
	
	#get notes in JSON
	def notesProcess(nt):
		nt = {'note_id': nt.id, 'note_note': nt.note}
		return nt
	notes = []
	for note in valuenotes:
		notes.append(notesProcess(note))
	noteJSON = json.dumps(notes)
	
	#handle forms
	if request.method == 'POST':
		if 'editSub' in request.POST:
			editvaluegoalform = ValueGoalForm(request.POST, instance=goal)
			if editvaluegoalform.is_valid():
				newgoal = editvaluegoalform.save()
				if (not newgoal.determinate):
					newgoal.endValue = None
					newgoal.complete_by = None
					newgoal.completed = False
					newgoal.date_completed = None
					newgoal.save()
					return HttpResponseRedirect(link)
				else:
					cmpl = False
					current = presentValue
					if (newgoal.endValue > newgoal.startValue):
						if (current >= newgoal.endValue):
							cmpl = True
						else:
							cmpl = False
					else:
						if (current <= newgoal.endValue):
							cmpl = True
						else:
							cmpl = False
					if cmpl:
						newgoal.completed = True
						newgoal.date_completed = newgoal.last_updated
						newgoal.save()
						return HttpResponseRedirect(link)
					else: 
						newgoal.completed = False
						newgoal.date_completed = None
						newgoal.save()
						return HttpResponseRedirect(link)
		elif 'deleteSub' in request.POST:
			toDelete = get_object_or_404(ValueGoal, id=id)
			deletevaluegoalform = DeleteValueGoalForm(request.POST, instance=toDelete)
			if deletevaluegoalform.is_valid():
				toDelete.delete()
				return HttpResponseRedirect('/user/%s/'%request.user.username)
		elif 'updateSub' in request.POST:
			valueupdateform = ValueUpdateForm(request.POST)
			if valueupdateform.is_valid():
				vuform = valueupdateform.save(commit=False)
				vuform.goal = goal
				newval = vuform.value
				updateobj = valueupdateform.save()
				if (goal.determinate):
					cmpl = False
					current = presentValue
					total = newval+current
					if (goal.endValue > goal.startValue):
						if (total >= goal.endValue):
							cmpl = True
						else:
							cmpl = False
					else:
						if (total <= goal.endValue):
							cmpl = True
						else:
							cmpl = False
					if cmpl:
						goal.completed = True
						goal.date_completed = updateobj.date_created
						goal.save()
						return HttpResponseRedirect(link)
					else: 
						goal.completed = False
						goal.date_completed = None
						goal.save()
						return HttpResponseRedirect(link)
				else:
					return HttpResponseRedirect(link)
		elif 'editUpdateSub' in request.POST:
			collectupdateidform = CollectUpdateIDForm(request.POST)
			if collectupdateidform.is_valid():
				editupdate_id = collectupdateidform.cleaned_data['editupdate_id']
				clean_upd = goal.valueupdate.get(id=editupdate_id)
				oldvalue = clean_upd.value
				editupdateform = ValueUpdateForm(request.POST, instance=clean_upd)
				if editupdateform.is_valid():
					updateobj = editupdateform.save()
					newval = updateobj.value - oldvalue
					if (goal.determinate):
						cmpl = False
						current = presentValue
						total = newval+current
						if (goal.endValue > goal.startValue):
							if (total >= goal.endValue):
								cmpl = True
							else:
								cmpl = False
						else:
							if (total <= goal.endValue):
								cmpl = True
							else:
								cmpl = False
						if cmpl:
							goal.completed = True
							goal.date_completed = updateobj.date_created
							goal.save()
							return HttpResponseRedirect(link)
						else:
							goal.completed = False
							goal.date_completed = None
							goal.save()
							return HttpResponseRedirect(link)
					else:
						return HttpResponseRedirect(link)
		#Display subs
		elif 'noteSub' in request.POST:
			valuenoteform = ValueNoteForm(request.POST)
			if valuenoteform.is_valid():
				vnote = valuenoteform.save(commit=False)
				vnote.goal = goal
				vnote.save()
				return HttpResponseRedirect(link)
		elif 'enoteSub' in request.POST:
			collectnotejournalid = CollectNoteJournalID(request.POST)
			if collectnotejournalid.is_valid():
				note_id = collectnotejournalid.cleaned_data['note_id']
				noteObj = goal.valuenote.get(id=note_id)
				editvaluenoteform = ValueNoteForm(request.POST, instance=noteObj)
				if editvaluenoteform.is_valid():
					editvaluenoteform.save()
					return HttpResponseRedirect(link)
		elif 'dnoteSub' in request.POST:
			collectnotejournalid = CollectNoteJournalID(request.POST)
			if collectnotejournalid.is_valid():
				note_id = collectnotejournalid.cleaned_data['note_id']
				noteToDelete = goal.valuenote.get(id=note_id)
				deletevaluenoteform = DeleteValueNoteForm(request.POST, instance=noteToDelete)
				if deletevaluenoteform.is_valid():
					noteToDelete.delete()
					return HttpResponseRedirect(link)
		elif 'journalSub' in request.POST:
			valuejournalform = ValueJournalForm(request.POST)
			if valuejournalform.is_valid():
				vjrnl = valuejournalform.save(commit=False)
				vjrnl.goal = goal
				vjrnl.save()
				return HttpResponseRedirect(link)
		elif 'ejournalSub' in request.POST:
			collectnotejournalid = CollectNoteJournalID(request.POST)
			if collectnotejournalid.is_valid():
				journal_id = collectnotejournalid.cleaned_data['journal_id']
				journalObj = goal.valuejournal.get(id=journal_id)
				editvaluejournalform = ValueJournalForm(request.POST, instance=journalObj)
				if editvaluejournalform.is_valid():
					editvaluejournalform.save()
					return HttpResponseRedirect(link)
		elif 'djournalSub' in request.POST:
			collectnotejournalid = CollectNoteJournalID(request.POST)
			if collectnotejournalid.is_valid():
				journal_id = collectnotejournalid.cleaned_data['journal_id']
				journalToDelete = goal.valuejournal.get(id=journal_id)
				deletevaluejournalform = DeleteValueJournalForm(request.POST, instance=journalToDelete)
				if deletevaluejournalform.is_valid():
					journalToDelete.delete()
					return HttpResponseRedirect(link)
	return render(request, 'goals/valuegoals.html', {'user' : user, 'title' : title, 'goalJSON': mark_safe(goalJSON), 
				'updates': mark_safe(updates), 'goal' : goal, 'editvaluegoalform' : editvaluegoalform, 
				'deletevaluegoalform' : deletevaluegoalform, 'visual': visual, 'valueupdateform': valueupdateform,
				'editupdateform': editupdateform, 'collectupdateidform':collectupdateidform, 'presentValue':presentValue,
				'link': str(link), 'valuenoteform': valuenoteform, 'editvaluenoteform': editvaluenoteform, 
				'deletevaluenoteform': deletevaluenoteform, 'valuejournalform': valuejournalform, 'deletevaluejournalform': deletevaluejournalform, 
				'editvaluejournalform': editvaluejournalform, 'collectnotejournalid': collectnotejournalid, 'journalJSON': mark_safe(journalJSON), 
				'noteJSON' : mark_safe(noteJSON)})		

@login_required
def pgoals(request, username, title, id):
	"""
	Displays a progress goal
	"""
	user = request.user
	
	#goal variables
	goal = request.user.progressgoal.get(id=id)
	progressupdates = goal.progressupdate.all()
	progressnotes = goal.progressnote.all()
	progressjournal = goal.progressjournal.all().order_by("date")
	
	#visual
	visual = goal.visual
	link = ('/user/%s/pgoals/%s%d/'%(request.user.username, title, goal.id))
	
	#Form variables
	editprogressgoalform = ProgressGoalForm(instance=goal)
	cmplprogressgoalform = ProgressGoalForm(instance=goal)
	deleteprogressgoalform = DeleteProgressGoalForm()
	progressupdateform = ProgressUpdateForm()
	editupdateform = ProgressUpdateForm()
	collectupdateidform = CollectUpdateIDForm()
	
	#display forms
	progressnoteform = ProgressNoteForm()
	editprogressnoteform = ProgressNoteForm()
	deleteprogressnoteform = DeleteProgressNoteForm()
	progressjournalform = ProgressJournalForm()
	editprogressjournalform = ProgressJournalForm()
	deleteprogressjournalform = DeleteProgressJournalForm()
	collectnotejournalid = CollectNoteJournalID()
	
	#JSON encoder upgrade for decimals
	class DecimalEncoder(json.JSONEncoder):
		def _iterencode(self, o, markers=None):
			if isinstance(o, decimal.Decimal):
				return (str(o) for o in [o])
			return super(DecimalEncoder, self)._iterencode(o, markers)
	
	#converts datetime object for forms
	def getDateTime(date):
		if date is None:
			return date
		else:
			return str(date)

	#remove trailing zeros
	def zeroOut(val):
		newval = val.rstrip("0")
		last = len(newval)-1
		if (newval[last] == "."):
			return newval.rstrip(".")
		else:
			return newval
			
	#calculate totals and process 
	def processUpdate(up):
		upda = {"update_value": str(up.value), "update_description": up.description, 
			"update_date_created": getDateTime(up.date_created), "update_id": up.id,
			"update_last_updated": getDateTime(up.last_updated),"update_value_nozero": (zeroOut(str(up.value)))}
		return upda
	
	updates = []
	total = goal.startValue
	for upd in progressupdates:
		updates.append(processUpdate(upd))
	if (len(progressupdates) == 0):
		presentValue = goal.startValue
	else:
		presentValue = progressupdates[len(progressupdates)-1].value
	
	updates = json.dumps(updates)

	gl = {"goal_title": goal.title, "goal_description": goal.description, "goal_determinate": goal.determinate, 
		"goal_valueType": goal.valueType, "goal_startValue": str(goal.startValue), 
		"goal_endValue": str(goal.endValue), "goal_private": goal.private, "goal_completed": goal.completed, 
		"goal_complete_by": getDateTime(goal.complete_by), "goal_date_completed": getDateTime(goal.date_completed), 
		"goal_last_updated": getDateTime(goal.last_updated), "goal_date_created": getDateTime(goal.date_created), 
		"goal_id": goal.id, "goal_nozero": (zeroOut(str(goal.startValue))), "goal_currentNoZero": (zeroOut(str(presentValue))),
		"goal_endNoZero": (zeroOut(str(goal.endValue)))}
	goalJSON = json.dumps(gl, cls=DecimalEncoder)
	
	#get journal in JSON
	def journalProcess(jnl):
		jnl = {'journal_entry': jnl.entry, 'journal_title': jnl.title, 'journal_date': getDateTime(jnl.date), 'journal_id': jnl.id}
		return jnl
	journals = []
	for journal in progressjournal:
		journals.append(journalProcess(journal))
	journalJSON = json.dumps(journals)
	
	#get notes in JSON
	def notesProcess(nt):
		nt = {'note_id': nt.id, 'note_note': nt.note}
		return nt
	notes = []
	for note in progressnotes:
		notes.append(notesProcess(note))
	noteJSON = json.dumps(notes)
	
	#handle forms
	if request.method == 'POST':
		if 'editSub' in request.POST:
			editprogressgoalform = ProgressGoalForm(request.POST, instance=goal)
			if editprogressgoalform.is_valid():
				newgoal = editprogressgoalform.save()
				if (not newgoal.determinate):
					newgoal.endValue = None
					newgoal.complete_by = None
					newgoal.completed = False
					newgoal.date_completed = None
					newgoal.save()
					return HttpResponseRedirect(link)
				else:
					cmpl = False
					current = presentValue
					if (newgoal.endValue > newgoal.startValue):
						if (current >= newgoal.endValue):
							cmpl = True
						else:
							cmpl = False
					else:
						if (current <= newgoal.endValue):
							cmpl = True
						else:
							cmpl = False
					if cmpl:
						newgoal.completed = True
						newgoal.date_completed = newgoal.last_updated
						newgoal.save()
						return HttpResponseRedirect(link)
					else: 
						newgoal.completed = False
						newgoal.date_completed = None
						newgoal.save()
						return HttpResponseRedirect(link)
		elif 'deleteSub' in request.POST:
			toDelete = goal
			deleteprogressgoalform = DeleteProgressGoalForm(request.POST, instance=toDelete)
			if deleteprogressgoalform.is_valid():
				toDelete.delete()
				return HttpResponseRedirect('/user/%s/'%request.user.username)
		elif 'updateSub' in request.POST:
			progressupdateform = ProgressUpdateForm(request.POST)
			if progressupdateform.is_valid():
				puform = progressupdateform.save(commit=False)
				puform.goal = goal
				newval = puform.value
				updateobj = progressupdateform.save()
				if (goal.determinate):
					cmpl = False
					if (goal.endValue > goal.startValue):
						if (newval >= goal.endValue):
							cmpl = True
						else:
							cmpl = False
					else:
						if (newval <= goal.endValue):
							cmpl = True
						else:
							cmpl = False
					if cmpl:
						goal.completed = True
						goal.date_completed = updateobj.date_created
						goal.save()
						return HttpResponseRedirect(link)
					else: 
						goal.completed = False
						goal.date_completed = None
						goal.save()
						return HttpResponseRedirect(link)
				else:
					return HttpResponseRedirect(link)
		elif 'editUpdateSub' in request.POST:
			collectupdateidform = CollectUpdateIDForm(request.POST)
			if collectupdateidform.is_valid():
				editupdate_id = collectupdateidform.cleaned_data['editupdate_id']
				clean_upd = goal.progressupdate.get(id=editupdate_id)
				editupdateform = ProgressUpdateForm(request.POST, instance=clean_upd)
				if editupdateform.is_valid():
					updateobj = editupdateform.save()
					newval = updateobj.value
					if (goal.determinate):
						cmpl = False
						if (goal.endValue > goal.startValue):
							if (newval >= goal.endValue):
								cmpl = True
							else:
								cmpl = False
						else:
							if (newval <= goal.endValue):
								cmpl = True
							else:
								cmpl = False
						if cmpl:
							goal.completed = True
							goal.date_completed = updateobj.date_created
							goal.save()
							return HttpResponseRedirect(link)
						else:
							goal.completed = False
							goal.date_completed = None
							goal.save()
							return HttpResponseRedirect(link)
					else:
						return HttpResponseRedirect(link)
		#Display subs
		elif 'noteSub' in request.POST:
			progressnoteform = ProgressNoteForm(request.POST)
			if progressnoteform.is_valid():
				pnote = progressnoteform.save(commit=False)
				pnote.goal = goal
				pnote.save()
				return HttpResponseRedirect(link)
		elif 'enoteSub' in request.POST:
			collectnotejournalid = CollectNoteJournalID(request.POST)
			if collectnotejournalid.is_valid():
				note_id = collectnotejournalid.cleaned_data['note_id']
				noteObj = goal.progressnote.get(id=note_id)
				editprogressnoteform = ProgressNoteForm(request.POST, instance=noteObj)
				if editprogressnoteform.is_valid():
					editprogressnoteform.save()
					return HttpResponseRedirect(link)
		elif 'dnoteSub' in request.POST:
			collectnotejournalid = CollectNoteJournalID(request.POST)
			if collectnotejournalid.is_valid():
				note_id = collectnotejournalid.cleaned_data['note_id']
				noteToDelete = goal.progressnote.get(id=note_id)
				deleteprogressnoteform = DeleteProgressNoteForm(request.POST, instance=noteToDelete)
				if deleteprogressnoteform.is_valid():
					noteToDelete.delete()
					return HttpResponseRedirect(link)
		elif 'journalSub' in request.POST:
			progressjournalform = ProgressJournalForm(request.POST)
			if progressjournalform.is_valid():
				pjrnl = progressjournalform.save(commit=False)
				pjrnl.goal = goal
				pjrnl.save()
				return HttpResponseRedirect(link)
		elif 'ejournalSub' in request.POST:
			collectnotejournalid = CollectNoteJournalID(request.POST)
			if collectnotejournalid.is_valid():
				journal_id = collectnotejournalid.cleaned_data['journal_id']
				journalObj = goal.progressjournal.get(id=journal_id)
				editprogressjournalform = ProgressJournalForm(request.POST, instance=journalObj)
				if editprogressjournalform.is_valid():
					editprogressjournalform.save()
					return HttpResponseRedirect(link)
		elif 'djournalSub' in request.POST:
			collectnotejournalid = CollectNoteJournalID(request.POST)
			if collectnotejournalid.is_valid():
				journal_id = collectnotejournalid.cleaned_data['journal_id']
				journalToDelete = goal.progressjournal.get(id=journal_id)
				deleteprogressjournalform = DeleteProgressJournalForm(request.POST, instance=journalToDelete)
				if deleteprogressjournalform.is_valid():
					journalToDelete.delete()
					return HttpResponseRedirect(link)
	return render(request, 'goals/progressgoals.html', {'user' : user, 'title' : title, 'goalJSON': mark_safe(goalJSON), 
				'updates': mark_safe(updates), 'goal' : goal, 'editprogressgoalform' : editprogressgoalform, 
				'deleteprogressgoalform' : deleteprogressgoalform, 'visual': visual, 'progressupdateform': progressupdateform,
				'editupdateform': editupdateform, 'collectupdateidform':collectupdateidform, 'presentValue':presentValue,
				'progressnoteform': progressnoteform, 'editprogressnoteform': editprogressnoteform, 'deleteprogressnoteform': deleteprogressnoteform, 
				'progressjournalform': progressjournalform, 'deleteprogressjournalform': deleteprogressjournalform, 
				'editprogressjournalform': editprogressjournalform, 'collectnotejournalid': collectnotejournalid, 'journalJSON': mark_safe(journalJSON), 
				'noteJSON' : mark_safe(noteJSON)})		

def test_view(request):
	return render(request, 'testview.html')