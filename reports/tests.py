from django.test import TestCase
from .models import *
from farms.models import Farm, Owner
from django.db import transaction
# Create your tests here.
class IncidentReportTest(TestCase):

    fixtures = ["reports/fixtures/fixture_report.json"]

    def test_find_report_by_cph(self):        
        report = IncidentReport.get_reports_by_cph(
            county=2,
            parish="001",
            holding_number="00042"
        )
        #check we got some data.
        self.assertTrue(report)
        #there should be three reports
        self.assertEqual(3, len(report))


    def test_farm_has_no_reports(self):        
        report = IncidentReport.get_reports_by_cph(
            county=2,
            parish="001",
            holding_number="00049"
        )
        # no reports for this farm but the farm does exist, so no exceptions thrown.
        self.assertFalse(report)


    @classmethod
    def mock_legacy_farm_data(cls):
        owner = Owner(
            first_name= "Tina",
            last_name= "Jennings",
            email  = "georginabuckley@example.com",
            phone = "+44(0)1632960993")        
        farm = Farm(
            county=1,
            parish="001",
            holding_number="00001",
            owner = owner,
            address_line1= "1 Stevenson circle",
            address_line2 = "",
            city =  "West Melissaview",
            postcode =  "B1 9QL",
            farm_name =  "Archer Inc"
        )
        return farm


    def test_legacy_find_or_create(self):
        """
        When a report is made, the legacy data should first be coppied to the new database
        but this should only happen once.
        Although we have two seperate databases in the live version,
        This is combined into one, for testing, pulling in legacy data from another app into
        the default database seemed to cause issues, so I'm just creating the mock legacy objects
        manually in mock_legacy_farm_data() instead.
        """        
        #Check there's no farm in the database with this id:
        with self.assertRaises(FarmCopy.DoesNotExist):
            farm = FarmCopy.objects.get(
                    county=1,
                    parish="001",
                    holding_number="00001"
            )

        #the 'real one' from the legacy database.
        farm = IncidentReportTest.mock_legacy_farm_data()      
        
        # Create a report, referencing the legacy farm with the same details.
        with transaction.atomic():
            farm_copy = FarmCopy.find_or_copy_from(farm)
            if not farm_copy:
                raise LookupError("farm copy is null!")
            incident = IncidentReport.objects.create(
                farm=farm_copy,
                start_date = "2022-07-08",
                end_date = "2022-12-12",
                status = "E"
            )       
        
        # Now check we can find the farm.
        fc = FarmCopy.objects.get(
                    county=1,
                    parish="001",
                    holding_number="00001")

        #repeat the process (done when another report is filed for the same location)
        with transaction.atomic():
            farm_copy = FarmCopy.find_or_copy_from(farm)

        #Now confirm that there is still only one FarmCopy.
        #TODO: ideally the database would enforce this but I guess that's a little hard to do if it's a 3-field unique key
        list_farms = FarmCopy.objects.filter(
                    county=1,
                    parish="001",
                    holding_number="00001")
        self.assertEqual(1, len(list_farms))

