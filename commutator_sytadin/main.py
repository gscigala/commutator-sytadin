import logging
import requests
import re
import sys
import dbus
import dbus.service
import dbus.mainloop.glib
from gi.repository import GLib
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

class SytadinDBusService(dbus.service.Object):
    def __init__(self, bus_name, object_path='/com/example/Sytadin'):
        dbus.service.Object.__init__(self, bus_name, object_path)
        self.data = SytadinData(URL)

    @dbus.service.method('com.example.Sytadin', in_signature='', out_signature='')
    def update(self):
        self.data.update()
        self.PropertiesChanged(
            'com.example.Sytadin',
            {
                'traffic_level': self.data.traffic_level,
                'traffic_tendency': self.data.traffic_tendency,
                'traffic_value': self.data.traffic_value
            },
            []
        )

    @dbus.service.signal('org.freedesktop.DBus.Properties', signature='sa{sv}as')
    def PropertiesChanged(self, interface_name, changed_properties, invalidated_properties):
        pass

    @dbus.service.method('org.freedesktop.DBus.Properties', in_signature='ss', out_signature='v')
    def Get(self, interface_name, property_name):
        return getattr(self.data, property_name)

    @dbus.service.method('org.freedesktop.DBus.Properties', in_signature='s', out_signature='a{sv}')
    def GetAll(self, interface_name):
        return {
            'traffic_level': self.data.traffic_level,
            'traffic_tendency': self.data.traffic_tendency,
            'traffic_value': self.data.traffic_value
        }

def main():
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    bus_name = dbus.service.BusName('com.example.Sytadin', dbus.SessionBus())
    sytadin_service = SytadinDBusService(bus_name)

    loop = GLib.MainLoop()
    loop.run()

if __name__ == "__main__":
    sys.exit(main())
