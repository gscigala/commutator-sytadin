import dbus
import dbus.service
import dbus.mainloop.glib
from gi.repository import GLib
from .sytadin_data import SytadinData, URL

class SytadinDBusService(dbus.service.Object):
    def __init__(self, bus_name, update_interval, object_path='/com/commutator/Sytadin'):
        dbus.service.Object.__init__(self, bus_name, object_path)
        self.data = SytadinData(self.properties_changed, URL, update_interval)

    @dbus.service.signal('org.freedesktop.DBus.Properties', signature='sa{sv}as')
    def PropertiesChanged(self, interface_name, changed_properties, invalidated_properties):
        pass

    def properties_changed(self, changed_properties):
        self.PropertiesChanged('com.commutator.Sytadin', changed_properties, [])

    @dbus.service.method('org.freedesktop.DBus.Properties', in_signature='ss', out_signature='v')
    def Get(self, interface_name, property_name):
        try:
            return getattr(self.data, property_name)
        except AttributeError:
            raise dbus.exceptions.DBusException(
                f"Property '{property_name}' does not exist on interface '{interface_name}'",
                name='org.freedesktop.DBus.Error.UnknownProperty'
            )

    @dbus.service.method('org.freedesktop.DBus.Properties', in_signature='s', out_signature='a{sv}')
    def GetAll(self, interface_name):
        return {
            'traffic_level': self.data.traffic_level,
            'traffic_tendency': self.data.traffic_tendency,
            'traffic_value': self.data.traffic_value
        }

    def stop_auto_update(self):
        self.data.stop_auto_update()
