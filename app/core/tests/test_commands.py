"""
Test custom Django management commands.
"""
from unittest.mock import patch

from psycopg2 import OperationalError as Psycopg2Error

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


# el comando check lo provee BaseCommand, permite chequear el estado de la db
@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test commands."""

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database if database ready"""
        patched_check.return_value = True  # mock the return value to be True

        call_command('wait_for_db')  # calls the command

        patched_check.assert_called_once_with(databases=['default'])

    # replace the sleep function with magic mock so it doesnt pause
    # the unittest as it does in the real case
    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for database when getting OperationalError"""
        # Mock exceptions using side_effect:
        # here I simulate  Psycopg2Error (first 2 times the Command.check runs)
        # and Django OperationalError the next 3 times
        # finally, the sixth time it runs, it returns True
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])
