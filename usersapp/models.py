from django.db import models
from django.contrib.auth.models import AbstractUser

'''
персональный идентификатор, 
никнейм, статус (активный, заблокирован), 
избранное;
'''

class RecipesUser(AbstractUser):
	
	user_id = models.IntegerField(
		verbose_name = 'персональный идентификатор',
		default = -1,
		blank=False)

	nickname = models.CharField(
		verbose_name = 'никнейм',
		max_length=50,
		blank=False)

	not_delete = models.BooleanField(
		verbose_name = 'не удаляется',
		default=False)

	class Meta():
		ordering = ['is_superuser','username']

	def save(self, *args, **kwargs):
		if self.is_superuser:
			self.is_active = True
		super().save(*args, **kwargs)