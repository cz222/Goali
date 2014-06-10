from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.template import Template, Context
from django.template.loader import get_template

from forms import OneShotGoalForm

@login_required
def myprofile(request, username):
	user = request.user
	
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
def osgoals(request, title):
	user = request.user
	
	#goal variables
	oneshotgoalcount = request.user.oneshotgoal.count()
	oneshotgoals = request.user.oneshotgoal.all()
	
	return render(request, 'oneshotgoals.html', {'user' : user })