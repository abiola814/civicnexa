from django.db import models
# from . validators import validate_image_size
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    MARITAL_STATUS = [('Single', 'Single'),
                      ('Married', 'Married'),
                      ('Divorced', 'Divorced'),
                      ('Widowed', 'Widowed')
                      ]
    
    BLOOD_GROUP = [('O+', 'O positive'),
                      ('O-', 'O negative'),
                      ('A-', 'A negative'),
                      ('A+', 'A positive'),
                      ('B-', 'B negative'),
                      ('B+', 'B positive'),
                      ('AB-', 'AB negative'),
                      ('AB+', 'AB positive'),
                      ]
    
    GENOTYPE = [('AA', 'AA'),
                ('AS', 'AS'),
                ('SS', 'SS'),
                ('SC', 'SC'),
                ('AC', 'AC'),
            ]
    
    GENDER = [
        ('Male', 'Male'),
        ('Female', 'Feale'),
    ]
    
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(upload_to=None, max_length=None, null=True, blank=True, validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg'])])
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    dob = models.CharField(max_length=50)
    gender = models.CharField(max_length=50, choices=GENDER, null=True, blank=True)
    state_of_origin = models.CharField(max_length=100)
    state_of_resident = models.CharField(max_length=100)
    address = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=50)
    occupation = models.CharField(max_length=100, null=True)
    marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS, null=True)
    state_code = models.CharField(max_length=20, editable=False, null=True)
    bloodgroup = models.CharField(max_length=3, choices=BLOOD_GROUP, null=True)
    genotype = models.CharField(max_length=3, choices=GENOTYPE, null=True)
    role = models.ForeignKey("Role", default=1, on_delete=models.CASCADE, null=True)


    def __str__(self) -> str:
        return f'{self.first_name} - {self.last_name}'
    

class Role(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self) -> str:
        return str(self.title)

class Bank(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='bank')
    bank_name = models.CharField(max_length=50)
    BVN = models.CharField(max_length=100)
    account_number = models.CharField(max_length=50)
    account_name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.account_name

class NextOfKin(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='nextofkin')
    name = models.CharField(max_length=50)
    relationship = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    address = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name
    
# class Transaction(models.Model):
#     STATUSES = [
#         ('completed', 'paid'),
#         ('failed', 'failed'),
#         ('pending', 'pending')
#     ]

#     owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='transactions')
#     trxid = models.CharField(max_length=20)
#     created = models.DateTimeField(auto_now_add=True)
#     tx_type = models.CharField(max_length=50)
#     status = models.CharField(max_length=20, choices=STATUSES, default='pending')

#     class Meta:
#         ordering = ['-created']

#     def __str__(self):
#         return str(self.owner)


class Children(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=50)
    occupation = models.CharField(max_length=100)
    phone = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name

class Spouse(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    # gender = models.CharField(max_length=50)
    occupation = models.CharField(max_length=100)
    phone = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name


class Parent(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    # gender = models.CharField(max_length=50)
    occupation = models.CharField(max_length=100)
    phone = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name
    
    