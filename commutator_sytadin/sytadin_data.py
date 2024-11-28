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
        self.traffic_level = ''
        self.traffic_tendency = ''
        self.traffic_value = ''

    def update(self):
        """Get the latest data from the Sytadin."""
        translation_dict = {
            'Faible': 'Low',
            'Habituel': 'Normal',
            'Inhabituel': 'Unusual',
            'Exceptionnel': 'Exceptional',
            'En hausse': 'Increasing',
            'En baisse': 'Decreasing',
            'Stable': 'Stable'
        }

        try:
            raw_html = requests.get(self._resource, timeout=10).text
            data = BeautifulSoup(raw_html, "html.parser")

        except Exception as e:
            _LOGGER.error("Connection error: {}".format(e))
            self.data = None
            return

        values = data.select(".barometre_niveau")
        traffic_level_fr = values[0].select("img")[0].get('alt')
        self.traffic_level = translation_dict.get(traffic_level_fr, traffic_level_fr)
        _LOGGER.info("traffic_level = {}".format(self.traffic_level))

        values = data.select(".barometre_tendance")
        traffic_tendency_fr = values[0].select("img")[0].get('alt')
        self.traffic_tendency = translation_dict.get(traffic_tendency_fr, traffic_tendency_fr)
        _LOGGER.info("traffic_tendency = {}".format(self.traffic_tendency))

        values = data.select(".barometre_valeur")
        parse_traffic_value = re.search(REGEX, values[0].text)
        if parse_traffic_value:
            self.traffic_value = parse_traffic_value.group()
            _LOGGER.info("traffic_value = {}".format(self.traffic_value))
