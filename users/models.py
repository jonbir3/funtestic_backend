from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

MIN_LENGTH_OF_ID = 8
MAX_LENGTH_OF_ID = 9
LENGTH_OF_PHONE = 10


class Person(models.Model):
    phone_number = models.CharField(max_length=LENGTH_OF_PHONE,
                                    validators=[RegexValidator(regex='^[0-9]*$',
                                                               message='Numbers only',
                                                               code='num_only')],
                                    primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return '{0}'.format(str(self.user))
