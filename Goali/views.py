import datetime, random, hashlib
from django.contrib import auth
from django.core.context_processors import csrf
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response, get_object_or_404
from django.template import Template, Context
from django.template.loader import get_template

from forms import RegisterForm, ContactForm
from accounts.models import User

def homepage(request):
	"""
	Register a new user. Salt hash (use sha) and email them an activation key
	"""
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid() and form.clean_passwords and form.clean_username and form.clean_email:
			#Make activation key, STILL NEED TO WRITE VIEW FOR CONFIRMATION
			#salt = sha.new(str(random.random())).hexdigest()[:5]
			#activation_key = sha.new(salt+new_user.username).hexdigest()
			#key_expires = datetime.datetime.today() + datetime.timedelta(92)
			
			#save new user
			new_user = form.save()
			
			#send email
			#email_subject = 'Your Goali Account Confirmation'
			#email_body = "Hello, %s! Thank you for signing up for a Goali account!\nTo activate your account, click this link within 48 \hours:\n\nhttp://example.com/accounts/confirm/%s" % (new_user.username,new_profile.activation_key)
			#send_mail(email_subject,email_body,'admin@goali.net',[new_user.email])
			
			return HttpResponseRedirect("/account/")
	else:
		form = RegisterForm()
	return render(request, "homepage.html", { 'form': form,})

def login(request):
	if request.method != 'POST':
		#test for cookies
		if request.session.test_cookie_worked():
			request.session.delete_test_cookie()
			return
		raise Http404('Only POSTs are allowed')
	try:
		m = Member.objects.get(username=request.POST['username'])
		if m.password == request.POST['password']:
			request.sessions['member_id'] = m.id
			return HttpResponseRedirect('/you-are-logged-in/')
	except Member.DoesNotExist:
		return HttpResponse("Your username and password didn't match.")


def logout(request):
	try:
		del request.session['member_id']
	except KeyError:
		pass
	return HttpResponse("You're logged out.")

#contact web owner
def contact(request):
	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			send_mail(
				cd['subject'],
				cd['message'],
				cd.get('email', 'noreply@example.com'),
				['siteowner@example.com'],
			)
		return HttpResponseRedirect('/contact/thanks/')
	else:
		form = ContactForm()
	return render(request, 'contact_form.html', {'form': form})

