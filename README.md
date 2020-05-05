## Scany
Scany is a scanner for finding and displaying devices in your network.
It can be started as client and send your data to your server or it can be started as the server to make your data accessible for other applications like [CScany](https://github.com/ProjectJinx/CScany) or the [Scany App](https://github.com/ProjectJinx/ScanyApp).

## Usage

`Scany --URL http://yoururl.io`to start the client.

`Scany --server` to start the server.

`Scany --scan` to only start the scanner

## Dependencies

Scany uses [Scapy](https://scapy.net), [Dataset](https://dataset.readthedocs.io/en/latest/), [Flask](https://flask.palletsprojects.com/en/1.1.x/) and [Werkzeug](https://werkzeug.palletsprojects.com/en/1.0.x/)
