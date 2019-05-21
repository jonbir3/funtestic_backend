from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

MIN_LENGTH_OF_ID = 8
MAX_LENGTH_OF_ID = 9


class Person(models.Model):
    id_number = models.CharField(max_length=MAX_LENGTH_OF_ID,
                                 validators=[RegexValidator(regex='^[0-9]*$', message='Numbers only', code='num_only')])
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.name
