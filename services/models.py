from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils import timezone
from datetime import timedelta
from .utils import generate_secret_code

class PublicRecord(models.Model):
    record_type = models.CharField(max_length=100)
    description = models.TextField()
    date_created = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    id_image = models.ImageField(upload_to='media/id_images/', blank=True, null=True)

    def __str__(self):
        return f"{self.record_type} - {self.date_created}"

class MarriageLicense(models.Model):
    applicant1 = models.CharField(max_length=100)
    applicant2 = models.CharField(max_length=100)
    application_date = models.DateField(auto_now_add=True)
    issued_by = models.ForeignKey(User, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=100, unique=True)
    cert_pdf = models.FileField(upload_to='media/cert_pdfs/', blank=True, null=True)

    def __str__(self):
        return f"{self.license_number} - {self.applicant1} & {self.applicant2}"

class PropertyDeed(models.Model):
    owner = models.CharField(max_length=100)
    property_address = models.CharField(max_length=255)
    deed_number = models.CharField(max_length=100, unique=True)
    date_issued = models.DateField(auto_now_add=True)
    issued_by = models.ForeignKey(User, on_delete=models.CASCADE)
    deed_pdf = models.FileField(upload_to='media/deed_pdfs/', blank=True, null=True)

    def __str__(self):
        return f"{self.deed_number} - {self.property_address}"
    

class Vehicle(models.Model):
    owner_name = models.CharField(max_length=100)
    owner_id_number = models.CharField(max_length=20)
    number_plate = models.CharField(max_length=20, unique=True)
    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    insured = models.BooleanField(default=False)
    image1 = models.ImageField(upload_to='vehicle_images/')
    image2 = models.ImageField(upload_to='vehicle_images/', blank=True, null=True)
    image3 = models.ImageField(upload_to='vehicle_images/', blank=True, null=True)
    image4 = models.ImageField(upload_to='vehicle_images/', blank=True, null=True)
    image5 = models.ImageField(upload_to='vehicle_images/', blank=True, null=True)
    image6 = models.ImageField(upload_to='vehicle_images/', blank=True, null=True)

    def __str__(self):
        return f"{self.number_plate} - {self.model}"


class Person(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    id_number = models.CharField(max_length=8 , unique=True)
    full_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    social_security_number = models.CharField(max_length=10)
    last_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    place_of_birth = models.CharField(max_length=255)
    profile_picture = models.ImageField(upload_to='profile_pictures/')
    gender = models.CharField(max_length=10)  # Added gender field
    date_of_issue = models.DateField( null=True)  # Automatically sets the issue date
    expiry_date = models.DateField(null=True)  # Added expiry date field
    thumbprint = models.ImageField(upload_to='thumbprints/', null=True)  # Added thumbprint field
    nationality = models.CharField(max_length=50, default='Kenyan', blank=True)  # Added nationality field
    parent_or_guardian = models.CharField(max_length=255, blank=True, null=True) 

    def __str__(self):
        return self.full_name
    


class TaxPayment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    month = models.DateField()
    status = models.CharField(max_length=50, default='Pending')
    secret_code = models.CharField(max_length=10, unique=True, blank=True, null=True)
    code_expiration = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.secret_code:
            self.secret_code = generate_secret_code()
            self.code_expiration = timezone.now() + timedelta(days=30)  # Set code to expire in 30 days
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user} - {self.amount} - {self.month} - {self.status}'
    
    def is_code_expired(self):
        return timezone.now() > self.code_expiration
    


class Member(models.Model):
    identification_number = models.CharField(max_length=20, unique=True)
    username = models.CharField(max_length=30, unique=True)
    full_name = models.CharField(max_length=100)
    registration_fee_paid = models.BooleanField(default=False)
    phone = models.CharField(max_length=30)
    Email = models.EmailField(max_length=30)


    def __str__(self):
        return self.full_name
    
class Month(models.Model):
    name = models.CharField(max_length=20)  # E.g., 'January 2024'

    def __str__(self):
        return self.name

class MonthlyPayment(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='payments')
    month = models.ForeignKey(Month, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.member.full_name} - {self.month.name} - {self.amount}"