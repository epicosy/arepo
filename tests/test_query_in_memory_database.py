import unittest
from arepo.db import get_in_memory_database, DatabaseConnection
from arepo.models.common.tag import TagModel


class TestInMemoryDatabaseQuery(unittest.TestCase):
    def test_query_in_memory_database(self):
        # Initialize the in-memory database and get the engine
        engine = get_in_memory_database()

        # Create the database connection
        db = DatabaseConnection("", engine)

        # Create a session
        session = db.get_session()

        # Query the TagModel table
        entries = session.query(TagModel).all()

        # Close the session
        session.close()

        # Define the expected output
        expected_output = [
            (1, 'Third Party Advisory'),
            (2, 'Mailing List'),
            (3, 'Permissions Required'),
            (4, 'Tool Signature'),
            (5, 'VDB Entry'),
            (6, 'Release Notes'),
            (7, 'Patch'),
            (8, 'Technical Description'),
            (9, 'Press/Media Coverage'),
            (10, 'Exploit'),
            (11, 'US Government Resource'),
            (12, 'Broken Link'),
            (13, 'Not Applicable'),
            (14, 'Product'),
            (15, 'URL Repurposed'),
            (16, 'Vendor Advisory'),
            (17, 'Mitigation'),
            (18, 'Issue Tracking'),
            (19, 'Other')
        ]

        # Convert the entries to a list of tuples for comparison
        actual_output = [(entry.id, entry.name) for entry in entries]

        # Check if the actual output matches the expected output
        self.assertEqual(actual_output, expected_output)


if __name__ == "__main__":
    unittest.main()
