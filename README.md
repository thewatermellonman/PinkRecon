# ♡ PinkRecon ♡
PinkRecon is a cute and practical network reconnaissance tool built with Python, JavaScipt, HTML, and CSS. 

ONLY USE PINKRECON ON NETWORKS AND DEVICES YOU OWN OR HAVE EXPLICIT PERMISSION TO TEST.

## Features

Scans a specified local network, identifies online hosts, and records IP addresses.
Supports /24 networks
PinkRecon checks for common TCP ports

PinkRecon records port number, port state, connection latency, likely service, and service benner (when availible) for open ports

## Project Structure
discovery.py discovers devices on the target network
scanner.py does TCP port scanning and collects info
services.py attempts to retrieve service banners
network_scan.py combines host discovery and port scanning
app.py runs the Flask web server and provides the /scan API endpoint used by the dashboard

## Requirements
-Python 3.13+
-Flask
-Scapy

Install python dependencies with

python -m pip install flask scapy

## Running it
Clone the repo

git clone https://github.com/thewatermellonman/PinkRecon.git

Start the Flask server from the project directory

cd PinkRecon
python backend\app.py

Then open http://127.0.0.1:5000

Enter a network and press SCAN