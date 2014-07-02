from datetime import datetime
from django import forms
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.contrib import auth
from django.forms.formsets import formset_factory

from django.forms.models import inlineformset_factory
from models import OneShotGoal, OneShotJournal, OneShotNote, MilestoneGoal, Milestone, MilestoneGoalJournal, MilestoneGoalNote, MilestoneNote, SubMilestone, SubMilestoneNote

class OneShotGoalForm(forms.ModelForm):
	"""
	Form for creating one shot goals
	"""
	
	title = forms.CharField(required = True, label='', widget=forms.TextInput(attrs={'placeholder': 'Title*'}), max_length=75)
	description = forms.CharField(max_length=300, required = False, label='', widget=forms.Textarea(attrs={'placeholder': 'Goal Description'}))
	private = forms.BooleanField(required=False, label='Private')
	completed = forms.BooleanField(required=False, label='Completed')
	date_completed = forms.DateField(required=False, label='MM/DD/YYYY')

	class Meta:
		model = OneShotGoal
		fields = ('title', 'description', 'private', 'completed', 'date_completed', )
	
	def clean_title(self):
		"""
		Validate title and see if it's in use.
		"""
		title = self.cleaned_data['title']
		return title

	def clean_private(self):
		"""
		Validate private
		"""
		private = self.cleaned_data['private']
		if private is None:
			return False
		else:
			return private

	def clean_completed(self):
		"""
		Raise Error if date_completed has something when the goal is not yet completed and vice versa
		"""
		completed = self.cleaned_data.get('completed')
		date_completed = self.cleaned_data.get('date_completed')
		if completed is None:
			completed = False
		return completed
	
	def clean_date_completed(self):
		"""
		Raise Error if date_completed is greater than the current date.
		"""
		date_completed = self.cleaned_data.get('date_completed')
		completed = self.cleaned_data.get('completed')
		if (not completed) and (not (date_completed is None)):
			raise forms.ValidationError('Please mark the goal as completed.')
		elif completed and (date_completed is None):
			raise forms.ValidationError('Please enter a date of completion.')
		elif (date_completed is None):
			return date_completed
		else:
			if (datetime.now().date() < date_completed):
				raise forms.ValidationError('Time travel is not allowed.')
			else:
				return date_completed
	
class OneShotJournalForm(forms.ModelForm):
	"""
	Form for creating journal entries for one shot goals
	"""
	
	entry = forms.CharField(required=True, label='', widget=forms.Textarea(attrs={'placeholder': 'Journal Entry'}))

	class Meta:
		model = OneShotJournal
		fields = ('entry',)
		
class OneShotNoteForm(forms.ModelForm):
	"""
	Form for creating notes for one shot goals
	"""
	
	note = forms.CharField(required=True, label='', widget=forms.Textarea(attrs={'placeholder': 'Note'}))
	
	class Meta:
		model = OneShotNote
		fields = ('note',)

class DeleteOneShotJournalForm(forms.Form):
	object_id = forms.CharField(max_length=500, required = False, label='', widget=forms.TextInput(attrs={'placeholder': 'Object_id'}))
		
class DeleteOneShotNoteForm(forms.ModelForm):
	class Meta:
		model = OneShotNote
		fields = []

class DeleteOneShotForm(forms.ModelForm):
	class Meta:
		model = OneShotGoal
		fields = []
		
#MilestoneGoal, Milestone, SubMilestone, SubSubMilestone
#completed = forms.TypedChoiceField(required=False, label='Completed', coerce=lambda x: x =='True', choices=((False, 'No'), (True, 'Yes')), initial='No', widget=forms.RadioSelect)
class MilestoneGoalForm(forms.ModelForm):
	"""
	Form for creating Milestone Goals
	"""
	
	title = forms.CharField(required = True, label='', widget=forms.TextInput(attrs={'placeholder': 'Title*'}), max_length=75)
	description = forms.CharField(max_length=300, required = False, label='', widget=forms.Textarea(attrs={'placeholder': 'Goal Description'}))
	private = forms.BooleanField(required=False, label='Private')
	completed = forms.BooleanField(required=False, label='Completed')
	date_completed = forms.DateField(required=False, label='MM/DD/YYYY')

	class Meta:
		model = MilestoneGoal
		fields = ('title', 'description', 'private', 'completed', 'date_completed',)
	
	def clean_title(self):
		"""
		Validate title and see if it's in use.
		"""
		title = self.cleaned_data['title']
		return title
	
	def clean_private(self):
		"""
		Validate private
		"""
		private = self.cleaned_data['private']
		if private is None:
			return False
		else:
			return private
	
	def clean_completed(self):
		"""
		Raise Error if date_completed has something when the goal is not yet completed and vice versa
		"""
		completed = self.cleaned_data.get('completed')
		date_completed = self.cleaned_data.get('date_completed')
		if completed is None:
			completed = False
		return completed
	
	def clean_date_completed(self):
		"""
		Raise Error if date_completed is greater than the current date.
		"""
		date_completed = self.cleaned_data.get('date_completed')
		completed = self.cleaned_data.get('completed')
		if (not completed) and (not (date_completed is None)):
			raise forms.ValidationError('Please mark the goal as completed.')
		elif completed and (date_completed is None):
			raise forms.ValidationError('Please enter a date of completion.')
		elif (date_completed is None):
			return date_completed
		else:
			if (datetime.now().date() < date_completed):
				raise forms.ValidationError('Time travel is not allowed.')
			else:
				return date_completed

class DeleteMilestoneGoalForm(forms.ModelForm):
	class Meta:
		model = MilestoneGoal
		fields = []
		
class MilestoneGoalJournalForm(forms.ModelForm):
	"""
	Form for creating journal entries for milestone goals
	"""
	
	entry = forms.CharField(required=True, label='', widget=forms.Textarea(attrs={'placeholder': 'Journal Entry'}))

	class Meta:
		model = MilestoneGoalJournal
		fields = ('entry',)
		
class MilestoneGoalNoteForm(forms.ModelForm):
	"""
	Form for creating notes milestone goals
	"""
	
	note = forms.CharField(required=True, label='', widget=forms.Textarea(attrs={'placeholder': 'Note'}))
	
	class Meta:
		model = MilestoneGoalNote
		fields = ('note',)
		
class MilestoneForm(forms.ModelForm):
	"""
	Form for creating Milestones
	"""
	
	title = forms.CharField(required = True, label='', widget=forms.TextInput(attrs={'placeholder': 'Title*'}), max_length=75)
	description = forms.CharField(max_length=300, required = False, label='', widget=forms.Textarea(attrs={'placeholder': 'Goal Description'}))
	private = forms.BooleanField(required=False, label='Private', initial=False)
	completed = forms.BooleanField(required=False, label='Completed')
	date_completed = forms.DateField(required=False, label='MM/DD/YYYY')

	class Meta:
		model = Milestone
		fields = ('title', 'description', 'private', 'completed', 'date_completed',)

	def clean_private(self):
		"""
		Validate private
		"""
		private = self.cleaned_data['private']
		if private is None:
			return False
		else:
			return private
		
	def clean_completed(self):
		"""
		Raise Error if date_completed has something when the goal is not yet completed and vice versa
		"""
		completed = self.cleaned_data.get('completed')
		date_completed = self.cleaned_data.get('date_completed')
		if completed is None:
			completed = False
		return completed
	
	def clean_date_completed(self):
		"""
		Raise Error if date_completed is greater than the current date.
		"""
		date_completed = self.cleaned_data.get('date_completed')
		completed = self.cleaned_data.get('completed')
		if (not completed) and (not (date_completed is None)):
			raise forms.ValidationError('Please mark the goal as completed.')
		elif completed and (date_completed is None):
			raise forms.ValidationError('Please enter a date of completion.')
		elif (date_completed is None):
			return date_completed
		else:
			if (datetime.now().date() < date_completed):
				raise forms.ValidationError('Time travel is not allowed.')
			else:
				return date_completed

class MilestoneNoteForm(forms.ModelForm):
	"""
	Form for creating notes for milestones
	"""
	
	note = forms.CharField(required=True, label='', widget=forms.Textarea(attrs={'placeholder': 'Note'}))
	
	class Meta:
		model = MilestoneNote
		fields = ('note',)
					
class SubMilestoneForm(forms.ModelForm):
	"""
	Form for creating Sub-Milestones
	"""
	
	title = forms.CharField(required = True, label='', widget=forms.TextInput(attrs={'placeholder': 'Title*'}), max_length=75)
	description = forms.CharField(max_length=300, required = False, label='', widget=forms.Textarea(attrs={'placeholder': 'Goal Description'}))
	completed = forms.TypedChoiceField(required=False, label='Completed', coerce=lambda x: x =='True', choices=((False, 'No'), (True, 'Yes')), widget=forms.RadioSelect)
	date_completed = forms.DateField(required=False, label='MM/DD/YYYY')

	class Meta:
		model = SubMilestone
		fields = ('title', 'description', 'completed', 'date_completed',)

	def clean_completed(self):
		"""
		Raise Error if date_completed has something when the goal is not yet completed and vice versa
		"""
		completed = self.cleaned_data.get('completed')
		date_completed = self.cleaned_data.get('date_completed')
		if completed is None:
			completed = False
		return completed
	
	def clean_date_completed(self):
		"""
		Raise Error if date_completed is greater than the current date.
		"""
		date_completed = self.cleaned_data.get('date_completed')
		completed = self.cleaned_data.get('completed')
		if (not completed) and (not (date_completed is None)):
			raise forms.ValidationError('Please mark the goal as completed.')
		elif completed and (date_completed is None):
			raise forms.ValidationError('Please enter a date of completion.')
		elif (date_completed is None):
			return date_completed
		else:
			if (datetime.now().date() < date_completed):
				raise forms.ValidationError('Time travel is not allowed.')
			else:
				return date_completed

class SubMilestoneNoteForm(forms.ModelForm):
	"""
	Form for creating notes for sub-milestones
	"""
	
	note = forms.CharField(required=True, label='', widget=forms.Textarea(attrs={'placeholder': 'Note'}))
	
	class Meta:
		model = SubMilestoneNote
		fields = ('note',)
					
#Milestone Goal formsets
MilestoneFormSet = inlineformset_factory(MilestoneGoal, Milestone, form=MilestoneForm, extra=1)