import sys
import argparse
import signal
import dbus
import dbus.mainloop.glib
from gi.repository import GLib
from commutator_sytadin.sytadin_dbus_service import SytadinDBusService

def signal_handler(signum, frame):
    print("SIGINT received, stopping the service...")
    sytadin_service.stop_auto_update()
    loop.quit()

def main():
    parser = argparse.ArgumentParser(description='Sytadin Data Service')
    parser.add_argument('--session', action='store_true', help='Use DBus session bus instead of system bus')
    parser.add_argument('--update-interval', type=int, default=300, help='Update interval in seconds (default: 300)')
    args = parser.parse_args()

    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    bus_name = dbus.service.BusName('com.commutator.Sytadin', dbus.SystemBus() if not args.session else dbus.SessionBus())
    global sytadin_service
    sytadin_service = SytadinDBusService(bus_name, args.update_interval)

    global loop
    loop = GLib.MainLoop()

    signal.signal(signal.SIGINT, signal_handler)

    loop.run()

if __name__ == "__main__":
    sys.exit(main())
