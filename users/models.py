from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from cryptography.utils import CbcEngine

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

    # other fields from User: first_name, last_name, email, password

    def __str__(self):
        try:
            first_name = CbcEngine.get_engine().decrypt(self.user.first_name)
            last_name = CbcEngine.get_engine().decrypt(self.user.last_name)
        except (TypeError, ValueError):
            first_name = self.user.first_name
            last_name = self.user.last_name
        return '{0} {1}'.format(str(first_name), str(last_name))

    def save(self, **kwargs):
        cbc_engine = CbcEngine.get_engine()

        user = self.user
        user.first_name = cbc_engine.encrypt(user.first_name)
        user.last_name = cbc_engine.encrypt(user.last_name)
        user.email = cbc_engine.encrypt(user.email)
        user.username = cbc_engine.encrypt(user.username)
        user.save()
        self.phone_number = cbc_engine.encrypt(self.phone_number)
        super(Person, self).save(**kwargs)
