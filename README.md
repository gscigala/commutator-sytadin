# Communator-Sytadin

Communator-Sytadin is an application that provides a DBus interface for accessing real-time traffic information from Sytadin. It allows you to fetch and monitor traffic levels, trends, and values, making it easy to integrate traffic data into other applications or services.

## Installation

	pip install .

## Usage

To start the program, run:

	commutator-sytadin

You can also use the --session flag to use the DBus session bus instead of the system bus:

	commutator-sytadin --session
	
Additionally, you can specify the update interval in seconds using the --update-interval flag. The default interval is 480 seconds (8 minutes):

	commutator-sytadin --update-interval 600

## DBus Interface

### Properties

    traffic_level: The current level of traffic.
    traffic_tendency: The current trend of traffic.
    traffic_value: The current traffic value in kilometers.

### Possible Values

#### **Traffic Level**

- **Low**
- **Normal**
- **Unusual**
- **Exceptional**

#### **Traffic Tendency**

- **Increasing**
- **Decreasing**
- **Stable**

## Systemd Service

The project includes a systemd service file to manage the service using systemd. The service file is located at systemd/commutator-sytadin.service.

## DBus Configuration

The project includes a DBus configuration file to set the necessary permissions for the DBus service. The configuration file is located at dbus/com.commutator.Sytadin.conf.

## Testing

To run the tests, use the following command:

```sh
python -m unittest discover -s tests
