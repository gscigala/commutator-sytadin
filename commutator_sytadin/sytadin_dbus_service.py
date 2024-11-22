import dbus
import dbus.service
import dbus.mainloop.glib
from gi.repository import GLib
from .sytadin_data import SytadinData, URL

class SytadinDBusService(dbus.service.Object):
    def __init__(self, bus_name, object_path='/com/commutator/Sytadin'):
        dbus.service.Object.__init__(self, bus_name, object_path)
        self.data = SytadinData(URL)

    @dbus.service.method('com.commutator.Sytadin', in_signature='', out_signature='')
    def update(self):
        self.data.update()
        self.PropertiesChanged(
            'com.commutator.Sytadin',
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
