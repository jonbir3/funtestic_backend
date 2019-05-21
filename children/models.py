from django.db import models
from users.models import Person


class Child(models.Model):
    GENDER = (('M', 'Male'),
              ('F', 'Female'),
              ('O', 'Other'))
    age = models.CharField(max_length=2)
    gender = models.CharField(choices=GENDER, default='M', max_length=1)
    name = models.CharField(max_length=20)
    parent = models.ForeignKey(Person, on_delete=models.CASCADE)
