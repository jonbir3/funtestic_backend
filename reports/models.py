from django.db import models
from children.models import Child
from quiz.models import Quiz


class Report(models.Model):
    create_at = models.DateField(auto_now=True)
    child = models.OneToOneField(Child, on_delete=models.CASCADE)
    quizzes = models.ManyToManyField(Quiz)

    def __str__(self):
        return self.child.name
