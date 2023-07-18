from django.test import TestCase
from .models import *

# Create your tests here.
class IncidentReportTest(TestCase):

    fixtures = ["reports/fixtures/test_report.json"]

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


    def test_farm_doesnt_exist(self):        
        with self.assertRaises(FarmCopy.DoesNotExist):
            report = IncidentReport.get_reports_by_cph(
                county=1,
                parish="999",
                holding_number="99999"
            )
