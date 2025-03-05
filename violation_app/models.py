from django.db import models
from django.contrib.auth.models import User

class Violation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle_number = models.CharField(max_length=15)
    violation_type = models.CharField(max_length=100)
    fine_amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    image = models.ImageField(upload_to='violation_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.vehicle_number} - {self.violation_type}"

class Grievance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    violation = models.ForeignKey(Violation, related_name="grievances", on_delete=models.CASCADE)
    complaint_text = models.TextField()
    complaint_text = models.TextField()
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Resolved', 'Resolved')], default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Grievance by {self.user.username} - {self.violation}"

class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle_number = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.vehicle_number} - {self.user}"
    
class UploadedImage(models.Model):
    image = models.ImageField(upload_to="uploads/")
    # detected_image = models.ImageField(upload_to="uploads/", blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.image}"


