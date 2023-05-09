from django.db import models
from UserAuth.models import Profile


class RestaurantOwner(Profile):

    def delete(self, *args, **kwargs):
        self.user.delete()
        super().delete(*args, **kwargs)


class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(RestaurantOwner, on_delete=models.CASCADE, related_name='restaurants')

    def __str__(self):
        return "{} - {}".format(self.name, self.owner.user)

