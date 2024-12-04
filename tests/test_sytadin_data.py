import unittest
from unittest.mock import patch, MagicMock
from commutator_sytadin.sytadin_data import SytadinData

class TestSytadinData(unittest.TestCase):

    @patch('commutator_sytadin.sytadin_data.requests.get')
    def test_update(self, mock_get):
        # Mock the response from requests.get
        mock_response = MagicMock()
        mock_response.text = '''
        <html>
            <div class="barometre_niveau"><img alt="Level 1" /></div>
            <div class="barometre_tendance"><img alt="Tendency 1" /></div>
            <div class="barometre_valeur">1.23</div>
        </html>
        '''
        mock_get.return_value = mock_response

        # Mock the properties_changed_callback
        properties_changed_callback = MagicMock()

        # Create an instance of SytadinData with the mock callback
        sytadin_data = SytadinData(properties_changed_callback, 'http://example.com', 300)
        sytadin_data.update()

        # Check the updated values
        self.assertEqual(sytadin_data.traffic_level, 'Level 1')
        self.assertEqual(sytadin_data.traffic_tendency, 'Tendency 1')
        self.assertEqual(sytadin_data.traffic_value, '1.23')

        # Check that the properties_changed_callback was called with the updated properties
        properties_changed_callback.assert_called_once_with({
            'traffic_level': 'Level 1',
            'traffic_tendency': 'Tendency 1',
            'traffic_value': '1.23'
        })

        sytadin_data.stop_auto_update()

if __name__ == '__main__':
    unittest.main()
