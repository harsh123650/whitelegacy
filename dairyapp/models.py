from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone  # ✅ Required for default date

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20)
    custom_id = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f"{self.custom_id} - {self.user.username}"


class MilkDelivery(models.Model):
    customer_id = models.CharField(max_length=10)
    date = models.DateField()
    time = models.TimeField()
    submitted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


class MilkingLog(models.Model):
    buffalo_number = models.CharField(max_length=10, default='B001')  # ✅ Default value
    date = models.DateField(default=timezone.now)                      # ✅ Default value
    milk_time = models.TimeField()
    milk_quantity = models.FloatField()
    submitted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


class HealthLog(models.Model):
    buffalo_number = models.CharField(max_length=10, default='B001')  # ✅ Default value
    date = models.DateField(default=timezone.now)                     # ✅ Default value
    health_notes = models.TextField()
    submitted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
