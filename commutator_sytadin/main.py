import sys
import signal
import dbus
import dbus.mainloop.glib
from gi.repository import GLib
from .sytadin_dbus_service import SytadinDBusService

def signal_handler(signum, frame):
    print("SIGINT received, stopping the service...")
    loop.quit()

def main():
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    bus_name = dbus.service.BusName('com.example.Sytadin', dbus.SessionBus())
    sytadin_service = SytadinDBusService(bus_name)

    global loop
    loop = GLib.MainLoop()

    signal.signal(signal.SIGINT, signal_handler)

    loop.run()

if __name__ == "__main__":
    sys.exit(main())
