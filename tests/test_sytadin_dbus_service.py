import unittest
from unittest.mock import patch, MagicMock
from commutator_sytadin.sytadin_dbus_service import SytadinDBusService

class TestSytadinDBusService(unittest.TestCase):

    @patch('commutator_sytadin.sytadin_dbus_service.SytadinData')
    def test_properties_changed(self, mock_sytadin_data):
        # Mock the SytadinData instance
        mock_instance = MagicMock()
        mock_instance.traffic_level = 'Level 1'
        mock_instance.traffic_tendency = 'Tendency 1'
        mock_instance.traffic_value = '1.23'
        mock_sytadin_data.return_value = mock_instance

        # Create an instance of SytadinDBusService
        bus_name = MagicMock()
        update_interval = 300
        sytadin_service = SytadinDBusService(bus_name, update_interval)

        # Mock the PropertiesChanged signal
        properties_changed_signal = MagicMock()
        sytadin_service.PropertiesChanged = properties_changed_signal

        # Simulate the properties_changed method being called
        sytadin_service.properties_changed({
            'traffic_level': 'Level 1',
            'traffic_tendency': 'Tendency 1',
            'traffic_value': '1.23'
        })

        # Check if the PropertiesChanged signal was emitted
        properties_changed_signal.assert_called_once_with(
            'com.commutator.Sytadin',
            {
                'traffic_level': 'Level 1',
                'traffic_tendency': 'Tendency 1',
                'traffic_value': '1.23'
            },
            []
        )

    @patch('commutator_sytadin.sytadin_dbus_service.SytadinData')
    def test_get_method(self, mock_sytadin_data):
        # Mock the SytadinData instance
        mock_instance = MagicMock()
        mock_instance.traffic_level = 'Level 1'
        mock_instance.traffic_tendency = 'Tendency 1'
        mock_instance.traffic_value = '1.23'
        mock_sytadin_data.return_value = mock_instance

        # Create an instance of SytadinDBusService
        bus_name = MagicMock()
        update_interval = 300
        sytadin_service = SytadinDBusService(bus_name, update_interval)

        # Test the Get method
        self.assertEqual(sytadin_service.Get('com.commutator.Sytadin', 'traffic_level'), 'Level 1')
        self.assertEqual(sytadin_service.Get('com.commutator.Sytadin', 'traffic_tendency'), 'Tendency 1')
        self.assertEqual(sytadin_service.Get('com.commutator.Sytadin', 'traffic_value'), '1.23')

    @patch('commutator_sytadin.sytadin_dbus_service.SytadinData')
    def test_get_all_method(self, mock_sytadin_data):
        # Mock the SytadinData instance
        mock_instance = MagicMock()
        mock_instance.traffic_level = 'Level 1'
        mock_instance.traffic_tendency = 'Tendency 1'
        mock_instance.traffic_value = '1.23'
        mock_sytadin_data.return_value = mock_instance

        # Create an instance of SytadinDBusService
        bus_name = MagicMock()
        update_interval = 300
        sytadin_service = SytadinDBusService(bus_name, update_interval)

        # Test the GetAll method
        properties = sytadin_service.GetAll('com.commutator.Sytadin')
        self.assertEqual(properties, {
            'traffic_level': 'Level 1',
            'traffic_tendency': 'Tendency 1',
            'traffic_value': '1.23'
        })

if __name__ == '__main__':
    unittest.main()
