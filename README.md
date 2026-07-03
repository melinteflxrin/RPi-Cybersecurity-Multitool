# RPi Cybersecurity Multitool

A menu-driven cybersecurity toolkit for the Raspberry Pi, developed as a thesis
project. It bundles a collection of Bluetooth (BLE and Classic), WiFi, and
phishing tools behind a single terminal interface for security research and
educational purposes.

## Features

- **BLE** — AirPods spam, Apple advertisement spam, Android spam, name spoofing, device scanning
- **Bluetooth (Classic)** — L2CAP DoS
- **WiFi** — network scanning, beacon broadcast, AP network flooding, deauthentication, ESSID brute-force, packet capture, HTTP/local DoS
- **Phishing** — Facebook and Google credential-harvesting pages

## Requirements

- Raspberry Pi running a Linux OS (developed on a Pi Zero 2 W)
- Bluetooth adapter with BLE support
- WiFi adapter capable of monitor mode (for WiFi attacks)
- Root / `sudo` privileges

## Setup

The full, reproducible setup — every command needed to go from a fresh Raspberry
Pi to a working install — is documented in [SETUP.md](SETUP.md).

## Usage

From the repository root:

```bash
sudo python main.py
```

Navigate the menu by category (BLE / Bluetooth / WiFi / Phishing) and follow the
per-tool prompts.

## Attribution

Sources and inspirations are credited in [SOURCES.md](SOURCES.md).

## Disclaimer

This tool is for **educational purposes only**. Only use it on devices and
networks you own or have explicit, written permission to test. Unauthorized use
may violate laws and regulations, and is solely your responsibility. See
[LICENSE](LICENSE) for terms.
