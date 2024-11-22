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

        # Create an instance of SytadinData
        sytadin_data = SytadinData('http://example.com')
        sytadin_data.update()

        # Check the updated values
        self.assertEqual(sytadin_data.traffic_level, 'Level 1')
        self.assertEqual(sytadin_data.traffic_tendency, 'Tendency 1')
        self.assertEqual(sytadin_data.traffic_value, '1.23')

if __name__ == '__main__':
    unittest.main()
