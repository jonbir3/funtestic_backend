from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from cryptography.utils import CbcEngine

MIN_LENGTH_OF_ID = 8
MAX_LENGTH_OF_ID = 9
LENGTH_OF_PHONE = 10


# class PersonQuerySet(models.query.QuerySet):
#
#     def get(self, **kwargs):
#         # for key, val in kwargs.items():
#         #     kwargs[key] = CbcEngine.get_engine().encrypt(val)
#         person = super(PersonQuerySet, self).get(**kwargs)
#
#         cbc_engine = CbcEngine.get_engine()
#         person.phone_number = cbc_engine.decrypt(person.phone_number)
#         user = person.user
#         user.username = cbc_engine.decrypt(user.username)
#         user.first_name = cbc_engine.decrypt(user.first_name)
#         user.last_name = cbc_engine.decrypt(user.last_name)
#         user.email = cbc_engine.decrypt(user.email)
#         person.user = user
#         return person

#     def create(self, **kwargs):
#         for key, val in kwargs.items():
#             if key == 'user':
#                 kwargs[key] = dict(val)
#                 for user_key, user_val in kwargs[key].items():
#                     if user_key is not 'password':
#                         kwargs[key][user_key] = CbcEngine.get_engine().encrypt(user_val)
#             else:
#                 kwargs[key] = CbcEngine.get_engine().encrypt(val)
#
#         user = User.objects.create(kwargs['user'])
#         kwargs['user'] = user
#
#         return super(PersonQuerySet, self).create(**kwargs)


# class PersonManager(models.Manager.from_queryset(PersonQuerySet)):
#     pass


class Person(models.Model):
    # objects = PersonManager()

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
        if self.user_id is None:
            self.user = user
        super(Person, self).save(**kwargs)
