from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string
from faker import Faker
from farms.models import Owner, Farm

class Command(BaseCommand):
    help = 'Create random farms and owners'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='Indicates the number of farms to be created (with an owner each).')
        parser.add_argument('parish', type=int, help='Indicates the number of farms to be placed per parish.')


    def _cph(total, farms_per_parishes):
        county = 1
        parish = 1
        holding = 1    
            
        farms_per_parish =  total // farms_per_parishes
        farms_in_parish = 0

        for count in range(total):
            yield county, parish, holding        
            
            holding+=1
            farms_in_parish+=1
            if farms_in_parish>farms_per_parishes:
                parish=1
                county+=1
                holding=1
                farms_in_parish=0


    def handle(self, *args, **kwargs):
        fake = Faker('en-gb')
        
        count = kwargs['count']
        per_parish = kwargs['parish']

        county_count = 50
        parish_count = 999
        holdings_per_parish = 200

        for county, parish, holding_number in Command._cph(count, per_parish):

            # Generate random values                        
            owner_name = fake.name()
            email = fake.email()
            phone = fake.phone_number()
            address = fake.street_address().splitlines()
            address1 = address[0]
            address2 = address[1] if len(address) > 1 else ""

            # Create the Owner instance
            owner = Owner.objects.create(
                first_name=owner_name.split()[0],
                last_name=owner_name.split()[1],
                email=email,
                phone=phone
            )

            # Create the Farm instance
            farm = Farm.objects.create(
                county=county,
                parish=str(parish).zfill(3),
                holding_number=str(holding_number).zfill(5),
                address_line1=address1,
                address_line2= address2,
                city=fake.city(),
                postcode=fake.postcode(),                
                farm_name=fake.company(),                
                owner=owner
            )

            # Output the created farm and owner details
            self.stdout.write(f"Created Farm: {farm}")
            self.stdout.write(f"Owner: {owner}")

        self.stdout.write(self.style.SUCCESS(f"Successfully generated {count} farms and owners."))