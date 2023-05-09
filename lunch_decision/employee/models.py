from django.db import models
from UserAuth.models import Profile

from menus.models import Menu


class Employee(Profile):
    company = models.CharField(max_length=255)
    department = models.CharField(max_length=255)

    def delete(self, *args, **kwargs):
        self.user.delete()
        super().delete(*args, **kwargs)


class Vote(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    points = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee} voted {self.points} points for {self.menu}"

    class Meta:
        unique_together = ('employee', 'menu')
