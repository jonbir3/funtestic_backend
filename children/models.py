from django.db import models
from users.models import Person
from django.core.validators import RegexValidator

MAX_LENGTH_OF_ID = 9


class Child(models.Model):
    GENDER = (('M', 'Male'),
              ('F', 'Female'),
              ('O', 'Other'))
    id_number = models.CharField(max_length=MAX_LENGTH_OF_ID,
                                 validators=[RegexValidator(regex='^[0-9]*$',
                                                            message='Numbers only',
                                                            code='num_only')],
                                 primary_key=True)
    age = models.CharField(max_length=2)
    gender = models.CharField(choices=GENDER, default='M', max_length=1)
    name = models.CharField(max_length=20)
    parent = models.ForeignKey(Person, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
