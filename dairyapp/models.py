from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone  



# User Profile Model

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20)
    custom_id = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f"{self.custom_id} - {self.user.username}"


# Milk Delivery Logs

class MilkDelivery(models.Model):
    customer_id = models.CharField(max_length=10)
    date = models.DateField()
    time = models.TimeField()
    submitted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Delivery to {self.customer_id} on {self.date} at {self.time}"



# Milking Logs
class MilkingLog(models.Model):
    buffalo_number = models.CharField(max_length=10, default='B001')
    date = models.DateField(default=timezone.now)
    milk_time = models.TimeField()
    milk_quantity = models.FloatField()
    submitted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.buffalo_number} – {self.milk_quantity}L @ {self.milk_time}"

# Health Logs
class HealthLog(models.Model):
    buffalo_number = models.CharField(max_length=10, default='B001')
    date = models.DateField(default=timezone.now)
    health_notes = models.TextField()
    submitted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.buffalo_number} – {self.date}"

# Contact Us Messages

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=150)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} – {self.subject}"

#Subscription Request (public form)

class SubscriptionRequest(models.Model):
    name = models.CharField(max_length=100, default="Harshal Patil")
    email = models.EmailField(default="example@example.com")
    mobile = models.CharField(max_length=15, default="9999999999")
    address = models.TextField(default="Enter Full Address")
    litre_needed = models.IntegerField(default=1)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request: {self.name} – {self.litre_needed}L"


#Active Subscription
class Subscription(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)  # हे असलेच पाहिजे

    def __str__(self):
        return f"{self.customer.username} - {self.plan}"

#Payment Logs
class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.CharField(max_length=20, choices=[
        ('Monthly', 'Monthly'),
        ('Quarterly', 'Quarterly'),
        ('Yearly', 'Yearly'),
    ])
    amount = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} – {self.plan} – ₹{self.amount}"
