from datetime import datetime
from django import forms
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.contrib import auth
from django.forms.formsets import formset_factory
from django.forms import extras
from django.contrib.admin.widgets import AdminSplitDateTime

from django.forms.models import inlineformset_factory, BaseInlineFormSet
from models import OneShotGoal, OneShotJournal, OneShotNote
from models import MilestoneGoal, Milestone, MilestoneGoalJournal, MilestoneGoalNote, MilestoneJournal, MilestoneNote
from models import TimeOneShotGoal, TimeOneShotJournal, TimeOneShotNote 
from models import TimeMilestoneGoal, TimeMilestone, TimeMilestoneGoalJournal, TimeMilestoneGoalNote, TimeMilestoneJournal, TimeMilestoneNote
from models import ValueGoal, ValueUpdate, ValueJournal, ValueNote
from models import ProgressGoal, ProgressUpdate, ProgressJournal, ProgressNote

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

class DeleteOneShotForm(forms.ModelForm):
	"""
	Empty form used for deleting objects and avoiding CSRF attacks.
	Also used for uncomplete.
	"""
	class Meta:
		model = OneShotGoal
		fields = []
	
class OneShotNoteForm(forms.ModelForm):
	"""
	Form for creating notes for one shot goals
	"""
	note = forms.CharField(required=True, label='', widget=forms.Textarea(attrs={'placeholder': 'Note'}))
	class Meta:
		model = OneShotNote
		fields = ('note',)
		
class DeleteOneShotNoteForm(forms.ModelForm):
	class Meta:
		model = OneShotNote
		fields = []

class OneShotJournalForm(forms.ModelForm):
	entry = forms.CharField(required=True, label='', widget=forms.Textarea(attrs={'placeholder': 'Journal Entry'}))
	title = forms.CharField(required=False, label='', widget=forms.Textarea(attrs={'placeholder': 'Entry Title'}), max_length=75)
	class Meta:
		model = OneShotJournal
		fields = ('entry','title',)
		
class DeleteOneShotJournalForm(forms.ModelForm):
	class Meta:
		model = OneShotJournal
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

class MilestoneForm(forms.ModelForm):
	"""
	Form for creating Milestones
	"""
	title = forms.CharField(required = True, label='', widget=forms.TextInput(attrs={'placeholder': 'Title*'}), max_length=75)
	description = forms.CharField(max_length=300, required = False, label='', widget=forms.Textarea(attrs={'placeholder': 'Goal Description'}))
	private = forms.BooleanField(required=False, label='Private')
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

class DeleteMilestoneForm(forms.ModelForm):
	"""
	Form for deleting Milestones
	"""
	class Meta:
		model = Milestone
		fields = []
	
class MilestoneGoalNoteForm(forms.ModelForm):
	note = forms.CharField(required=True, label='', widget=forms.Textarea(attrs={'placeholder': 'Note'}))
	class Meta:
		model = MilestoneGoalNote
		fields = ('note',)
		
class DeleteMilestoneGoalNoteForm(forms.ModelForm):
	class Meta:
		model = MilestoneGoalNote
		fields = []

class MilestoneGoalJournalForm(forms.ModelForm):
	entry = forms.CharField(required=True, label='', widget=forms.Textarea(attrs={'placeholder': 'Journal Entry'}))
	title = forms.CharField(required=False, label='', widget=forms.Textarea(attrs={'placeholder': 'Entry Title'}), max_length=75)
	class Meta:
		model = MilestoneGoalJournal
		fields = ('entry','title',)
		
class DeleteMilestoneGoalJournalForm(forms.ModelForm):
	class Meta:
		model = MilestoneGoalJournal
		fields = []
	
class MilestoneNoteForm(forms.ModelForm):
	note = forms.CharField(required=True, label='', widget=forms.Textarea(attrs={'placeholder': 'Note'}))
	class Meta:
		model = MilestoneNote
		fields = ('note',)
		
class DeleteMilestoneNoteForm(forms.ModelForm):
	class Meta:
		model = MilestoneNote
		fields = []

class MilestoneJournalForm(forms.ModelForm):
	entry = forms.CharField(required=True, label='', widget=forms.Textarea(attrs={'placeholder': 'Journal Entry'}))
	title = forms.CharField(required=False, label='', widget=forms.Textarea(attrs={'placeholder': 'Entry Title'}), max_length=75)
	class Meta:
		model = MilestoneJournal
		fields = ('entry','title',)
		
class DeleteMilestoneJournalForm(forms.ModelForm):
	class Meta:
		model = MilestoneJournal
		fields = []
		
#Milestone Goal formsets
class RequiredInlineFormSet(BaseInlineFormSet):
	"""
	New formset with the first form required to be filled out
	"""
	def __init__(self, *args, **kwargs):
		super(RequiredInlineFormSet, self).__init__(*args, **kwargs)
		self.forms[0].empty_permitted = False

MilestoneFormSet = inlineformset_factory(MilestoneGoal, Milestone, form=MilestoneForm, extra=1, formset=RequiredInlineFormSet)
SubMilestoneFormSet = inlineformset_factory(Milestone, Milestone, form=MilestoneForm, extra=1, formset=RequiredInlineFormSet)

#Time Goals
class TimeOneShotGoalForm(forms.ModelForm):
	"""
	Form for creating Time Goals
	"""
	title = forms.CharField(required = True, label='', widget=forms.TextInput(attrs={'placeholder': 'Title*'}), max_length=75)
	description = forms.CharField(max_length=300, required = False, label='', widget=forms.Textarea(attrs={'placeholder': 'Goal Description'}))
	private = forms.BooleanField(required=False, label='Private')
	complete_by = forms.DateTimeField(required=True, label='Date To Complete By')
	completed = forms.BooleanField(required=False, label='Completed')
	date_completed = forms.DateField(required=False, label='Date Completed', widget=extras.SelectDateWidget(years=range(1950,2015)))

	class Meta:
		model = TimeOneShotGoal
		fields = ('title', 'description', 'private', 'complete_by', 'completed', 'date_completed',)
	
	def clean_title(self):
		title = self.cleaned_data['title']
		if (title[0] == ' '):
			raise ValidationError('Please do not lead with whitespace')
		else:
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
	
	def clean_complete_by(self):
		"""
		Raise Error if complete_by is less than the current date.
		"""
		complete_by = self.cleaned_data.get('complete_by')
		if (datetime.now() > complete_by):
			raise forms.ValidationError('Time travel is not allowed.')
		else:
			return complete_by
	
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
			if (datetime.now() < date_completed):
				raise forms.ValidationError('Time travel is not allowed.')
			else:
				return date_completed

class DeleteTimeOneShotForm(forms.ModelForm):
	class Meta:
		model = TimeOneShotGoal
		fields = []
		
class TimeOneShotNoteForm(forms.ModelForm):
	note = forms.CharField(required=True, label='', widget=forms.Textarea(attrs={'placeholder': 'Note'}))
	class Meta:
		model = TimeOneShotNote
		fields = ('note',)
		
class DeleteTimeOneShotNoteForm(forms.ModelForm):
	class Meta:
		model = TimeOneShotNote
		fields = []

class TimeOneShotJournalForm(forms.ModelForm):
	entry = forms.CharField(required=True, label='', widget=forms.Textarea(attrs={'placeholder': 'Journal Entry'}))
	title = forms.CharField(required=False, label='', widget=forms.Textarea(attrs={'placeholder': 'Entry Title'}), max_length=75)
	class Meta:
		model = TimeOneShotJournal
		fields = ('entry','title',)
		
class DeleteTimeOneShotJournalForm(forms.ModelForm):
	class Meta:
		model = TimeOneShotJournal
		fields = []

#Time Milestone Goal
class TimeMilestoneGoalForm(forms.ModelForm):
	"""
	Form for creating Time Goals
	"""
	title = forms.CharField(required = True, label='', widget=forms.TextInput(attrs={'placeholder': 'Title*'}), max_length=75)
	description = forms.CharField(max_length=300, required = False, label='', widget=forms.Textarea(attrs={'placeholder': 'Goal Description'}))
	private = forms.BooleanField(required=False, label='Private')
	complete_by = forms.DateTimeField(required=True, label='Date To Complete By*')
	completed = forms.BooleanField(required=False, label='Completed')
	date_completed = forms.DateField(required=False, label='Date Completed', widget=extras.SelectDateWidget(years=range(1950,2015)))

	class Meta:
		model = TimeMilestoneGoal
		fields = ('title', 'description', 'private', 'complete_by', 'completed', 'date_completed',)
	
	def clean_title(self):
		title = self.cleaned_data['title']
		if (title[0] == ' '):
			raise ValidationError('Please do not lead with whitespace')
		else:
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
	
	def clean_complete_by(self):
		"""
		Raise Error if complete_by is less than the current date.
		"""
		complete_by = self.cleaned_data.get('complete_by')
		if (datetime.now() > complete_by):
			raise forms.ValidationError('Time travel is not allowed.')
		else:
			return complete_by
	
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
			if (datetime.now() < date_completed):
				raise forms.ValidationError('Time travel is not allowed.')
			else:
				return date_completed

class DeleteTimeMilestoneGoalForm(forms.ModelForm):
	class Meta:
		model = TimeMilestoneGoal
		fields = []
		
class TimeMilestoneForm(forms.ModelForm):
	"""
	Form for creating Milestones
	"""
	title = forms.CharField(required = True, label='', widget=forms.TextInput(attrs={'placeholder': 'Title*'}), max_length=75)
	description = forms.CharField(max_length=300, required = False, label='', widget=forms.Textarea(attrs={'placeholder': 'Goal Description'}))
	private = forms.BooleanField(required=False, label='Private')
	complete_by = forms.DateTimeField(required=False, label='Date To Complete By')
	completed = forms.BooleanField(required=False, label='Completed')
	date_completed = forms.DateField(required=False, label='Date Completed', widget=extras.SelectDateWidget(years=range(1950,2015)))

	class Meta:
		model = TimeMilestone
		fields = ('title', 'description', 'private', 'complete_by', 'completed', 'date_completed',)
	
	def clean_title(self):
		title = self.cleaned_data['title']
		if (title[0] == ' '):
			raise ValidationError('Please do not lead with whitespace')
		else:
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
	
	def clean_complete_by(self):
		"""
		Raise Error if complete_by is less than the current date.
		"""
		complete_by = self.cleaned_data.get('complete_by')
		if complete_by is None:
			return complete_by	
		elif (datetime.now() > complete_by):
			raise forms.ValidationError('Time travel is not allowed.')
		else:
			return complete_by
	
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
			if (datetime.now() < date_completed):
				raise forms.ValidationError('Time travel is not allowed.')
			else:
				return date_completed

class DeleteTimeMilestoneForm(forms.ModelForm):
	class Meta:
		model = TimeMilestone
		fields = []

class TimeMilestoneGoalNoteForm(forms.ModelForm):
	note = forms.CharField(required=True, label='', widget=forms.Textarea(attrs={'placeholder': 'Note'}))
	class Meta:
		model = TimeMilestoneGoalNote
		fields = ('note',)
		
class DeleteTimeMilestoneGoalNoteForm(forms.ModelForm):
	class Meta:
		model = TimeMilestoneGoalNote
		fields = []

class TimeMilestoneGoalJournalForm(forms.ModelForm):
	entry = forms.CharField(required=True, label='', widget=forms.Textarea(attrs={'placeholder': 'Journal Entry'}))
	title = forms.CharField(required=False, label='', widget=forms.Textarea(attrs={'placeholder': 'Entry Title'}), max_length=75)
	class Meta:
		model = TimeMilestoneGoalJournal
		fields = ('entry','title',)
		
class DeleteTimeMilestoneGoalJournalForm(forms.ModelForm):
	class Meta:
		model = TimeMilestoneGoalJournal
		fields = []
	
class TimeMilestoneNoteForm(forms.ModelForm):
	note = forms.CharField(required=True, label='', widget=forms.Textarea(attrs={'placeholder': 'Note'}))
	class Meta:
		model = TimeMilestoneNote
		fields = ('note',)
		
class DeleteTimeMilestoneNoteForm(forms.ModelForm):
	class Meta:
		model = TimeMilestoneNote
		fields = []

class TimeMilestoneJournalForm(forms.ModelForm):
	entry = forms.CharField(required=True, label='', widget=forms.Textarea(attrs={'placeholder': 'Journal Entry'}))
	title = forms.CharField(required=False, label='', widget=forms.Textarea(attrs={'placeholder': 'Entry Title'}), max_length=75)
	class Meta:
		model = TimeMilestoneJournal
		fields = ('entry','title',)
		
class DeleteTimeMilestoneJournalForm(forms.ModelForm):
	class Meta:
		model = TimeMilestoneJournal
		fields = []
		
TimeMilestoneFormSet = inlineformset_factory(TimeMilestoneGoal, TimeMilestone, form=TimeMilestoneForm, extra=1, formset=RequiredInlineFormSet)
TimeSubMilestoneFormSet = inlineformset_factory(TimeMilestone, TimeMilestone, form=TimeMilestoneForm, extra=1, formset=RequiredInlineFormSet)

#Value Goal
class ValueGoalForm(forms.ModelForm):
	"""
	Form for creating Value Goals
	"""
	title = forms.CharField(required = True, label='', widget=forms.TextInput(attrs={'placeholder': 'Title*'}), max_length=75)
	description = forms.CharField(max_length=300, required = False, label='', widget=forms.Textarea(attrs={'placeholder': 'Goal Description'}))
	valueType = forms.CharField(required=True, label='', widget=forms.TextInput(attrs={'placeholder': 'Value Type*'}),  max_length=20)
	determinate = forms.TypedChoiceField(required=True, label='Do you have an end goal?', coerce=lambda x: x =='True', choices=((False, 'No'), (True, 'Yes')), initial='No', widget=forms.RadioSelect)
	startValue = forms.DecimalField(required=True, max_digits = 22, decimal_places=10, label='', widget=forms.TextInput(attrs={'placeholder': 'Starting Value*'}))
	endValue = forms.DecimalField(required=False, max_digits = 22, decimal_places=10, label='', widget=forms.TextInput(attrs={'placeholder': 'End Value'}))
	private = forms.BooleanField(required=False, label='Private')
	complete_by = forms.DateTimeField(required=False, label='Date To Complete By')
	completed = forms.BooleanField(required=False, label='Completed')
	date_completed = forms.DateTimeField(required=False, label='Date Completed*')

	class Meta:
		model = ValueGoal
		fields = ('title', 'description', 'valueType', 'determinate', 'startValue', 'endValue', 'private', 'complete_by', 'completed', 'date_completed',)
	
	def clean_title(self):
		title = self.cleaned_data['title']
		if (title[0] == ' '):
			raise ValidationError('Please do not lead with whitespace')
		else:
			return title
	
	def clean_determinate(self):
		determinate = self.cleaned_data['determinate']
		if (determinate is None):
			return False
		else:
			return determinate
	
	def clean_endValue(self):
		determinate = self.cleaned_data.get('determinate')
		endValue = self.cleaned_data.get('endValue')
		if (determinate):
			if (endValue is None):
				raise forms.ValidationError('Please enter an end value.')
			else:
				return endValue
	
	def clean_private(self):
		"""
		Validate private
		"""
		private = self.cleaned_data['private']
		if private is None:
			return False
		else:
			return private
	
	def clean_complete_by(self):
		"""
		Raise Error if complete_by is less than the current date.
		"""
		complete_by = self.cleaned_data.get('complete_by')
		if (complete_by is None):
			return complete_by
		elif (datetime.now() > complete_by):
			raise forms.ValidationError('Time travel is not allowed.')
		else:
			return complete_by
	
	def clean_completed(self):
		"""
		Raise Error if date_completed has something when the goal is not yet completed and vice versa
		"""
		completed = self.cleaned_data.get('completed')
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
			if (datetime.now() < date_completed):
				raise forms.ValidationError('Time travel is not allowed.')
			else:
				return date_completed

class DeleteValueGoalForm(forms.ModelForm):
	class Meta:
		model = ValueGoal
		fields = []
		
class ValueUpdateForm(forms.ModelForm):
	"""
	Form for Value Goal Updates
	"""
	value = forms.DecimalField(required=True, max_digits = 22, decimal_places=10)
	description = forms.CharField(required=False, max_length=70)
	
	class Meta:
		model = ValueUpdate
		fields = ['value', 'description',]

class ValueNoteForm(forms.ModelForm):
	note = forms.CharField(required=True, label='', widget=forms.Textarea(attrs={'placeholder': 'Note'}))
	class Meta:
		model = ValueNote
		fields = ('note',)
		
class DeleteValueNoteForm(forms.ModelForm):
	class Meta:
		model = ValueNote
		fields = []

class ValueJournalForm(forms.ModelForm):
	entry = forms.CharField(required=True, label='', widget=forms.Textarea(attrs={'placeholder': 'Journal Entry'}))
	title = forms.CharField(required=False, label='', widget=forms.Textarea(attrs={'placeholder': 'Entry Title'}), max_length=75)
	class Meta:
		model = ValueJournal
		fields = ('entry','title',)
		
class DeleteValueJournalForm(forms.ModelForm):
	class Meta:
		model = ValueJournal
		fields = []

#PROGRESS GOAL FORMS
class ProgressGoalForm(forms.ModelForm):
	"""
	Form for creating Progress Goals
	"""
	title = forms.CharField(required = True, label='', widget=forms.TextInput(attrs={'placeholder': 'Title*'}), max_length=75)
	description = forms.CharField(max_length=300, required = False, label='', widget=forms.Textarea(attrs={'placeholder': 'Goal Description'}))
	valueType = forms.CharField(required=True, label='', widget=forms.TextInput(attrs={'placeholder': 'Value Type*'}),  max_length=20)
	determinate = forms.TypedChoiceField(required=True, label='Do you have an end goal?', coerce=lambda x: x =='True', choices=((False, 'No'), (True, 'Yes')), initial='No', widget=forms.RadioSelect)
	startValue = forms.DecimalField(required=True, max_digits = 22, decimal_places=10, label='', widget=forms.TextInput(attrs={'placeholder': 'Starting Value*'}))
	endValue = forms.DecimalField(required=False, max_digits = 22, decimal_places=10, label='', widget=forms.TextInput(attrs={'placeholder': 'End Value'}))
	private = forms.BooleanField(required=False, label='Private')
	complete_by = forms.DateTimeField(required=False, label='Date To Complete By')
	completed = forms.BooleanField(required=False, label='Completed')
	date_completed = forms.DateTimeField(required=False, label='Date Completed*')

	class Meta:
		model = ProgressGoal
		fields = ('title', 'description', 'valueType', 'determinate', 'startValue', 'endValue', 'private', 'complete_by', 'completed', 'date_completed',)
	
	def clean_title(self):
		title = self.cleaned_data['title']
		if (title[0] == ' '):
			raise ValidationError('Please do not lead with whitespace')
		else:
			return title
	
	def clean_determinate(self):
		determinate = self.cleaned_data['determinate']
		if (determinate is None):
			return False
		else:
			return determinate
	
	def clean_endValue(self):
		determinate = self.cleaned_data.get('determinate')
		endValue = self.cleaned_data.get('endValue')
		if (determinate):
			if (endValue is None):
				raise forms.ValidationError('Please enter an end value.')
			else:
				return endValue
	
	def clean_private(self):
		"""
		Validate private
		"""
		private = self.cleaned_data['private']
		if private is None:
			return False
		else:
			return private
	
	def clean_complete_by(self):
		"""
		Raise Error if complete_by is less than the current date.
		"""
		complete_by = self.cleaned_data.get('complete_by')
		if (complete_by is None):
			return complete_by
		elif (datetime.now() > complete_by):
			raise forms.ValidationError('Time travel is not allowed.')
		else:
			return complete_by
	
	def clean_completed(self):
		"""
		Raise Error if date_completed has something when the goal is not yet completed and vice versa
		"""
		completed = self.cleaned_data.get('completed')
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
			if (datetime.now() < date_completed):
				raise forms.ValidationError('Time travel is not allowed.')
			else:
				return date_completed

class DeleteProgressGoalForm(forms.ModelForm):
	class Meta:
		model = ProgressGoal
		fields = []
		
class ProgressUpdateForm(forms.ModelForm):
	"""
	Form for Value Goal Updates
	"""
	value = forms.DecimalField(required=True, max_digits = 22, decimal_places=10)
	description = forms.CharField(required=False, max_length=70)
	
	class Meta:
		model = ProgressUpdate
		fields = ['value', 'description',]

class ProgressNoteForm(forms.ModelForm):
	note = forms.CharField(required=True, label='', widget=forms.Textarea(attrs={'placeholder': 'Note'}))
	class Meta:
		model = ProgressNote
		fields = ('note',)
		
class DeleteProgressNoteForm(forms.ModelForm):
	class Meta:
		model = ProgressNote
		fields = []

class ProgressJournalForm(forms.ModelForm):
	entry = forms.CharField(required=True, label='', widget=forms.Textarea(attrs={'placeholder': 'Journal Entry'}))
	title = forms.CharField(required=False, label='', widget=forms.Textarea(attrs={'placeholder': 'Entry Title'}), max_length=75)
	class Meta:
		model = ProgressJournal
		fields = ('entry','title',)
		
class DeleteProgressJournalForm(forms.ModelForm):
	class Meta:
		model = ProgressJournal
		fields = []

#UNIVERSAL FORMS
class CompletedButtonForm(forms.Form):
	"""
	Form for completing milestones
	"""
	date_completed = forms.DateTimeField(required=True, label='', widget=forms.TextInput(attrs={'placeholder': 'Date of Completion(MM/DD/YYYY)*'}))
		
class CollectMilestoneIDForm(forms.Form):
	"""
	Form for creating Sub-Milestones
	"""
	milestone_id = forms.CharField(required = False)
	editmilestone_id = forms.CharField(required = False)
	deletemilestone_id = forms.CharField(required = False)
	completedmilestone_id = forms.CharField(required = False)
	completedmilestone_isGoal = forms.BooleanField(required = False)

class CollectUpdateIDForm(forms.Form):
	"""
	form for collecting update id for value and progress goals
	"""
	editupdate_id = forms.CharField(required = False)

class MilestoneCollectNoteJournalID(forms.Form):
	milestone_id = forms.IntegerField(required = False)
	note_id = forms.IntegerField(required = False)
	journal_id = forms.IntegerField(required = False)
	milestone_note_id = forms.IntegerField(required = False)
	milestone_journal_id = forms.IntegerField(required = False)

class CollectNoteJournalID(forms.Form):
	note_id = forms.IntegerField(required = False)
	journal_id = forms.IntegerField(required = False)