

from django.db import models
from django.contrib.auth.models import AbstractUser

'''
персональный идентификатор, 
никнейм, статус (активный, заблокирован), 
избранное;
'''

class RecipesUser(AbstractUser):
    
    user_id = models.CharField(
        verbose_name = 'персональный идентификатор',
        max_length = 50,
        default = -1,
        unique = True,
        blank=False)

    nickname = models.CharField(
        verbose_name = 'никнейм',
        max_length=50,
        unique = True,
        blank=False)

    not_delete = models.BooleanField(
        verbose_name = 'не удаляется',
        default=False)

    USERNAME_FIELD = 'nickname'

    class Meta():
        ordering = ['user_id','username']

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.is_active = True
        super().save(*args, **kwargs)
