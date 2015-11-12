import unittest
from autoconstruccion.models import Project


class TestProjectModel(unittest.TestCase):
    
    def test_should_have_name_field(self):
        assert Project.name
        
    def test_should_have_description_field(self):
        assert Project.description
    
    def test_should_have_start_date_field(self):
        assert Project.start_date

    def test_should_have_end_date_field(self):
        assert Project.end_date

    def test_should_have_image_field(self):
        assert Project.image

    def test_should_have_location_field(self):
        assert Project.location
        
    def test_should_have_contact_phone_field(self):
        assert Project.contact_phone
    
    def test_should_have_a_manager_field(self):
        assert Project.manager
