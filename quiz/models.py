from django.db import models
from children.models import Child
from cryptography.utils import CbcEngine


class Quiz(models.Model):
    grade = models.CharField(max_length=6)
    child = models.ForeignKey(Child, on_delete=models.CASCADE)

    def __str__(self):
        try:
            child_name = CbcEngine.get_engine().decrypt(self.child.name)
            grade = CbcEngine.get_engine().decrypt(self.grade)
        except (TypeError, ValueError):
            child_name = self.child.name
            grade = self.grade
        return '{0}, {1}'.format(child_name, grade)

    def save(self, **kwargs):
        cbc_engine = CbcEngine.get_engine()
        self.grade = cbc_engine.encrypt(self.grade)
        super(Quiz, self).save(**kwargs)
