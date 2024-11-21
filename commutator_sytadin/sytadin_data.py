import logging
import requests
import re
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)
_LOGGER = logging.getLogger(__name__)

URL = "http://www.sytadin.fr/sys/barometres_de_la_circulation.jsp.html"

REGEX = r'(\d*\.\d+|\d+)'

class SytadinData:
    """The class for handling the data retrieval."""

    def __init__(self, resource):
        """Initialize the data object."""
        self._resource = resource
        self.data = None
        self.traffic_level = None
        self.traffic_tendency = None
        self.traffic_value = None

    def update(self):
        """Get the latest data from the Sytadin."""
        translation_dict = {
            'Faible': 'Low',
            'Habituel': 'Normal',
            'Inhabituel': 'Unusual',
            'Exceptionnel': 'Exceptional',
            'En Hausse': 'Increasing',
            'En Baisse': 'Decreasing',
            'Stable': 'Stable'
        }

        try:
            raw_html = requests.get(self._resource, timeout=10).text
            data = BeautifulSoup(raw_html, "html.parser")

            values = data.select(".barometre_niveau")
            traffic_level_fr = values[0].select("img")[0].get('alt')
            self.traffic_level = translation_dict.get(traffic_level_fr, traffic_level_fr)

            values = data.select(".barometre_tendance")
            traffic_tendency_fr = values[0].select("img")[0].get('alt')
            self.traffic_tendency = translation_dict.get(traffic_tendency_fr, traffic_tendency_fr)

            values = data.select(".barometre_valeur")
            parse_traffic_value = re.search(REGEX, values[0].text)
            if parse_traffic_value:
                self.traffic_value = parse_traffic_value.group()

        except requests.exceptions.ConnectionError:
            _LOGGER.error("Connection error")
            self.data = None
