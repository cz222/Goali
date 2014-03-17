from django.template.loader import get_template
from django.shortcuts import render
from django.template import Template, Context
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib import auth
from django.core.context_processors import csrf
from forms import RegisterForm, ContactForm
import datetime

#REGISTRATION AND LOGIN/LOGOUT
	
def register(request):
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect("/accounts/")
	else:
		form = UserCreationForm()
	return render(request, "registration/register.html", { 'form': form,})
	
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




def hello(request):
	return HttpResponse("Hello world")
	
def current_datetime(request):
	now = datetime.datetime.now()
	t = get_template('current_datetime.html')
	html = t.render(Context({'current_date': now}))
	return HttpResponse(html)

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

