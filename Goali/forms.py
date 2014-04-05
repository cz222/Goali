from django import forms
from django.contrib.auth.models import User
from django.core.validators import validate_email

class RegisterForm(forms.ModelForm):
	"""
	Form for registering new use account
	"""
	username = forms.RegexField(required = True, label='', widget=forms.TextInput(attrs={'placeholder': 'Username'}), max_length=30, regex=r'^[\w.@+-]+$', error_messages={'invalid': "This value may contain only letters, numbers, and @/./+/-/_ characters."})
	email = forms.EmailField(max_length=75, required = True, label='', widget=forms.TextInput(attrs={'placeholder': 'Email'}))
	password1 = forms.CharField(max_length=70, required = True, label='', widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
	password2 = forms.CharField(max_length=70, required = True, label='', widget=forms.PasswordInput(attrs={'placeholder': 'Repeat Password'}))

	class Meta:
		model = User
		fields = ('username', 'email',)
	
	def clean_username(self):
		"""
		Validate the username to be alphanumeric and see if it's in use.
		"""
		username = self.cleaned_data['username']
		if User.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
			raise forms.ValidationError('This username is already taken.')
		else:
			return username
	
	def clean_email(self):
		"""
		Validates that the email isn't in use
		"""
		email = self.cleaned_data['email']
		if User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
			raise forms.ValidationError('This email is already registered.')
		else:
			return email
			
	def clean_password2(self):
		"""
		Validate that the two passwords match
		"""
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Your passwords don't match.")
		return password2
	
	def save(self, commit = True):
		"""
		Save values and return object for storing
		"""
		user = super(RegisterForm, self).save(commit = False)
		user.email = self.cleaned_data['email']
		user.set_password(self.cleaned_data['password1'])
		
		if commit:
			user.save()
		return user


		
class RegisterTermsOfService(RegisterForm):
	"""
	adds required checkbox for reading Terms of Service
	"""
	tos = forms.BooleanField(required=True, widget=forms.CheckboxInput, label='By checking this box, I have read and agree to the Terms of Service', error_messages={'required': "You must agree to the terms to register"})
	
class ContactForm(forms.Form):
	subject = forms.CharField(max_length=100, label='Subject')
	email = forms.EmailField(required=False, label='E-Mail Address (optional)')
	message = forms.CharField(widget=forms.Textarea, label='Subject')
	
