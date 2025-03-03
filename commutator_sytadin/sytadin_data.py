import logging
import requests
import re
from bs4 import BeautifulSoup
import threading
import sdnotify

logging.basicConfig(level=logging.INFO)
_LOGGER = logging.getLogger(__name__)

URL = "http://www.sytadin.fr/sys/barometres_de_la_circulation.jsp.html"

REGEX = r'(\d*\.\d+|\d+)'

class SytadinData:
    """The class for handling the data retrieval."""

    def __init__(self, properties_changed_callback, resource, update_interval):
        """Initialize the data object."""
        self.resource = resource
        self.traffic_level = ''
        self.traffic_tendency = ''
        self.traffic_value = ''
        self.timer = None
        self.properties_changed_callback = properties_changed_callback
        self.update_interval = update_interval
        self.auto_update()
        sdnotify.SystemdNotifier().notify("READY=1")

    def auto_update(self):
        """Update the data and restart the timer."""
        try:
            self.update()
        except Exception as e:
            _LOGGER.error("Error in auto_update: {}".format(e))
        finally:
            self.timer = threading.Timer(self.update_interval, self.auto_update)
            self.timer.start()

    def stop_auto_update(self):
        """Stop the auto-update timer."""
        if self.timer:
            self.timer.cancel()
            self.timer = None

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
            raw_html = requests.get(self.resource, timeout=10).text
            data = BeautifulSoup(raw_html, "html.parser")

        except Exception as e:
            _LOGGER.error("Connection error: {}".format(e))
            self.data = None
            raise ConnectionError("Failed to connect to the resource")

        try:
            values = data.select(".barometre_niveau")
            traffic_level_fr = values[0].select("img")[0].get('alt')
            new_traffic_level = translation_dict.get(traffic_level_fr, traffic_level_fr)
            _LOGGER.info("traffic_level = {}".format(new_traffic_level))

            values = data.select(".barometre_tendance")
            traffic_tendency_fr = values[0].select("img")[0].get('alt')
            new_traffic_tendency = translation_dict.get(traffic_tendency_fr, traffic_tendency_fr)
            _LOGGER.info("traffic_tendency = {}".format(new_traffic_tendency))

            values = data.select(".barometre_valeur")
            parse_traffic_value = re.search(REGEX, values[0].text)
            new_traffic_value = parse_traffic_value.group() if parse_traffic_value else ''
            _LOGGER.info("traffic_value = {}".format(new_traffic_value))

        except:
            raise ConnectionError("Error in data parsing")

        changed_properties = {}

        if new_traffic_level != self.traffic_level:
            _LOGGER.info("new traffic_level!")
            self.traffic_level = new_traffic_level
            changed_properties['traffic_level'] = new_traffic_level

        if new_traffic_tendency != self.traffic_tendency:
            _LOGGER.info("new traffic_tendency!")
            self.traffic_tendency = new_traffic_tendency
            changed_properties['traffic_tendency'] = new_traffic_tendency

        if new_traffic_value != self.traffic_value:
            _LOGGER.info("new traffic_value!")
            self.traffic_value = new_traffic_value
            changed_properties['traffic_value'] = new_traffic_value

        if changed_properties:
            self.properties_changed_callback(changed_properties)
