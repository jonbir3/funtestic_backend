from django.db import models
from children.models import Child


class Quiz(models.Model):
    grade = models.DecimalField(max_digits=4, decimal_places=2)
    child = models.ForeignKey(Child, on_delete=models.CASCADE)

    def __str__(self):
        return '{0}, {1}'.format(self.child.name, self.grade)
