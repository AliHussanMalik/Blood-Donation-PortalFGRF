# donors/models.py
from django.db import models
from django.conf import settings

class DonorProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    blood_group = models.CharField(max_length=5)
    age = models.PositiveIntegerField()
    city = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.user.email} - {self.blood_group}"

# hospitals/models.py
class HospitalProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    hospital_name = models.CharField(max_length=200)
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    available_blood_types = models.TextField(help_text="Comma separated blood types")

    def __str__(self):
        return self.hospital_name

# requests/models.py
class BloodRequest(models.Model):
    BLOOD_GROUPS = [
        ("A+", "A+"), ("A-", "A-"),
        ("B+", "B+"), ("B-", "B-"),
        ("O+", "O+"), ("O-", "O-"),
        ("AB+", "AB+"), ("AB-", "AB-"),
    ]

    hospital = models.ForeignKey(HospitalProfile, on_delete=models.CASCADE)
    patient_name = models.CharField(max_length=100)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUPS)
    urgency_level = models.CharField(max_length=50, choices=[("Low","Low"),("Medium","Medium"),("High","High")])
    status = models.CharField(max_length=20, default="Pending")  # Pending, Approved, Assigned, Completed
    created_at = models.DateTimeField(auto_now_add=True)

    # Admin will later assign a donor
    assigned_donor = models.ForeignKey(DonorProfile, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Request {self.id} - {self.blood_group} ({self.status})"
