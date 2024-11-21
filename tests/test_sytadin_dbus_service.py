import unittest
from unittest.mock import patch, MagicMock
from commutator_sytadin.sytadin_dbus_service import SytadinDBusService

class TestSytadinDBusService(unittest.TestCase):

    @patch('commutator_sytadin.sytadin_dbus_service.SytadinData')
    def test_update(self, mock_sytadin_data):
        # Mock the SytadinData instance
        mock_instance = MagicMock()
        mock_instance.traffic_level = 'Level 1'
        mock_instance.traffic_tendency = 'Tendency 1'
        mock_instance.traffic_value = '1.23'
        mock_sytadin_data.return_value = mock_instance

        # Create an instance of SytadinDBusService
        bus_name = MagicMock()
        sytadin_service = SytadinDBusService(bus_name)

        # Call the update method
        sytadin_service.update()

        # Check if the update method of SytadinData was called
        mock_instance.update.assert_called_once()

if __name__ == '__main__':
    unittest.main()
