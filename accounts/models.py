from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=30)
    email = models.EmailField(max_length=75, unique=True)
	
    def __unicode__(self):
        return self.username
	
	class Meta:
		ordering = ['username']