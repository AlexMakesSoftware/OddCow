from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator, MaxLengthValidator
from django.contrib import admin

# These records are in the legacy database, where the primary keys can change at any moment (no really).
# Whilst that is true, the CPH reference won't change and the owner(s) can be gauranteed to point to the right
# farm, it's just that their ids might have changed.


class Farm(models.Model):        
    class Meta:        
        unique_together = ['county', 'parish', 'holding_number']
    my_meta_db_using = 'legacy'

    county = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(50)])
    parish = models.CharField(max_length=3, validators=[MinLengthValidator(3), MaxLengthValidator(3)])
    holding_number = models.CharField(max_length=5, validators=[MinLengthValidator(5), MaxLengthValidator(5)])
    # Address fields
    address_line1 = models.CharField(max_length=100)
    address_line2 = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100)
    postcode = models.CharField(max_length=10)
    farm_name = models.CharField(max_length=100)
    owner = models.ForeignKey('Owner', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.farm_name} | {self.county}/{self.parish}/{self.holding_number}"
    
    def cph_to_str(self):
        return f"{self.county}/{self.parish}/{self.holding_number}"

class Owner(models.Model):
    my_meta_db_using = 'legacy'
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.first_name} {self.last_name} | {self.phone}"
