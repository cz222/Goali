from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms.Form):
    username = models.CharField(required = True, max_length=25)
	email = forms.EmailField(required = True)
	first_name = forms.CharField(required = True)
	last_name = forms.CharField(required = True)
	password1 = models.CharField(required = True, max_length=30)
	password2 = models.CharField(required = True, max_length=30)
	
	class Meta:
		model = User
		fields = ('username', 'email', 'first_name', 'last_name')
	
	def save(self, commit = True):
		user = super(RegisterForm, self).save(commit = False)
		user.email = self.cleaned_data['email']
		user.first_name = self.cleaned_data['first_name']
		user.last_name = self.cleaned_data['last_name']
		user.set_password(self.cleaned_data['password1'])
		
		if commit:
			user.save()
		
		return user

class ContactForm(forms.Form):
	subject = forms.CharField(max_length=100, label='Subject')
	email = forms.EmailField(required=False, label='E-Mail Address (optional)')
	message = forms.CharField(widget=forms.Textarea, label='Subject')
	
