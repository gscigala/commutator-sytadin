import sys
import dbus
import dbus.mainloop.glib
from gi.repository import GLib
from .sytadin_dbus_service import SytadinDBusService

def main():
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    bus_name = dbus.service.BusName('com.example.Sytadin', dbus.SessionBus())
    sytadin_service = SytadinDBusService(bus_name)

    loop = GLib.MainLoop()
    loop.run()

if __name__ == "__main__":
    sys.exit(main())
