from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator, MaxLengthValidator
from django.db.models import Max
from django.db import IntegrityError
from django.contrib.auth.models import User

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
    
    def cph_to_str(self):
        return f"{self.county}/{self.parish}/{self.holding_number}"

    # honestly not sure if this is useful, or works or does anything...? TODO: test
    class Meta:
        unique_together = ['county', 'parish', 'holding_number']
    
    
    @classmethod
    def find_or_copy_from(cls, farm):
        """
        If we already have a copy of this farm in the database, then return it,
        otherwise create a record from the parameters passed in.
        Make sure you call this from a transaction!
        """
        farm_copy = FarmCopy.objects.filter(
            county = farm.county,
            parish = farm.parish,
            holding_number = farm.holding_number
        )
        if len(farm_copy) > 1:
            raise IntegrityError("Integrity constraint violation, more than one copy of the same farm found. "+farm_copy)
        
        if not farm_copy.exists():
            owner_copy = OwnerCopy.objects.create(
                first_name = farm.owner.first_name,
                last_name = farm.owner.last_name,
                email = farm.owner.email,
                phone = farm.owner.phone
            )            
            farm_copy = FarmCopy.objects.create(
                county = farm.county,
                parish = farm.parish,
                holding_number = farm.holding_number,
                address_line1 = farm.address_line1,
                address_line2 = farm.address_line2,
                city = farm.city,
                postcode = farm.postcode,
                farm_name = farm.farm_name,
                owner = owner_copy
            )
            return farm_copy
        else:
            return farm_copy.first()


class OwnerCopy(models.Model):            
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.first_name} {self.last_name} | {self.phone}"



def get_admin_user_id():
    return User.objects.get(username='admin').id


class IncidentReport(models.Model):
    STATUS_CHOICES = (
        ('S', 'Suspected'),
        ('C', 'Confirmed'),
        ('E', 'Ended'),
    )

    incident_number = models.CharField(max_length=8, validators=[MinLengthValidator(8), MaxLengthValidator(8)], unique=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)    
    farm = models.ForeignKey(FarmCopy, on_delete=models.CASCADE, related_name='incidents')

    created_by = models.ForeignKey(User, on_delete = models.SET_NULL, null=True, blank=True, related_name='created_reports')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=get_admin_user_id, related_name='assigned_reports')

    def __str__(self):
        return f"Incident #{self.incident_number} | {self.farm.farm_name}"


    def save(self, *args, **kwargs):        
        if not self.incident_number:
            max_incident_number = IncidentReport.objects.aggregate(Max('incident_number'))['incident_number__max']
            if max_incident_number:
                next_number = int(max_incident_number) + 1
            else:
                next_number = 1
            self.incident_number = str(next_number).zfill(8)
        super().save(*args, **kwargs)


    @classmethod
    def get_reports_by_cph(cls, county, parish, holding_number):     
        
        try:
            farm = FarmCopy.objects.get(county = county,
                        parish=parish,
                        holding_number=holding_number)        
        except FarmCopy.DoesNotExist:
            #If this happens it just means we haven't coppied the legacy db farm record to create a report, that's fine.
            return None
        
        return cls.objects.filter(farm=farm)


class Observation(models.Model):
    incident = models.ForeignKey(IncidentReport, on_delete=models.CASCADE)
    recorded_on = models.DateField(auto_now_add=True)
    note = models.TextField()
    user = models.ForeignKey(User, on_delete = models.SET_NULL, null=True, blank=True)
