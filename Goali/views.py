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

from forms import RegisterForm, LoginForm, ContactForm
from accounts.models import Forum, Thread, Post

def homepage(request):
	"""
	Register a new user. Salt hash (use sha) and email them an activation key
	"""
	if request.user.is_authenticated():
		return HttpResponseRedirect('/user/%s/'%request.user.username)
	else:
		if request.method == 'POST':
			if 'registerSub' in request.POST:
				registerform = RegisterForm(request.POST)
				loginform = LoginForm()
				if registerform.is_valid():
					#Make activation key, STILL NEED TO WRITE VIEW FOR CONFIRMATION
					#salt = sha.new(str(random.random())).hexdigest()[:5]
					#activation_key = sha.new(salt+new_user.username).hexdigest()
					#key_expires = datetime.datetime.today() + datetime.timedelta(92)
					
					#save new user
					new_user = registerform.save()
					
					#send email
					#email_subject = 'Your Goali Account Confirmation'
					#email_body = "Hello, %s! Thank you for signing up for a Goali account!\nTo activate your account, click this link within 48 \hours:\n\nhttp://example.com/accounts/confirm/%s" % (new_user.username,new_profile.activation_key)
					#send_mail(email_subject,email_body,'admin@goali.net',[new_user.email])
					
					#logging in user
					user = auth.authenticate(username=request.POST['username'], password=request.POST['password1'])
					if user is not None:
						if user.is_active:
							auth.login(request, user)
	#						request.sessions['member_id'] = m.id
							return HttpResponseRedirect('/%s/'%request.user.username)
					else:
						return HttpResponseRedirect('login failed')
			elif 'loginSub' in request.POST:
				try:
					loginform = LoginForm(request.POST)
					registerform = RegisterForm()
					if loginform.is_valid():
						username = request.POST.get('username', '')
						password = request.POST.get('password', '')
						if not "@" in username:
							user = auth.authenticate(username=username, password=password)
							#if user is not None and user.is_active:
							if user is not None:
								if user.is_active:
									auth.login(request, user)
	#								request.sessions['member_id'] = m.id
									return HttpResponseRedirect('/user/%s/'%request.user.username)
								else:
									return HttpResponseRedirect('your account is not active, please contact the site administrator')
							else:
								HttpResponse("your username and password are incorrect")
						else:
							acct = loginform.get_user(username)
							user = auth.authenticate(username=acct, password=password)
							if user is not None:
								if user.is_active:
									auth.login(request, user)
	#								request.sessions['member_id'] = m.id
									return HttpResponseRedirect('/user/%s/'%request.user.username)
								else:
									return HttpResponseRedirect('your account is not active, please contact the site administrator')
							else:
								HttpResponse("your username and password are incorrect")	
				except User.DoesNotExist:
					return HttpResponse("Your username and password didn't match.")
		else:
			registerform = RegisterForm()
			loginform = LoginForm()
		return render(request, "homepage.html", { 'registerform': registerform, 'loginform': loginform } )

def login_new(request):
	"""
	Login as a new user. Still needs to be finished.
	"""
	return HttpResponseRedirect("/")

def logout(request):
	"""
	Logout
	"""
	auth.logout(request)
	return HttpResponseRedirect("/")

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
	
#about page
def about(request):
	return render(request, "about.html")
	
#lounge page
def lounge(request):
	if request.user.is_authenticated():
		return render(request, "lounge-auth.html")
	else:
		registerform = RegisterForm()
		loginform = LoginForm()
		if request.method == 'POST':
			if 'registerSub' in request.POST:
				registerform = RegisterForm(request.POST)
				if registerform.is_valid():
					new_user = registerform.save()
					user = auth.authenticate(username=request.POST['username'], password=request.POST['password1'])
					if user is not None:
						if user.is_active:
							auth.login(request, user)
							return HttpResponseRedirect('/%s/'%request.user.username)
					else:
						return HttpResponseRedirect('login failed')
			elif 'loginSub' in request.POST:
				try:
					loginform = LoginForm(request.POST)
					if loginform.is_valid():
						username = request.POST.get('username', '')
						password = request.POST.get('password', '')
						if not "@" in username:
							user = auth.authenticate(username=username, password=password)
							if user is not None:
								if user.is_active:
									auth.login(request, user)
									return HttpResponseRedirect('/user/%s/'%request.user.username)
								else:
									return HttpResponseRedirect('your account is not active, please contact the site administrator')
							else:
								HttpResponse("your username and password are incorrect")
						else:
							acct = loginform.get_user(username)
							user = auth.authenticate(username=acct, password=password)
							if user is not None:
								if user.is_active:
									auth.login(request, user)
									return HttpResponseRedirect('/user/%s/'%request.user.username)
								else:
									return HttpResponseRedirect('your account is not active, please contact the site administrator')
							else:
								HttpResponse("your username and password are incorrect")	
				except User.DoesNotExist:
					return HttpResponse("Your username and password didn't match.")
		return render(request, "lounge.html", { 'registerform': registerform, 'loginform': loginform })

def add_csrf(request, **kwargs):
	d = dict(user=request.user, **kwargs)
	d.update(csrf(request))
	return datetime

def mk_paginator(request, items, num_items):
	"""
	Create and return a paginator
	"""
	paginator = Paginator(items, num_items)
	try:
		page = int(request.GET.get("page", '1'))
	except ValueError: 
		page = 1
		
	try:
		items = paginator.page(page)
	except (invalidPage, EmptyPage):
		items = paginator.page(paginator.num_pages)
	return items
	
#Forums
def forums(request):
	"""
	Forum mainpage, lists all the forums and stuff
	"""
	forums = Forum.objects.all();
	return render(request, "forums/forums.html", {'forums': forums})
	
def forum(request, id):
	"""
	Forum page, lists all the threads in a forum
	"""
	threads = Thread.objects.filter(id=id).order_by("-created")
	threads = mk_paginator(request, threads, 20)
	return render(request, "forums/forum.html", {'threads': threads, 'id': id})
	#return render_to_response("forums/forum.html", add_csrf(request, threads=threads, id=id))

def thread(request, id):
	"""
	Listing of posts in a thread.
	"""
	posts = Post.objects.filter(id=id).order_by("created")
	posts = mk_paginator(request, posts, 15)
	title = Thread.objects.get(id=id).title
	return render(request, "forums/thread.html", {'posts': posts, 'id': id, 'title': title, 'media_url': MEDIA_URL})
	#return render_to_response("forums/thread.html", add_csrf(request, p

def post(request, ptype, id):
	"""
	Display a post
	"""
	action = reverse("dbe.forum.views.%s" % ptype, args=[id])
	if ptype == "new_thread":
		title = "Start New Topic"
		subject = ''
	elif ptype == "reply":
		title = "Reply"
		subject = "re: " + Thread.objects.get(pk=pk).title
	return render_to_response("forum/post.html", add_csrf(request, subject=subject, action=action, title=title))
	
def new_thread(request, id):
	"""
	Start a new thread
	"""
	p = request.POST
	if p["subject"] and p["body"]:
		forum = Forum.objects.get(id=id)
		thread = Thread.objects.create(forum=forum, title=p["subject"], creator=request.user)
		Post.objects.create(thread=thread, title=p["subject"], body=p["body"], creator=request.user)
	return HttpResponseRedirect(reverse("dbe.forum.views.forum", args=[id]))
	
def reply(request, id):
	"""
	Reply to a thread
	"""
	p = request.POST
	if p["body"]:
		thread = Thread.objects.get(id=id)
		post = Post.objects.create(thread=thread, title=p["subject"], body=p["body"], creator=request.user)
	return HttpResponseRedirect(reverse("dbe.forum.views.thread", args=[id])+"?page=last")