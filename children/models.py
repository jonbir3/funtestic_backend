from django.db import models

from cryptography.utils import CbcEngine
from users.models import Person
from django.core.validators import RegexValidator

MAX_LENGTH_OF_ID = 9


# class ChildQuerySet(models.query.QuerySet):
#
#     def get(self, **kwargs):
#         child = super(ChildQuerySet, self).get(**kwargs)
#
#         cbc_engine = CbcEngine.get_engine()
#         child.id_number = cbc_engine.decrypt(child.id_number)
#         child.age = cbc_engine.decrypt(child.age)
#         child.gender = cbc_engine.decrypt(child.gender)
#         child.name = cbc_engine.decrypt(child.name)
#
#         return child
#
#     def filter(self, *args, **kwargs):
#         list_of_children = super(ChildQuerySet, self).filter(*args, **kwargs)
#         cbc_engine = CbcEngine.get_engine()
#         for child in list_of_children:
#             child.id_number = cbc_engine.decrypt(child.id_number)
#             child.age = cbc_engine.decrypt(child.age)
#             child.gender = cbc_engine.decrypt(child.gender)
#             child.name = cbc_engine.decrypt(child.name)
#
#         return list_of_children


# class ChildManager(models.Manager.from_queryset(ChildQuerySet)):
#     pass


class Child(models.Model):
    GENDER = (('male', 'Male'),
              ('female', 'Female'),
              ('other', 'Other'))

    # objects = ChildManager()

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
        try:
            name = CbcEngine.get_engine().decrypt(self.name)
        except (TypeError, ValueError):
            name = self.name
        return name

    def save(self, **kwargs):
        cbc_engine = CbcEngine.get_engine()
        self.id_number = cbc_engine.encrypt(self.id_number)
        self.age = cbc_engine.encrypt(self.age)
        self.gender = cbc_engine.encrypt(self.gender)
        self.name = cbc_engine.encrypt(self.name)
        super(Child, self).save(**kwargs)
