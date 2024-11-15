import logging
import requests
import re
import sys

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
        from bs4 import BeautifulSoup

        try:
            raw_html = requests.get(self._resource, timeout=10).text
            data = BeautifulSoup(raw_html, "html.parser")

            values = data.select(".barometre_niveau")
            self.traffic_level = values[0].select("img")[0].get('alt')

            values = data.select(".barometre_tendance")
            self.traffic_tendency = values[0].select("img")[0].get('alt')

            values = data.select(".barometre_valeur")
            parse_traffic_value = re.search(REGEX, values[0].text)
            if parse_traffic_value:
                self.traffic_value = parse_traffic_value.group()

        except requests.exceptions.ConnectionError:
            _LOGGER.error("Connection error")
            self.data = None

def main():
    data = SytadinData(URL)
    data.update()

    _LOGGER.info(f"traffic level = {data.traffic_level}")
    _LOGGER.info(f"traffic tendency = {data.traffic_tendency}")
    _LOGGER.info(f"traffic value = {data.traffic_value}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
