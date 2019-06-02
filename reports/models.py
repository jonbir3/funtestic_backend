from django.db import models
from children.models import Child
from cryptography.utils import CbcEngine
from quiz.models import Quiz


class Report(models.Model):
    create_at = models.DateField(auto_now=True)
    child = models.OneToOneField(Child, on_delete=models.CASCADE)
    quizzes = models.ManyToManyField(Quiz)

    def __str__(self):
        return self.child.name

    def save(self, **kwargs):
        cbc_engine = CbcEngine.get_engine()
        self.create_at = cbc_engine.encrypt(str(self.create_at))
        super(Report, self).save(**kwargs)
