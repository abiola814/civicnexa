from django.db import models
# from . validators import validate_image_size
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
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
    
    GENDER = [('Female', 'Female'),
             ('Male', 'Male'),
            ]
    
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(upload_to=None, max_length=None, null=True, blank=True, validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg'])])
    first_name = models.CharField(max_length=50)
    # email = models.CharField(max_length=50)
    gender = models.CharField(max_length=6, default='Female')
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    dob = models.CharField(max_length=50)
    state_of_origin = models.CharField(max_length=100)
    # state_of_resident = models.CharField(max_length=100)
    address = models.CharField(max_length=100, null=True)
    nin = models.CharField(max_length=11, null=True)
    phone = models.CharField(max_length=50)
    occupation = models.CharField(max_length=100, null=True)
    image = models.ImageField(blank=True,null=True,upload_to="photos")
    face_id = models.CharField(max_length=150)
    marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS, null=True)
    health_code = models.CharField(max_length=20, editable=False, null=True)
    bloodgroup = models.CharField(max_length=3, choices=BLOOD_GROUP, null=True)
    genotype = models.CharField(max_length=3, choices=GENOTYPE, null=True)
    role = models.ForeignKey("Role", default=1, on_delete=models.CASCADE, null=True)



    def save(self, *args, **kwargs):
        if not self.health_code:
         
            self.health_code = (
                f"{self.state_of_origin[:2]}{self.first_name[:2]}{self.last_name[:2]}{self.phone[-5:]}"
            ).upper()

        super(Profile, self).save(*args, **kwargs)


    def __str__(self) -> str:
        return f'{self.first_name} - {self.last_name}'
    

class Role(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self) -> str:
        return str(self.title)



class NextOfKin(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='nextofkin')
    name = models.CharField(max_length=50)
    relationship = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    address = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name



class Relatives(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=50, null=True, blank=True)
    occupation = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name

