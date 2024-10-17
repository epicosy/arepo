import unittest
from unittest.mock import patch
from io import StringIO
from arepo.main import main


class TestInitCommand(unittest.TestCase):
    @patch('sys.stdout', new_callable=StringIO)
    def test_init_command(self, mock_stdout):
        db_uri = "sqlite:///:memory:"
        args = ['--uri', db_uri, 'init']

        # Call the main function with arguments
        with patch('sys.argv', ['arepo'] + args):
            main()

        expected_output = (
            "Initializing the database.\n"
            "Populated 'abstractions' table.\n"
            "Populated 'tags' table.\n"
            "Populated 'operations' table.\n"
            "Populated 'phases' table.\n"
            "Populated 'bf_classes' table.\n"
            "Populated 'cwes' table.\n"
            "Populated 'cwe_operations' table.\n"
            "Populated 'cwe_phases' table.\n"
            "Populated 'cwe_bf_classes' table.\n"
            "Populated 'vendors' table.\n"
            "Populated 'grouping' table.\n"
        )

        self.assertEqual(mock_stdout.getvalue(), expected_output)


if __name__ == "__main__":
    unittest.main()
