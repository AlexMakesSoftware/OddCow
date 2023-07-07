from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator, MaxLengthValidator

# The 'Copy' classes are our non-legacy copy of the records taken from the legacy databases. This is our copy of the
# data for which we can guarantee referrential integrity and we are free to update as we see fit. It will not write back
# to the legacy database, ever. We might want to update it from the legacy data if some genius decides to update that but
# that's tomorrow's problem.


class FarmCopy(models.Model):   
    county = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(50)])
    parish = models.CharField(max_length=3, validators=[MinLengthValidator(3), MaxLengthValidator(3)])
    holding_number = models.CharField(max_length=5, validators=[MinLengthValidator(5), MaxLengthValidator(5)])
    # Address fields
    address_line1 = models.CharField(max_length=100)
    address_line2 = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100)
    postcode = models.CharField(max_length=10)
    farm_name = models.CharField(max_length=100)
    owner = models.ForeignKey('OwnerCopy', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.farm_name} | {self.county}/{self.parish}/{self.holding_number}"
    
    class Meta:
        unique_together = ['county', 'parish', 'holding_number']


class OwnerCopy(models.Model):            
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.first_name} {self.last_name} | {self.phone}"


class IncidentReport(models.Model):
    STATUS_CHOICES = (
        ('S', 'Suspected'),
        ('C', 'Confirmed'),
        ('E', 'Ended'),
    )

    incident_number = models.CharField(max_length=8, validators=[MinLengthValidator(8), MaxLengthValidator(8)])
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    
    farm = models.ForeignKey(FarmCopy, on_delete=models.CASCADE, related_name='incidents')

    def __str__(self):
        return f"Incident #{self.incident_number} | {self.farm.farm_name}"
    
    @staticmethod
    def generate_unique_incident_number():
        last_incident = IncidentReport.objects.order_by('-incident_number').first()
        last_number = int(last_incident.incident_number) if last_incident else 10150102
        new_number = last_number + 1
        incident_number = str(new_number).zfill(8)
        return incident_number