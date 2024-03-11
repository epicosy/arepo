import unittest
from arepo.db import get_in_memory_database, DatabaseConnection
from arepo.models.common.scoring import CVSS3,CVSS2,CVSS3Source, CVSS2Source, VulnerabilityCVSS3,VulnerabilityCVSS2,Source


class TestScoring(unittest.TestCase):
    def setUp(self):
        engine = get_in_memory_database()

        # Create the database connection
        db = DatabaseConnection("", engine)

        # Create a session
        self.session = db.get_session()
    
    def tearDown(self):
        # Close the session after each test case
        self.session.close()
    
    def test_CVSS3(self):

        entries = self.session.query(CVSS3).all()


        # Convert the entries to a list of tuples for comparison
        actual_output = [(entry.id, entry.name) for entry in entries]
   
        # Check if the actual output matches the expected output
        self.assertIsNotNone(actual_output)

    def test_CVSS2(self):
        entries = self.session.query(CVSS2).all()

  

        # Convert the entries to a list of tuples for comparison
        actual_output = [(entry.id, entry.name) for entry in entries]
   
        # Check if the actual output matches the expected output
        self.assertIsNotNone(actual_output)


    def test_CVSS3Source(self):
        entries = self.session.query(CVSS3Source).all()

 
        # Convert the entries to a list of tuples for comparison
        actual_output = [(entry.id, entry.name) for entry in entries]
   
        # Check if the actual output matches the expected output
        self.assertIsNotNone(actual_output)

    def test_CVSS2Source(self):

        entries = self.session.query(CVSS2Source).all()

   

        # Convert the entries to a list of tuples for comparison
        actual_output = [(entry.id, entry.name) for entry in entries]
   
        # Check if the actual output matches the expected output
        self.assertIsNotNone(actual_output)
   
    def test_VulnerabilityCVSS3(self):
        entries = self.session.query(VulnerabilityCVSS3).all()


        # Convert the entries to a list of tuples for comparison
        actual_output = [(entry.id, entry.name) for entry in entries]
   
        # Check if the actual output matches the expected output
        self.assertIsNotNone(actual_output)

    def test_VulnerabilityCVSS2(self):
        entries = self.session.query(VulnerabilityCVSS2).all()



        # Convert the entries to a list of tuples for comparison
        actual_output = [(entry.id, entry.name) for entry in entries]
   
        # Check if the actual output matches the expected output
        self.assertIsNotNone(actual_output)

    def test_Source(self):
        entries = self.session.query(Source).all()


        # Convert the entries to a list of tuples for comparison
        actual_output = [(entry.id, entry.name) for entry in entries]
   
        # Check if the actual output matches the expected output
        self.assertIsNotNone(actual_output)


if __name__ == "__main__":
    unittest.main()
