from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField()
    email = models.EmailField()
    first_name = models.CharField()
    last_name = models.CharField()
	
	def __unicode__(self):
		return self.username